import os
import pygame
from ..PatternAnimation import PatternAnimation

class ProxyAnimation(PatternAnimation):
    """Proxy pattern animation drawn directly into the DiagramView."""

    def __init__(self, view: "DiagramView"):
        super().__init__(view)

        # Load resources
        current_dir = os.path.dirname(os.path.abspath(__file__))
        base_path = os.path.normpath(
            os.path.join(current_dir, "../../../../main/resources/diagrams/structural_patterns/proxy/")
        )
        self.scientist_img = pygame.image.load(os.path.join(base_path, "dataScientist.png"))
        self.password_img = pygame.image.load(os.path.join(base_path, "password.png"))
        self.data_img = pygame.image.load(os.path.join(base_path, "data.png"))

        # Initialize
        self.reset_positions()
        self.frame_count = 0
        self.phase = 0   # 0 = no access, 1 = access granted
        self.paused = False

    # ---------------- Helpers ----------------

    def reset_positions(self):
        w, h = self.view.width(), self.view.height()

        # Place icons
        self.scientist_pos = (int(w * 0.05), int(h * 0.4))
        self.password_pos = (int(w * 0.4), int(h * 0.35))
        self.data_pos = (int(w * 0.75), int(h * 0.35))

    def scale_elements(self):
        scientist = self.scale_image(self.scientist_img, 120, 140)
        password = self.scale_image(self.password_img, 120, 120)
        data = self.scale_image(self.data_img, 140, 120)
        return scientist, password, data

    # ---------------- Frame Update ----------------

    def update_frame(self):
        if self.paused:
            return

        surface = self.create_surface()
        scientist, password, data = self.scale_elements()

        # Draw icons
        surface.blit(scientist, self.scientist_pos)
        surface.blit(password, self.password_pos)
        surface.blit(data, self.data_pos)

        # Centers
        scientist_center = (self.scientist_pos[0] + scientist.get_width(),
                            self.scientist_pos[1] + scientist.get_height() // 2)
        password_center_left = (self.password_pos[0],
                                self.password_pos[1] + password.get_height() // 2)
        password_center_right = (self.password_pos[0] + password.get_width(),
                                 self.password_pos[1] + password.get_height() // 2)
        data_center = (self.data_pos[0],
                       self.data_pos[1] + data.get_height() // 2)

        # Animate
        self.frame_count += 1
        arrow_speed = 15

        if self.phase == 0:  # Access denied
            # Scientist → Password
            self.draw_growing_arrow(surface, scientist_center, password_center_left,
                                    self.frame_count * arrow_speed, color=(255, 0, 0))

            if self.frame_count > 80:
                self.draw_message(surface, "Access Denied", (255, 0, 0),
                                  (*self.password_pos, password.get_width(), password.get_height()))

        else:  # Access granted
            # Scientist → Password
            self.draw_growing_arrow(surface, scientist_center, password_center_left,
                                    self.frame_count * arrow_speed, color=(0, 255, 0))

            # Password → Data
            if self.frame_count > 40:
                self.draw_growing_arrow(surface, password_center_right, data_center,
                                        (self.frame_count - 40) * arrow_speed, color=(0, 255, 0))

            if self.frame_count > 100:
                self.draw_message(surface, "Access Granted", (0, 255, 0),
                                  (*self.data_pos, data.get_width(), data.get_height()))

        # Loop: switch phase
        if self.frame_count > 200:
            self.frame_count = 0
            self.phase = 1 - self.phase

        # Finalize
        self.finalize_frame(surface)
