import os
import pygame
from ..PatternAnimation import PatternAnimation

class FlyweightAnimation(PatternAnimation):
    """Flyweight pattern animation drawn directly into DiagramView."""

    def __init__(self, view: "DiagramView"):
        super().__init__(view)

        # Load resources
        current_dir = os.path.dirname(os.path.abspath(__file__))
        base_path = os.path.normpath(
            os.path.join(current_dir, "../../../../main/resources/diagrams/structural_patterns/flyweight/")
        )
        self.editor_img = pygame.image.load(os.path.join(base_path, "textEditor.png"))
        self.font_img = pygame.image.load(os.path.join(base_path, "font.png"))
        self.h_img = pygame.image.load(os.path.join(base_path, "letterH.png"))
        self.i_img = pygame.image.load(os.path.join(base_path, "letterI.png"))
        self.ex_img = pygame.image.load(os.path.join(base_path, "exclamation.png"))

        # Initialize
        self.reset_positions()
        self.frame_count = 0
        self.paused = False

    # ---------------- Helpers ----------------

    def reset_positions(self):
        w, h = self.view.width(), self.view.height()

        # Editor on top
        self.editor_pos = (int(w * 0.4), int(0.05 * h))

        # Shared font in the middle
        self.font_pos = (int(w * 0.45), int(0.4 * h))

        # Letters at bottom
        self.h_pos = (int(w * 0.3), int(0.75 * h))
        self.i_pos = (int(w * 0.5), int(0.75 * h))
        self.ex_pos = (int(w * 0.7), int(0.75 * h))

    def scale_elements(self):
        editor = self.scale_image(self.editor_img, 180, 120)
        font = self.scale_image(self.font_img, 120, 100)
        h = self.scale_image(self.h_img, 80, 100)
        i = self.scale_image(self.i_img, 80, 100)
        ex = self.scale_image(self.ex_img, 80, 100)
        return editor, font, h, i, ex

    # ---------------- Frame Update ----------------

    def update_frame(self):
        if self.paused:
            return

        surface = self.create_surface()
        editor, font_img, h, i, ex = self.scale_elements()

        # Draw base elements
        surface.blit(editor, self.editor_pos)
        surface.blit(font_img, self.font_pos)
        surface.blit(h, self.h_pos)
        surface.blit(i, self.i_pos)
        surface.blit(ex, self.ex_pos)

        # Centers
        editor_center = (self.editor_pos[0] + editor.get_width() // 2,
                         self.editor_pos[1] + editor.get_height())
        font_center_top = (self.font_pos[0] + font_img.get_width() // 2,
                           self.font_pos[1])
        font_center_bottom = (self.font_pos[0] + font_img.get_width() // 2,
                              self.font_pos[1] + font_img.get_height())
        h_center = (self.h_pos[0] + h.get_width() // 2, self.h_pos[1])
        i_center = (self.i_pos[0] + i.get_width() // 2, self.i_pos[1])
        ex_center = (self.ex_pos[0] + ex.get_width() // 2, self.ex_pos[1])

        # Animate arrows
        self.frame_count += 1
        arrow_growth_speed = 15

        # Editor → Font
        self.draw_growing_arrow(surface, editor_center, font_center_top,
                                self.frame_count * arrow_growth_speed,
                                color=(255, 255, 0))

        # Font → Letters
        if self.frame_count > 30:
            self.draw_growing_arrow(surface, font_center_bottom, h_center,
                                    (self.frame_count - 30) * arrow_growth_speed,
                                    color=(0, 255, 255))
        if self.frame_count > 60:
            self.draw_growing_arrow(surface, font_center_bottom, i_center,
                                    (self.frame_count - 60) * arrow_growth_speed,
                                    color=(0, 255, 255))
        if self.frame_count > 90:
            self.draw_growing_arrow(surface, font_center_bottom, ex_center,
                                    (self.frame_count - 90) * arrow_growth_speed,
                                    color=(0, 255, 255))

        # Labels (reuse base font)
        surface.blit(self.font.render("TextEditor", True, (255, 255, 0)),
                     (self.editor_pos[0], self.editor_pos[1] - 30))
        surface.blit(self.font.render("Font (shared)", True, (255, 255, 255)),
                     (self.font_pos[0], self.font_pos[1] - 30))
        surface.blit(self.font.render("Letter H", True, (255, 255, 255)),
                     (self.h_pos[0], self.h_pos[1] + h.get_height() + 5))
        surface.blit(self.font.render("Letter I", True, (255, 255, 255)),
                     (self.i_pos[0], self.i_pos[1] + i.get_height() + 5))
        surface.blit(self.font.render("Letter !", True, (255, 255, 255)),
                     (self.ex_pos[0], self.ex_pos[1] + ex.get_height() + 5))

        # Loop
        if self.frame_count > 200:
            self.frame_count = 0

        # Finalize
        self.finalize_frame(surface)
