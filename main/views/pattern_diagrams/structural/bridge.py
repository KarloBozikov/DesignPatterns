import os
import pygame
from ..PatternAnimation import PatternAnimation

class BridgeAnimation(PatternAnimation):
    """Bridge pattern animation: decouple Shape from Color."""

    def __init__(self, view: "DiagramView"):
        super().__init__(view)

        # Load resources
        current_dir = os.path.dirname(os.path.abspath(__file__))
        base_path = os.path.normpath(
            os.path.join(current_dir, "../../../../main/resources/diagrams/structural_patterns/bridge/")
        )
        self.circle_img = pygame.image.load(os.path.join(base_path, "circle.png"))
        self.square_img = pygame.image.load(os.path.join(base_path, "square.png"))
        self.blue_paint_img = pygame.image.load(os.path.join(base_path, "blue_paint.png"))
        self.red_paint_img = pygame.image.load(os.path.join(base_path, "red_paint.png"))

        # Init state
        self.reset_positions()
        self.frame_count = 0
        self.phase = 0
        self.paused = False

    # ---------------- Helpers ----------------

    def reset_positions(self):
        """Reset positions of shapes and paints based on the current view size."""
        w, h = self.view.width(), self.view.height()

        # Shapes at the top
        self.circle_pos = (int(w * 0.25), int(h * 0.2))
        self.square_pos = (int(w * 0.65), int(h * 0.2))

        # Paints at bottom
        self.blue_pos = (int(w * 0.25), int(h * 0.65))
        self.red_pos = (int(w * 0.65), int(h * 0.65))

    def scale_elements(self):
        """Scale images relative to view size."""
        circle = self.scale_image(self.circle_img, 150, 150)
        square = self.scale_image(self.square_img, 150, 150)
        blue = self.scale_image(self.blue_paint_img, 80, 120)
        red = self.scale_image(self.red_paint_img, 80, 120)
        return circle, square, blue, red

    # ---------------- Frame Update ----------------

    def update_frame(self):
        if self.paused:
            return

        surface = self.create_surface()
        circle, square, blue, red = self.scale_elements()

        # Draw shapes
        surface.blit(circle, self.circle_pos)
        surface.blit(square, self.square_pos)

        # Draw paints
        surface.blit(blue, self.blue_pos)
        surface.blit(red, self.red_pos)

        # Centers for arrow connections
        circle_center = (self.circle_pos[0] + circle.get_width() // 2,
                         self.circle_pos[1] + circle.get_height() // 2)
        square_center = (self.square_pos[0] + square.get_width() // 2,
                         self.square_pos[1] + square.get_height() // 2)
        blue_center = (self.blue_pos[0] + blue.get_width() // 2,
                       self.blue_pos[1] + blue.get_height() // 2)
        red_center = (self.red_pos[0] + red.get_width() // 2,
                      self.red_pos[1] + red.get_height() // 2)

        # Animate arrows
        self.frame_count += 1
        progress = self.frame_count * 15

        if self.phase == 0:
            self.draw_growing_arrow(surface, blue_center, circle_center, progress, (0, 150, 255))
            self.draw_growing_arrow(surface, red_center, square_center, progress, (255, 0, 0))
        else:
            self.draw_growing_arrow(surface, blue_center, square_center, progress, (0, 150, 255))
            self.draw_growing_arrow(surface, red_center, circle_center, progress, (255, 0, 0))

        # Labels
        if self.phase == 0:
            labels = {
                "Circle.paint(Blue)": (self.circle_pos[0], self.circle_pos[1] + circle.get_height() + 10),
                "Square.paint(Red)": (self.square_pos[0], self.square_pos[1] + square.get_height() + 10),
            }
        else:
            labels = {
                "Circle.paint(Red)": (self.circle_pos[0], self.circle_pos[1] + circle.get_height() + 10),
                "Square.paint(Blue)": (self.square_pos[0], self.square_pos[1] + square.get_height() + 10),
            }
        self.draw_labels(surface, labels)

        # Loop every ~6s
        if self.frame_count > 200:
            self.frame_count = 0
            self.phase = 1 - self.phase

        # Finalize
        self.finalize_frame(surface)
