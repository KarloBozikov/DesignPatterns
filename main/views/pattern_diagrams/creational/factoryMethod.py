import os
import pygame
from PySide6.QtCore import QTimer
from PySide6.QtGui import QPixmap
from ..PatternAnimation import PatternAnimation


class FactoryAnimation(PatternAnimation):
    """Factory Method animation drawn directly into DiagramView."""

    def __init__(self, view: "DiagramView"):
        super().__init__(view)

        # Load resources
        current_dir = os.path.dirname(os.path.abspath(__file__))
        base_path = os.path.normpath(
            os.path.join(current_dir, "../../../../main/resources/diagrams/creational_patterns/factory_method/")
        )
        self.drawing_img_orig = pygame.image.load(os.path.join(base_path, "drawing.png"))
        self.pen_img_orig = pygame.image.load(os.path.join(base_path, "pen.png"))
        self.pencil_img_orig = pygame.image.load(os.path.join(base_path, "pencil.png"))
        self.brush_img_orig = pygame.image.load(os.path.join(base_path, "paint_brush.png"))

        # Initialize positions
        self.reset_positions()
        self.speed = 5
        self.paused = False

    # ---------------- Helpers ----------------

    def reset_positions(self):
        """Set initial positions of drawing tools and canvas."""
        w, h = self.view.width(), self.view.height()
        sx, sy = self.scale_factor()

        # Drawing canvas at top center
        self.canvas_pos = (int(w * 0.5 - 100 * sx), int(50 * sy))

        # Tools start at the bottom
        self.pen_pos = [int(150 * sx), int(h - 200 * sy)]
        self.pencil_pos = [int(w * 0.5 - 60 * sx), int(h - 200 * sy)]
        self.brush_pos = [int(w - 250 * sx), int(h - 200 * sy)]

        # Save originals for reset
        self.pen_pos_orig = list(self.pen_pos)
        self.pencil_pos_orig = list(self.pencil_pos)
        self.brush_pos_orig = list(self.brush_pos)

    def move_towards(self, current, target, step):
        if current < target:
            return current + min(step, target - current)
        elif current > target:
            return current - min(step, current - target)
        return current

    def scale_elements(self):
        """Scale images according to view size."""
        sx, sy = self.scale_factor()

        drawing_img = pygame.transform.scale(self.drawing_img_orig, (int(200 * sx), int(150 * sy)))
        pen_img = pygame.transform.scale(self.pen_img_orig, (int(60 * sx), int(120 * sy)))
        pencil_img = pygame.transform.scale(self.pencil_img_orig, (int(60 * sx), int(120 * sy)))
        brush_img = pygame.transform.scale(self.brush_img_orig, (int(80 * sx), int(120 * sy)))

        return drawing_img, self.canvas_pos, pen_img, self.pen_pos, pencil_img, self.pencil_pos, brush_img, self.brush_pos

    # ---------------- Frame Update ----------------

    def update_frame(self):
        if self.paused:
            return

        frame_surface = self.create_surface()

        # --- Scale elements ---
        (drawing_img, canvas_pos,
         pen_img, pen_pos,
         pencil_img, pencil_pos,
         brush_img, brush_pos) = self.scale_elements()

        # Draw canvas at top
        frame_surface.blit(drawing_img, canvas_pos)

        # --- Arrow source: bottom center of drawing icon ---
        source_center = (
            canvas_pos[0] + drawing_img.get_width() // 2,
            canvas_pos[1] + drawing_img.get_height()     # bottom edge instead of middle
        )

        # Frame counter
        if not hasattr(self, "frame_count"):
            self.frame_count = 0
        self.frame_count += 1

        # Timing
        arrow_growth_speed = 15
        show_tools_at = 20
        show_labels_at = 50

        # Arrow style
        arrow_color = (255, 255, 255)
        arrow_thickness = 8

        # --- Growing arrow helper ---
        def draw_growing_arrow(surface, start, end, progress, color=(255, 255, 255)):
            dx, dy = end[0] - start[0], end[1] - start[1]
            length = max(1, (dx ** 2 + dy ** 2) ** 0.5)
            ux, uy = dx / length, dy / length
            current_len = min(progress, length)
            mid = (start[0] + ux * current_len, start[1] + uy * current_len)

            pygame.draw.line(surface, color, start, mid, arrow_thickness)

            if progress >= length:
                arrow_size = 14
                perp = (-uy, ux)
                p1 = (end[0] - ux * arrow_size + perp[0] * arrow_size / 2,
                      end[1] - uy * arrow_size + perp[1] * arrow_size / 2)
                p2 = (end[0] - ux * arrow_size - perp[0] * arrow_size / 2,
                      end[1] - uy * arrow_size - perp[1] * arrow_size / 2)
                pygame.draw.polygon(surface, color, [end, p1, p2])

        # --- Arrow targets: top edge of each tool ---
        pen_target = (pen_pos[0] + pen_img.get_width() // 2, pen_pos[1])
        pencil_target = (pencil_pos[0] + pencil_img.get_width() // 2, pencil_pos[1])
        brush_target = (brush_pos[0] + brush_img.get_width() // 2, brush_pos[1])

        # --- Step 1: animate arrows from drawing -> tools ---
        progress = self.frame_count * arrow_growth_speed
        draw_growing_arrow(frame_surface, source_center, pen_target, progress, arrow_color)
        draw_growing_arrow(frame_surface, source_center, pencil_target, progress, arrow_color)
        draw_growing_arrow(frame_surface, source_center, brush_target, progress, arrow_color)

        # --- Step 2: show tools ---
        if self.frame_count >= show_tools_at:
            frame_surface.blit(pen_img, pen_pos)
            frame_surface.blit(pencil_img, pencil_pos)
            frame_surface.blit(brush_img, brush_pos)

            # --- Step 3: show labels (multiline) ---
            if self.frame_count >= show_labels_at:
                font = pygame.font.SysFont("Arial", 26)
                labels = {
                    "Pen": (pen_pos[0], pen_pos[1] + pen_img.get_height() + 15),
                    "Pencil": (pencil_pos[0], pencil_pos[1] + pencil_img.get_height() + 15),
                    "Brush": (brush_pos[0], brush_pos[1] + brush_img.get_height() + 15),
                }

                for tool, pos in labels.items():
                    line1 = "DrawingApp uses:"
                    line2 = f"{tool.lower()}.draw()"

                    surf1 = font.render(line1, True, arrow_color)
                    surf2 = font.render(line2, True, arrow_color)

                    frame_surface.blit(surf1, pos)
                    frame_surface.blit(surf2, (pos[0], pos[1] + surf1.get_height() + 2))

        # --- Loop ---
        if self.frame_count > 480:
            self.frame_count = 0
            self.reset_positions()

        # Convert → QImage → QLabel
        qimg = self.to_qimage(frame_surface)
        self.label.setPixmap(QPixmap.fromImage(qimg))

    def resume(self):
        """Reset and restart animation loop."""
        self.reset_positions()
        self.paused = False
        self.timer.start(1000 // 60)
