import os
import pygame
from ..PatternAnimation import PatternAnimation

class StateAnimation(PatternAnimation):
    """State pattern animation: Traffic light cycling between Red, Yellow, Green."""

    def __init__(self, view: "DiagramView"):
        super().__init__(view)

        # Load resources
        current_dir = os.path.dirname(os.path.abspath(__file__))
        base_path = os.path.normpath(
            os.path.join(
                current_dir,
                "../../../../main/resources/diagrams/behavioral_patterns/state/"
            )
        )
        self.red_light_img = pygame.image.load(os.path.join(base_path, "red_light.png"))
        self.yellow_light_img = pygame.image.load(os.path.join(base_path, "yellow_light.png"))
        self.green_light_img = pygame.image.load(os.path.join(base_path, "green_light.png"))

        # Initialize
        self.reset_positions()
        self.frame_count = 0
        self.paused = False
        self.current_state = "red"

        # State duration in frames (60fps → 2s each)
        self.state_duration = 120

    # ---------------- Helpers ----------------

    def reset_positions(self):
        """Center the traffic light images in the view."""
        w, h = self.view.width(), self.view.height()
        sx, sy = self.scale_factor()
        self.center_pos = (int(w * 0.5 - 60 * sx), int(h * 0.3))

    def scale_elements(self):
        """Scale light images dynamically according to view size."""
        w, h = self.view.width(), self.view.height()
        size = int(min(w * 0.25, h * 0.25))

        red = pygame.transform.scale(self.red_light_img, (size, size))
        yellow = pygame.transform.scale(self.yellow_light_img, (size, size))
        green = pygame.transform.scale(self.green_light_img, (size, size))
        return red, yellow, green

    # ---------------- Frame Update ----------------

    def update_frame(self):
        if self.paused:
            return

        surface = self.create_surface()
        red_img, yellow_img, green_img = self.scale_elements()

        # Frame timing
        self.frame_count += 1
        if self.frame_count >= self.state_duration:
            self.frame_count = 0
            if self.current_state == "red":
                self.current_state = "yellow"
            elif self.current_state == "yellow":
                self.current_state = "green"
            else:
                self.current_state = "red"

        # Select the correct image and label
        if self.current_state == "red":
            active_img = red_img
            label_text = "Red → Stop"
        elif self.current_state == "yellow":
            active_img = yellow_img
            label_text = "Yellow → Caution"
        else:
            active_img = green_img
            label_text = "Green → Go"

        # Draw the active light
        surface.blit(active_img, self.center_pos)

        # Label below the light
        label = self.font.render(label_text, True, (255, 255, 255))
        icon_width, icon_height = active_img.get_size()
        label_x = self.center_pos[0] + icon_width // 2 - label.get_width() // 2
        label_y = self.center_pos[1] + icon_height + 10
        surface.blit(label, (label_x, label_y))

        # Finalize
        self.finalize_frame(surface)
