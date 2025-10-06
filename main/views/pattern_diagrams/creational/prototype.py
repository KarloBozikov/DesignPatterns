import os
import pygame
from PySide6.QtCore import QTimer
from PySide6.QtGui import QPixmap
from ..PatternAnimation import PatternAnimation


class PrototypeAnimation(PatternAnimation):
    """Prototype pattern animation drawn directly into DiagramView."""

    def __init__(self, view: "DiagramView"):
        super().__init__(view)

        # Load resources
        current_dir = os.path.dirname(os.path.abspath(__file__))
        base_path = os.path.normpath(
            os.path.join(current_dir, "../../../../main/resources/diagrams/creational_patterns/prototype/")
        )
        self.key_img = pygame.image.load(os.path.join(base_path, "key.png"))

        # Initialize
        self.reset_positions()
        self.frame_count = 0
        self.paused = False

    # ---------------- Helpers ----------------

    def reset_positions(self):
        """Set positions for prototype and two clones."""
        w, h = self.view.width(), self.view.height()
        sx, sy = self.scale_factor()

        # Prototype at top center
        self.prototype_pos = (int(w * 0.5 - 50 * sx), int(80 * sy))

        # Two clones side by side below
        self.clone_positions = [
            (int(w * 0.35 - 50 * sx), int(h * 0.55)),  # left clone
            (int(w * 0.65 - 50 * sx), int(h * 0.55)),  # right clone
        ]

    def scale_elements(self):
        sx, sy = self.scale_factor()
        key_img = pygame.transform.scale(self.key_img, (int(100 * sx), int(100 * sy)))
        return key_img

    # ---------------- Frame Update ----------------

    def update_frame(self):
        if self.paused:
            return

        frame_surface = self.create_surface()
        key_img = self.scale_elements()

        # Draw prototype
        frame_surface.blit(key_img, self.prototype_pos)

        # Start point (bottom center of prototype)
        proto_center = (
            self.prototype_pos[0] + key_img.get_width() // 2,
            self.prototype_pos[1] + key_img.get_height()
        )

        self.frame_count += 1
        arrow_growth_speed = 15
        arrow_color = (255, 255, 255)
        arrow_thickness = 6

        def draw_arrow(surface, start, end, progress):
            dx, dy = end[0] - start[0], end[1] - start[1]
            length = max(1, (dx ** 2 + dy ** 2) ** 0.5)
            ux, uy = dx / length, dy / length
            current_len = min(progress, length)
            mid = (start[0] + ux * current_len, start[1] + uy * current_len)
            pygame.draw.line(surface, arrow_color, start, mid, arrow_thickness)
            if progress >= length:
                arrow_size = 12
                perp = (-uy, ux)
                p1 = (end[0] - ux * arrow_size + perp[0] * arrow_size / 2,
                      end[1] - uy * arrow_size + perp[1] * arrow_size / 2)
                p2 = (end[0] - ux * arrow_size - perp[0] * arrow_size / 2,
                      end[1] - uy * arrow_size - perp[1] * arrow_size / 2)
                pygame.draw.polygon(surface, arrow_color, [end, p1, p2])

        # Step 1: animate arrows to clone positions
        progress = self.frame_count * arrow_growth_speed
        for clone_pos in self.clone_positions:
            target = (clone_pos[0] + key_img.get_width() // 2, clone_pos[1])
            draw_arrow(frame_surface, proto_center, target, progress)

        # Step 2: show clones
        if self.frame_count > 20:
            for clone_pos in self.clone_positions:
                frame_surface.blit(key_img, clone_pos)

        # Step 3: labels
        if self.frame_count > 40:
            font = pygame.font.SysFont("Arial", 24, bold=True)

            # Label above prototype
            proto_label = font.render("Original", True, arrow_color)
            frame_surface.blit(
                proto_label,
                (self.prototype_pos[0] + key_img.get_width() // 2 - proto_label.get_width() // 2,
                 self.prototype_pos[1] - 30)
            )

            # Labels below clones
            for i, clone_pos in enumerate(self.clone_positions, start=1):
                clone_label = font.render(f"Copy {i}", True, arrow_color)
                frame_surface.blit(
                    clone_label,
                    (clone_pos[0] + key_img.get_width() // 2 - clone_label.get_width() // 2,
                     clone_pos[1] + key_img.get_height() + 5)
                )

        # Loop after ~6 sec
        if self.frame_count > 360:
            self.frame_count = 0
            self.reset_positions()

        # Convert → QImage → QLabel
        qimg = self.to_qimage(frame_surface)
        self.label.setPixmap(QPixmap.fromImage(qimg))
