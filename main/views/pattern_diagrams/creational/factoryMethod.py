import os
import pygame
from ..PatternAnimation import PatternAnimation

class FactoryAnimation(PatternAnimation):
    """Factory Method pattern animation."""

    def __init__(self, view: "DiagramView"):
        super().__init__(view)

        # Load resources
        current_dir = os.path.dirname(os.path.abspath(__file__))
        base_path = os.path.normpath(
            os.path.join(current_dir, "../../../../main/resources/diagrams/creational_patterns/factory_method/")
        )
        self.imgs = {
            "drawing": pygame.image.load(os.path.join(base_path, "drawing.png")),
            "pen": pygame.image.load(os.path.join(base_path, "pen.png")),
            "pencil": pygame.image.load(os.path.join(base_path, "pencil.png")),
            "brush": pygame.image.load(os.path.join(base_path, "paint_brush.png")),
        }

        self.reset_positions()
        self.frame_count = 0
        self.paused = False

    # ---------------- Helpers ----------------

    def reset_positions(self):
        w, h = self.view.width(), self.view.height()
        sx, sy = self.scale_factor()

        # Drawing canvas at the top center
        self.canvas_pos = (int(w * 0.5 - 100 * sx), int(50 * sy))

        # Tools start at the bottom
        self.pen_pos = [int(150 * sx), int(h - 200 * sy)]
        self.pencil_pos = [int(w * 0.5 - 60 * sx), int(h - 200 * sy)]
        self.brush_pos = [int(w - 250 * sx), int(h - 200 * sy)]

    def scale_elements(self):
        drawing = self.scale_image(self.imgs["drawing"], 200, 150)
        pen = self.scale_image(self.imgs["pen"], 60, 120)
        pencil = self.scale_image(self.imgs["pencil"], 60, 120)
        brush = self.scale_image(self.imgs["brush"], 80, 120)
        return drawing, pen, pencil, brush

    # ---------------- Frame Update ----------------

    def update_frame(self):
        if self.paused:
            return

        surface = self.create_surface()
        drawing_img, pen_img, pencil_img, brush_img = self.scale_elements()

        # Draw canvas
        surface.blit(drawing_img, self.canvas_pos)

        # Source = bottom center of drawing canvas
        source_center = (
            self.canvas_pos[0] + drawing_img.get_width() // 2,
            self.canvas_pos[1] + drawing_img.get_height()
        )

        # Frame counter
        self.frame_count += 1

        # Timings
        arrow_growth_speed = 15
        show_tools_at = 20
        show_labels_at = 50

        # Targets = top of each tool
        pen_target = (self.pen_pos[0] + pen_img.get_width() // 2, self.pen_pos[1])
        pencil_target = (self.pencil_pos[0] + pencil_img.get_width() // 2, self.pencil_pos[1])
        brush_target = (self.brush_pos[0] + brush_img.get_width() // 2, self.brush_pos[1])

        # Step 1: animate arrows
        progress = self.frame_count * arrow_growth_speed
        self.draw_growing_arrow(surface, source_center, pen_target, progress)
        self.draw_growing_arrow(surface, source_center, pencil_target, progress)
        self.draw_growing_arrow(surface, source_center, brush_target, progress)

        # Step 2: show tools
        if self.frame_count >= show_tools_at:
            surface.blit(pen_img, self.pen_pos)
            surface.blit(pencil_img, self.pencil_pos)
            surface.blit(brush_img, self.brush_pos)

            # Step 3: show labels
            if self.frame_count >= show_labels_at:
                labels = {
                    "Pen": (self.pen_pos[0], self.pen_pos[1] + pen_img.get_height() + 15),
                    "Pencil": (self.pencil_pos[0], self.pencil_pos[1] + pencil_img.get_height() + 15),
                    "Brush": (self.brush_pos[0], self.brush_pos[1] + brush_img.get_height() + 15),
                }
                for tool, pos in labels.items():
                    line1 = "DrawingApp uses:"
                    line2 = f"{tool.lower()}.draw()"

                    surf1 = self.font.render(line1, True, (255, 255, 255))
                    surf2 = self.font.render(line2, True, (255, 255, 255))

                    surface.blit(surf1, pos)
                    surface.blit(surf2, (pos[0], pos[1] + surf1.get_height() + 2))

        # Loop reset
        if self.frame_count > 480:
            self.frame_count = 0
            self.reset_positions()

        # Finalize frame
        self.finalize_frame(surface)

    def resume(self):
        self.reset_positions()
        self.paused = False
        self.timer.start(1000 // 60)
