import os
import pygame
from ..PatternAnimation import PatternAnimation

class BuilderAnimation(PatternAnimation):
    """Builder pattern animation drawn directly into the DiagramView."""

    def __init__(self, view: "DiagramView"):
        super().__init__(view)

        # Load resources
        current_dir = os.path.dirname(os.path.abspath(__file__))
        base_path = os.path.normpath(
            os.path.join(current_dir, "../../../../main/resources/diagrams/creational_patterns/builder/")
        )
        self.imgs = {
            "architect": pygame.image.load(os.path.join(base_path, "architect.png")),
            "house": pygame.image.load(os.path.join(base_path, "house.png")),
            "classic": pygame.image.load(os.path.join(base_path, "classic_house.png")),
            "modern": pygame.image.load(os.path.join(base_path, "modern_house.png")),
        }

        # Initialize
        self.reset_positions()
        self.frame_count = 0
        self.paused = False

    # ---------------- Helpers ----------------

    def reset_positions(self):
        """Set positions for architect, generic house, and final houses."""
        w, h = self.view.width(), self.view.height()
        sx, sy = self.scale_factor()

        self.architect_pos = (int(w * 0.5 - 60 * sx), int(40 * sy))
        self.house_pos = (int(w * 0.5 - 80 * sx), int(h * 0.4))
        self.classic_house_pos = (int(w * 0.3 - 100 * sx), int(h * 0.7))
        self.modern_house_pos = (int(w * 0.7 - 100 * sx), int(h * 0.7))

    def scale_elements(self):
        """Return scaled images for all elements."""
        architect = self.scale_image(self.imgs["architect"], 120, 120)
        house = self.scale_image(self.imgs["house"], 160, 140)
        classic = self.scale_image(self.imgs["classic"], 180, 140)
        modern = self.scale_image(self.imgs["modern"], 180, 140)
        return architect, house, classic, modern

    # ---------------- Frame Update ----------------

    def update_frame(self):
        if self.paused:
            return

        surface = self.create_surface()
        architect_img, house_img, classic_img, modern_img = self.scale_elements()

        # Draw architect
        surface.blit(architect_img, self.architect_pos)

        # Frame counter
        self.frame_count += 1
        progress = self.frame_count * 15  # arrow growth speed
        arrow_color = (255, 255, 255)

        # Step 1: Architect -> Generic House
        architect_center = (
            self.architect_pos[0] + architect_img.get_width() // 2,
            self.architect_pos[1] + architect_img.get_height()
        )
        house_target = (self.house_pos[0] + house_img.get_width() // 2, self.house_pos[1])
        self.draw_growing_arrow(surface, architect_center, house_target, progress, arrow_color)

        # Step 2: Show a generic house
        if self.frame_count > 20:
            surface.blit(house_img, self.house_pos)

        # Step 3: Generic house -> Classic + Modern
        if self.frame_count > 40:
            house_center = (
                self.house_pos[0] + house_img.get_width() // 2,
                self.house_pos[1] + house_img.get_height()
            )
            classic_target = (self.classic_house_pos[0] + classic_img.get_width() // 2, self.classic_house_pos[1])
            modern_target = (self.modern_house_pos[0] + modern_img.get_width() // 2, self.modern_house_pos[1])
            progress2 = (self.frame_count - 40) * 15
            self.draw_growing_arrow(surface, house_center, classic_target, progress2, arrow_color)
            self.draw_growing_arrow(surface, house_center, modern_target, progress2, arrow_color)

        # Step 4: Show final houses
        if self.frame_count > 60:
            surface.blit(classic_img, self.classic_house_pos)
            surface.blit(modern_img, self.modern_house_pos)

        # Step 5: Labels
        if self.frame_count > 80:
            labels = {
                "Director (Architect)": (
                    self.architect_pos[0] + architect_img.get_width() // 2,
                    self.architect_pos[1] - 30
                ),
                "Builder constructs House": (
                    self.house_pos[0] + house_img.get_width() // 2,
                    self.house_pos[1] - 30
                ),
                "Classic House": (
                    self.classic_house_pos[0] + classic_img.get_width() // 2,
                    self.classic_house_pos[1] + classic_img.get_height() + 5
                ),
                "Modern House": (
                    self.modern_house_pos[0] + modern_img.get_width() // 2,
                    self.modern_house_pos[1] + modern_img.get_height() + 5
                ),
            }
            # Center-align labels
            for text, (cx, cy) in labels.items():
                lbl = self.font.render(text, True, arrow_color)
                surface.blit(lbl, (cx - lbl.get_width() // 2, cy))

        # Loop
        if self.frame_count > 480:
            self.frame_count = 0
            self.reset_positions()

        # Finalize frame
        self.finalize_frame(surface)
