import os
import pygame
from ..PatternAnimation import PatternAnimation

class AbstractAnimation(PatternAnimation):
    """Abstract Factory pattern animation."""

    def __init__(self, view: "DiagramView"):
        super().__init__(view)

        # Load resources
        current_dir = os.path.dirname(os.path.abspath(__file__))
        base_path = os.path.normpath(
            os.path.join(current_dir, "../../../../main/resources/diagrams/creational_patterns/abstract_factory/")
        )
        self.imgs = {
            "factory": pygame.image.load(os.path.join(base_path, "factory.png")),
            "classic_chair": pygame.image.load(os.path.join(base_path, "classic_chair.png")),
            "classic_sofa": pygame.image.load(os.path.join(base_path, "classic_sofa.png")),
            "modern_chair": pygame.image.load(os.path.join(base_path, "modern_chair.png")),
            "modern_sofa": pygame.image.load(os.path.join(base_path, "modern_sofa.png")),
        }

        # Init
        self.reset_positions()
        self.frame_count = 0
        self.paused = False

    # ---------------- Helpers ----------------

    def reset_positions(self):
        """Set positions for factory and product families."""
        w, h = self.view.width(), self.view.height()
        sx, sy = self.scale_factor()

        # Main factory at top
        self.factory_pos = (int(w * 0.5 - 90 * sx), int(40 * sy))

        # Classic family (left)
        self.classic_group_pos = (int(w * 0.25 - 120 * sx), int(h * 0.45))
        self.classic_chair_pos = (self.classic_group_pos[0], self.classic_group_pos[1])
        self.classic_sofa_pos = (self.classic_group_pos[0] + int(120 * sx), self.classic_group_pos[1])

        # Modern family (right)
        self.modern_group_pos = (int(w * 0.65 - 120 * sx), int(h * 0.45))
        self.modern_chair_pos = (self.modern_group_pos[0], self.modern_group_pos[1])
        self.modern_sofa_pos = (self.modern_group_pos[0] + int(120 * sx), self.modern_group_pos[1])

    def scale_elements(self):
        """Return scaled images and positions."""
        factory = self.scale_image(self.imgs["factory"], 180, 120)
        classic_chair = self.scale_image(self.imgs["classic_chair"], 90, 90)
        classic_sofa = self.scale_image(self.imgs["classic_sofa"], 120, 90)
        modern_chair = self.scale_image(self.imgs["modern_chair"], 90, 90)
        modern_sofa = self.scale_image(self.imgs["modern_sofa"], 120, 90)

        return (factory, self.factory_pos,
                classic_chair, self.classic_chair_pos,
                classic_sofa, self.classic_sofa_pos,
                modern_chair, self.modern_chair_pos,
                modern_sofa, self.modern_sofa_pos)

    # ---------------- Frame Update ----------------

    def update_frame(self):
        if self.paused:
            return

        surface = self.create_surface()
        (factory_img, factory_pos,
         classic_chair_img, classic_chair_pos,
         classic_sofa_img, classic_sofa_pos,
         modern_chair_img, modern_chair_pos,
         modern_sofa_img, modern_sofa_pos) = self.scale_elements()

        # Draw factory
        surface.blit(factory_img, factory_pos)

        # Start point: bottom center of the factory
        factory_center = (factory_pos[0] + factory_img.get_width() // 2,
                          factory_pos[1] + factory_img.get_height())

        self.frame_count += 1
        progress = self.frame_count * 15  # arrow growth speed

        # Step 1: branching arrows to groups
        classic_group_center = (self.classic_group_pos[0] + 100, self.classic_group_pos[1] - 20)
        modern_group_center = (self.modern_group_pos[0] + 100, self.modern_group_pos[1] - 20)

        self.draw_growing_arrow(surface, factory_center, classic_group_center, progress)
        self.draw_growing_arrow(surface, factory_center, modern_group_center, progress)

        # Step 2: show furniture
        if self.frame_count > 20:
            surface.blit(classic_chair_img, classic_chair_pos)
            surface.blit(classic_sofa_img, classic_sofa_pos)
            surface.blit(modern_chair_img, modern_chair_pos)
            surface.blit(modern_sofa_img, modern_sofa_pos)

        # Step 3: group labels
        if self.frame_count > 40:
            labels = {
                "Creates Victorian Furniture": (classic_chair_pos[0], classic_chair_pos[1] + 120),
                "Creates Modern Furniture": (modern_sofa_pos[0], modern_sofa_pos[1] + 120),
            }
            self.draw_labels(surface, labels)

        # Loop reset
        if self.frame_count > 300:
            self.frame_count = 0
            self.reset_positions()

        # Finalize
        self.finalize_frame(surface)
