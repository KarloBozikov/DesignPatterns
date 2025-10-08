import os
import pygame
from ..PatternAnimation import PatternAnimation

class CompositeAnimation(PatternAnimation):
    """Composite pattern animation drawn directly into the DiagramView."""

    def __init__(self, view: "DiagramView"):
        super().__init__(view)

        # Load resources
        current_dir = os.path.dirname(os.path.abspath(__file__))
        base_path = os.path.normpath(
            os.path.join(current_dir, "../../../../main/resources/diagrams/structural_patterns/composite/")
        )
        self.package_img = pygame.image.load(os.path.join(base_path, "package.png"))
        self.headphones_img = pygame.image.load(os.path.join(base_path, "headphones.png"))
        self.laptop_img = pygame.image.load(os.path.join(base_path, "laptop.png"))
        self.smartphone_img = pygame.image.load(os.path.join(base_path, "smartphone.png"))

        # Initialize
        self.reset_positions()
        self.frame_count = 0
        self.paused = False

    # ---------------- Helpers ----------------

    def reset_positions(self):
        """Arrange package at top, items below."""
        w, h = self.view.width(), self.view.height()
        sx, sy = self.scale_factor()

        # Package at the top center
        self.package_pos = (int(w * 0.5 - 80 * sx), int(50 * sy))

        # Items below
        self.headphones_pos = (int(w * 0.2), int(h * 0.55))
        self.laptop_pos = (int(w * 0.45), int(h * 0.55))
        self.smartphone_pos = (int(w * 0.7), int(h * 0.55))

    def scale_elements(self):
        package = self.scale_image(self.package_img, 160, 140)
        headphones = self.scale_image(self.headphones_img, 120, 120)
        laptop = self.scale_image(self.laptop_img, 150, 120)
        smartphone = self.scale_image(self.smartphone_img, 100, 120)
        return package, headphones, laptop, smartphone

    # ---------------- Frame Update ----------------

    def update_frame(self):
        if self.paused:
            return

        surface = self.create_surface()
        package, headphones, laptop, smartphone = self.scale_elements()

        # Draw package
        surface.blit(package, self.package_pos)

        # Draw items
        surface.blit(headphones, self.headphones_pos)
        surface.blit(laptop, self.laptop_pos)
        surface.blit(smartphone, self.smartphone_pos)

        # Centers
        package_center = (self.package_pos[0] + package.get_width() // 2,
                          self.package_pos[1] + package.get_height())
        headphone_center = (self.headphones_pos[0] + headphones.get_width() // 2,
                            self.headphones_pos[1])
        laptop_center = (self.laptop_pos[0] + laptop.get_width() // 2,
                         self.laptop_pos[1])
        smartphone_center = (self.smartphone_pos[0] + smartphone.get_width() // 2,
                             self.smartphone_pos[1])

        # Animate arrows downward (Package → Items)
        self.frame_count += 1
        progress = self.frame_count * 15
        self.draw_growing_arrow(surface, package_center, headphone_center, progress)
        self.draw_growing_arrow(surface, package_center, laptop_center, progress)
        self.draw_growing_arrow(surface, package_center, smartphone_center, progress)

        # Labels
        package_text = ["Order", "2520$"]
        for i, line in enumerate(package_text):
            label = self.font.render(line, True, (255, 255, 0))
            surface.blit(label, (self.package_pos[0], self.package_pos[1] - 60 + i * 28))

        labels = {
            "Headphones\n120$": (self.headphones_pos[0], self.headphones_pos[1] + headphones.get_height() + 10),
            "Laptop\n1600$": (self.laptop_pos[0], self.laptop_pos[1] + laptop.get_height() + 10),
            "Smartphone\n800$": (self.smartphone_pos[0], self.smartphone_pos[1] + smartphone.get_height() + 10),
        }

        for text, pos in labels.items():
            for i, line in enumerate(text.splitlines()):
                label = self.font.render(line, True, (255, 255, 255))
                surface.blit(label, (pos[0], pos[1] + i * 28))

        # Loop
        if self.frame_count > 200:
            self.frame_count = 0

        # Finalize
        self.finalize_frame(surface)
