import os
import pygame
from ..PatternAnimation import PatternAnimation

class PrototypeAnimation(PatternAnimation):
    """Prototype pattern animation drawn directly into the DiagramView."""

    def __init__(self, view: "DiagramView"):
        super().__init__(view)

        # Load resources
        current_dir = os.path.dirname(os.path.abspath(__file__))
        base_path = os.path.normpath(
            os.path.join(current_dir, "../../../../main/resources/diagrams/creational_patterns/prototype/")
        )
        self.key_img_orig = pygame.image.load(os.path.join(base_path, "key.png"))

        # Initialize
        self.reset_positions()
        self.frame_count = 0
        self.paused = False

    # ---------------- Helpers ----------------

    def reset_positions(self):
        """Set positions for the prototype and its clones."""
        w, h = self.view.width(), self.view.height()
        sx, sy = self.scale_factor()

        # Prototype at the top center
        self.prototype_pos = (int(w * 0.5 - 50 * sx), int(80 * sy))

        # Two clones side by side below
        self.clone_positions = [
            (int(w * 0.35 - 50 * sx), int(h * 0.55)),
            (int(w * 0.65 - 50 * sx), int(h * 0.55)),
        ]

    def scale_elements(self):
        """Return scaled prototype image."""
        return self.scale_image(self.key_img_orig, 100, 100)

    # ---------------- Frame Update ----------------

    def update_frame(self):
        if self.paused:
            return

        surface = self.create_surface()
        key_img = self.scale_elements()

        # Draw prototype
        surface.blit(key_img, self.prototype_pos)

        # Start point (bottom center of prototype)
        proto_center = (
            self.prototype_pos[0] + key_img.get_width() // 2,
            self.prototype_pos[1] + key_img.get_height()
        )

        self.frame_count += 1
        arrow_growth_speed = 15

        # Step 1: arrows towards clones
        progress = self.frame_count * arrow_growth_speed
        for clone_pos in self.clone_positions:
            target = (clone_pos[0] + key_img.get_width() // 2, clone_pos[1])
            self.draw_growing_arrow(surface, proto_center, target, progress)

        # Step 2: draw clones
        if self.frame_count > 20:
            for clone_pos in self.clone_positions:
                surface.blit(key_img, clone_pos)

        # Step 3: labels
        if self.frame_count > 40:
            proto_label = self.font.render("Original", True, (255, 255, 255))
            surface.blit(
                proto_label,
                (self.prototype_pos[0] + key_img.get_width() // 2 - proto_label.get_width() // 2,
                 self.prototype_pos[1] - 30)
            )

            for i, clone_pos in enumerate(self.clone_positions, start=1):
                clone_label = self.font.render(f"Copy {i}", True, (255, 255, 255))
                surface.blit(
                    clone_label,
                    (clone_pos[0] + key_img.get_width() // 2 - clone_label.get_width() // 2,
                     clone_pos[1] + key_img.get_height() + 5)
                )

        # Loop
        if self.frame_count > 360:
            self.frame_count = 0
            self.reset_positions()

        # Finalize
        self.finalize_frame(surface)
