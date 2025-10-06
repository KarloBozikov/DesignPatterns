import os
import pygame
from PySide6.QtCore import QTimer
from PySide6.QtGui import QPixmap
from ..PatternAnimation import PatternAnimation


class AbstractAnimation(PatternAnimation):
    """Abstract Factory animation drawn directly into DiagramView."""

    def __init__(self, view: "DiagramView"):
        super().__init__(view)

        # Load resources
        current_dir = os.path.dirname(os.path.abspath(__file__))
        base_path = os.path.normpath(
            os.path.join(current_dir, "../../../../main/resources/diagrams/creational_patterns/abstract_factory/")
        )
        self.factory_img = pygame.image.load(os.path.join(base_path, "factory.png"))
        self.classic_chair_img = pygame.image.load(os.path.join(base_path, "classic_chair.png"))
        self.classic_sofa_img = pygame.image.load(os.path.join(base_path, "classic_sofa.png"))
        self.modern_chair_img = pygame.image.load(os.path.join(base_path, "modern_chair.png"))
        self.modern_sofa_img = pygame.image.load(os.path.join(base_path, "modern_sofa.png"))

        # Initialize
        self.reset_positions()
        self.frame_count = 0
        self.paused = False

    def reset_positions(self):
        """Set positions for factory + grouped product families."""
        w, h = self.view.width(), self.view.height()
        sx, sy = self.scale_factor()

        # Main abstract factory
        self.factory_pos = (int(w * 0.5 - 90 * sx), int(40 * sy))

        # Classic family (left group)
        self.classic_group_pos = (int(w * 0.25 - 120 * sx), int(h * 0.45))
        self.classic_chair_pos = (self.classic_group_pos[0], self.classic_group_pos[1])
        self.classic_sofa_pos = (self.classic_group_pos[0] + int(120 * sx), self.classic_group_pos[1])

        # Modern family (right group)
        self.modern_group_pos = (int(w * 0.65 - 120 * sx), int(h * 0.45))
        self.modern_chair_pos = (self.modern_group_pos[0], self.modern_group_pos[1])
        self.modern_sofa_pos = (self.modern_group_pos[0] + int(120 * sx), self.modern_group_pos[1])

    def scale_elements(self):
        sx, sy = self.scale_factor()

        factory_img = pygame.transform.scale(self.factory_img, (int(180 * sx), int(120 * sy)))
        classic_chair_img = pygame.transform.scale(self.classic_chair_img, (int(90 * sx), int(90 * sy)))
        classic_sofa_img = pygame.transform.scale(self.classic_sofa_img, (int(120 * sx), int(90 * sy)))
        modern_chair_img = pygame.transform.scale(self.modern_chair_img, (int(90 * sx), int(90 * sy)))
        modern_sofa_img = pygame.transform.scale(self.modern_sofa_img, (int(120 * sx), int(90 * sy)))

        return (factory_img, self.factory_pos,
                classic_chair_img, self.classic_chair_pos,
                classic_sofa_img, self.classic_sofa_pos,
                modern_chair_img, self.modern_chair_pos,
                modern_sofa_img, self.modern_sofa_pos)

    def update_frame(self):
        if self.paused:
            return

        frame_surface = self.create_surface()
        (factory_img, factory_pos,
         classic_chair_img, classic_chair_pos,
         classic_sofa_img, classic_sofa_pos,
         modern_chair_img, modern_chair_pos,
         modern_sofa_img, modern_sofa_pos) = self.scale_elements()

        # Draw factory
        frame_surface.blit(factory_img, factory_pos)

        # Start point: bottom center of factory
        factory_center = (factory_pos[0] + factory_img.get_width() // 2,
                          factory_pos[1] + factory_img.get_height())

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

        # Step 1: two branching arrows (to group centers, not individual products)
        progress = self.frame_count * arrow_growth_speed
        classic_group_center = (self.classic_group_pos[0] + 100, self.classic_group_pos[1] - 20)
        modern_group_center = (self.modern_group_pos[0] + 100, self.modern_group_pos[1] - 20)

        draw_arrow(frame_surface, factory_center, classic_group_center, progress)
        draw_arrow(frame_surface, factory_center, modern_group_center, progress)

        # Step 2: show grouped products
        if self.frame_count > 20:
            frame_surface.blit(classic_chair_img, classic_chair_pos)
            frame_surface.blit(classic_sofa_img, classic_sofa_pos)
            frame_surface.blit(modern_chair_img, modern_chair_pos)
            frame_surface.blit(modern_sofa_img, modern_sofa_pos)

        # Step 3: labels under groups
        if self.frame_count > 40:
            font = pygame.font.SysFont("Arial", 22)
            labels = {
                "Creates Victorian Furniture": (classic_chair_pos[0], classic_chair_pos[1] + 120),
                "Creates Modern furniture": (modern_sofa_pos[0], modern_sofa_pos[1] + 120),
            }
            for text, pos in labels.items():
                label_surface = font.render(text, True, arrow_color)
                frame_surface.blit(label_surface, pos)

        # Loop
        if self.frame_count > 300:
            self.frame_count = 0
            self.reset_positions()

        qimg = self.to_qimage(frame_surface)
        self.label.setPixmap(QPixmap.fromImage(qimg))