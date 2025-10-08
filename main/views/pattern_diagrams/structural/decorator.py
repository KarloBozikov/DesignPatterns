import os
import pygame
from ..PatternAnimation import PatternAnimation

class DecoratorAnimation(PatternAnimation):
    """Decorator pattern animation drawn directly into DiagramView."""

    def __init__(self, view: "DiagramView"):
        super().__init__(view)

        # Load resources
        current_dir = os.path.dirname(os.path.abspath(__file__))
        base_path = os.path.normpath(
            os.path.join(current_dir, "../../../../main/resources/diagrams/structural_patterns/decorator/")
        )
        self.plain_img = pygame.image.load(os.path.join(base_path, "plainIceCream.png"))
        self.chocolate_img = pygame.image.load(os.path.join(base_path, "chocolate.png"))
        self.nuts_img = pygame.image.load(os.path.join(base_path, "nuts.png"))
        self.nutIce_img = pygame.image.load(os.path.join(base_path, "nutIceCream.png"))
        self.chocoIce_img = pygame.image.load(os.path.join(base_path, "chokoIceCream.png"))

        # Initialize
        self.reset_positions()
        self.frame_count = 0
        self.paused = False

    # ---------------- Helpers ----------------

    def reset_positions(self):
        w, h = self.view.width(), self.view.height()
        sx, sy = self.scale_factor()

        # Base plain ice cream in a center
        self.plain_pos = (int(w * 0.4), int(h * 0.15))

        # Decorators around it
        self.choco_pos = (int(w * 0.2), int(h * 0.55))
        self.nuts_pos = (int(w * 0.65), int(h * 0.55))

        # Results (decorated ice creams)
        self.chocoIce_pos = (int(w * 0.2), int(h * 0.8))
        self.nutIce_pos = (int(w * 0.65), int(h * 0.8))

    def scale_elements(self):
        plain = self.scale_image(self.plain_img, 120, 180)
        choco = self.scale_image(self.chocolate_img, 100, 100)
        nuts = self.scale_image(self.nuts_img, 100, 100)
        nutIce = self.scale_image(self.nutIce_img, 120, 180)
        chocoIce = self.scale_image(self.chocoIce_img, 120, 180)
        return plain, choco, nuts, nutIce, chocoIce

    # ---------------- Frame Update ----------------

    def update_frame(self):
        if self.paused:
            return

        surface = self.create_surface()
        plain, choco, nuts, nutIce, chocoIce = self.scale_elements()

        # Draw plain ice cream
        surface.blit(plain, self.plain_pos)

        # Centers
        plain_center = (self.plain_pos[0] + plain.get_width() // 2,
                        self.plain_pos[1] + plain.get_height() // 2)
        choco_center = (self.choco_pos[0] + choco.get_width() // 2,
                        self.choco_pos[1] + choco.get_height() // 2)
        nuts_center = (self.nuts_pos[0] + nuts.get_width() // 2,
                       self.nuts_pos[1] + nuts.get_height() // 2)

        # Step through phases
        self.frame_count += 1
        arrow_growth_speed = 15

        # Always show decorator ingredients
        surface.blit(choco, self.choco_pos)
        surface.blit(nuts, self.nuts_pos)

        # Phase 1: Chocolate decorator
        if self.frame_count > 30:
            progress = (self.frame_count - 30) * arrow_growth_speed
            self.draw_growing_arrow(surface, choco_center, plain_center, progress)
            surface.blit(chocoIce, self.chocoIce_pos)
            lbl = self.font.render("Plain + Chocolate", True, (255, 255, 255))
            surface.blit(lbl, (self.chocoIce_pos[0], self.chocoIce_pos[1] - 25))

        # Phase 2: Nuts decorator
        if self.frame_count > 60:
            progress = (self.frame_count - 60) * arrow_growth_speed
            self.draw_growing_arrow(surface, nuts_center, plain_center, progress)
            surface.blit(nutIce, self.nutIce_pos)
            lbl = self.font.render("Plain + Nuts", True, (255, 255, 255))
            surface.blit(lbl, (self.nutIce_pos[0], self.nutIce_pos[1] - 25))

        # Loop
        if self.frame_count > 200:
            self.frame_count = 0

        # Finalize
        self.finalize_frame(surface)
