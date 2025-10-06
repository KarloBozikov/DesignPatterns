import os
import pygame
from PySide6.QtCore import QTimer
from PySide6.QtGui import QPixmap
from ..PatternAnimation import PatternAnimation


class BuilderAnimation(PatternAnimation):
    """Builder pattern animation drawn directly into DiagramView."""

    def __init__(self, view: "DiagramView"):
        super().__init__(view)

        # Load resources
        current_dir = os.path.dirname(os.path.abspath(__file__))
        base_path = os.path.normpath(
            os.path.join(current_dir, "../../../../main/resources/diagrams/creational_patterns/builder/")
        )
        self.architect_img = pygame.image.load(os.path.join(base_path, "architect.png"))
        self.house_img = pygame.image.load(os.path.join(base_path, "house.png"))
        self.classic_house_img = pygame.image.load(os.path.join(base_path, "classic_house.png"))
        self.modern_house_img = pygame.image.load(os.path.join(base_path, "modern_house.png"))

        # Initialize
        self.reset_positions()
        self.frame_count = 0
        self.paused = False

    # ---------------- Helpers ----------------

    def reset_positions(self):
        """Set positions for architect, construction, and houses."""
        w, h = self.view.width(), self.view.height()
        sx, sy = self.scale_factor()

        # Architect (Director) top center
        self.architect_pos = (int(w * 0.5 - 60 * sx), int(40 * sy))

        # Generic house under construction in the middle
        self.house_pos = (int(w * 0.5 - 80 * sx), int(h * 0.4))

        # Two final houses below
        self.classic_house_pos = (int(w * 0.3 - 100 * sx), int(h * 0.7))
        self.modern_house_pos = (int(w * 0.7 - 100 * sx), int(h * 0.7))

    def scale_elements(self):
        sx, sy = self.scale_factor()

        architect_img = pygame.transform.scale(self.architect_img, (int(120 * sx), int(120 * sy)))
        house_img = pygame.transform.scale(self.house_img, (int(160 * sx), int(140 * sy)))
        classic_house_img = pygame.transform.scale(self.classic_house_img, (int(180 * sx), int(140 * sy)))
        modern_house_img = pygame.transform.scale(self.modern_house_img, (int(180 * sx), int(140 * sy)))

        return (architect_img, self.architect_pos,
                house_img, self.house_pos,
                classic_house_img, self.classic_house_pos,
                modern_house_img, self.modern_house_pos)

    # ---------------- Frame Update ----------------

    def update_frame(self):
        if self.paused:
            return

        frame_surface = self.create_surface()
        (architect_img, architect_pos,
         house_img, house_pos,
         classic_house_img, classic_house_pos,
         modern_house_img, modern_house_pos) = self.scale_elements()

        # Draw architect
        frame_surface.blit(architect_img, architect_pos)

        # Animation counter
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

        # Start point: bottom center of architect
        architect_center = (architect_pos[0] + architect_img.get_width() // 2,
                            architect_pos[1] + architect_img.get_height())

        # Step 1: arrow Architect -> Generic house
        progress = self.frame_count * arrow_growth_speed
        house_target = (house_pos[0] + house_img.get_width() // 2, house_pos[1])
        draw_arrow(frame_surface, architect_center, house_target, progress)

        # Step 2: show generic house
        if self.frame_count > 20:
            frame_surface.blit(house_img, house_pos)

        # Step 3: arrows to Classic & Modern houses
        if self.frame_count > 40:
            house_center = (house_pos[0] + house_img.get_width() // 2,
                            house_pos[1] + house_img.get_height())
            classic_target = (classic_house_pos[0] + classic_house_img.get_width() // 2, classic_house_pos[1])
            modern_target = (modern_house_pos[0] + modern_house_img.get_width() // 2, modern_house_pos[1])

            progress2 = (self.frame_count - 40) * arrow_growth_speed
            draw_arrow(frame_surface, house_center, classic_target, progress2)
            draw_arrow(frame_surface, house_center, modern_target, progress2)

        # Step 4: show final houses
        if self.frame_count > 60:
            frame_surface.blit(classic_house_img, classic_house_pos)
            frame_surface.blit(modern_house_img, modern_house_pos)

        # Step 5: labels
        if self.frame_count > 80:
            font = pygame.font.SysFont("Arial", 24, bold=True)
            # Architect label
            lbl = font.render("Director (Architect)", True, arrow_color)
            frame_surface.blit(lbl, (architect_pos[0] + architect_img.get_width()//2 - lbl.get_width()//2,
                                     architect_pos[1] - 30))
            # House under construction
            lbl2 = font.render("Builder constructs House", True, arrow_color)
            frame_surface.blit(lbl2, (house_pos[0] + house_img.get_width()//2 - lbl2.get_width()//2,
                                      house_pos[1] - 30))
            # Classic house
            lbl3 = font.render("Classic House", True, arrow_color)
            frame_surface.blit(lbl3, (classic_house_pos[0] + classic_house_img.get_width()//2 - lbl3.get_width()//2,
                                      classic_house_pos[1] + classic_house_img.get_height() + 5))
            # Modern house
            lbl4 = font.render("Modern House", True, arrow_color)
            frame_surface.blit(lbl4, (modern_house_pos[0] + modern_house_img.get_width()//2 - lbl4.get_width()//2,
                                      modern_house_pos[1] + modern_house_img.get_height() + 5))

        # Loop after ~8 sec
        if self.frame_count > 480:
            self.frame_count = 0
            self.reset_positions()

        # Convert → QImage → QLabel
        qimg = self.to_qimage(frame_surface)
        self.label.setPixmap(QPixmap.fromImage(qimg))
