import os
import pygame
from PySide6.QtCore import QTimer
from ..PatternAnimation import PatternAnimation


class SingletonAnimation(PatternAnimation):
    """Singleton pattern animation: two people send docs to the same printer."""

    def __init__(self, view: "DiagramView"):
        super().__init__(view)

        # Load resources
        current_dir = os.path.dirname(os.path.abspath(__file__))
        base_path = os.path.normpath(
            os.path.join(current_dir, "../../../../main/resources/diagrams/creational_patterns/singleton/")
        )

        self.imgs = {
            "printer": pygame.image.load(os.path.join(base_path, "printer.png")),
            "man": pygame.image.load(os.path.join(base_path, "man.png")),
            "woman": pygame.image.load(os.path.join(base_path, "woman.png")),
            "document": pygame.image.load(os.path.join(base_path, "document.png")),
        }

        # Movement speed
        self.speed = 5

        # Initialize positions
        self.reset_positions()

    # ---------------- Helpers ----------------

    def reset_positions(self):
        w, h = self.view.width(), self.view.height()
        sx, sy = self.scale_factor()

        self.printer_pos = (int(w * 0.5 - 75 * sx), int(50 * sy))
        self.man_pos = (int(150 * sx), int(h - 250 * sy))
        self.woman_pos = (int(w - 270 * sx), int(h - 250 * sy))

        self.doc1_pos = [self.man_pos[0] + int(80 * sx), self.man_pos[1] + int(40 * sy)]
        self.doc2_pos = [self.woman_pos[0] + int(50 * sx), self.woman_pos[1] + int(40 * sy)]

    def scale_elements(self):
        """Return scaled images and positions."""
        man_img = self.scale_image(self.imgs["man"], 150, 200)
        woman_img = self.scale_image(self.imgs["woman"], 120, 150)
        printer_img = self.scale_image(self.imgs["printer"], 150, 150)
        doc_img = self.scale_image(self.imgs["document"], 60, 80)
        return man_img, woman_img, printer_img, doc_img

    # ---------------- Frame Update ----------------

    def update_frame(self):
        if self.paused:
            return

        surface = self.create_surface()
        man_img, woman_img, printer_img, doc_img = self.scale_elements()

        # Draw people + printer
        surface.blit(man_img, self.man_pos)
        surface.blit(woman_img, self.woman_pos)
        surface.blit(printer_img, self.printer_pos)

        # Dynamic target (center of printer)
        target = (
            self.printer_pos[0] + printer_img.get_width() // 2 - doc_img.get_width() // 2,
            self.printer_pos[1] + printer_img.get_height() // 2 - doc_img.get_height() // 2,
        )

        # Move docs
        self.doc1_pos[0] = self.move_towards(self.doc1_pos[0], target[0], self.speed)
        self.doc1_pos[1] = self.move_towards(self.doc1_pos[1], target[1], self.speed)
        self.doc2_pos[0] = self.move_towards(self.doc2_pos[0], target[0], self.speed)
        self.doc2_pos[1] = self.move_towards(self.doc2_pos[1], target[1], self.speed)

        # Draw docs
        surface.blit(doc_img, self.doc1_pos)
        surface.blit(doc_img, self.doc2_pos)

        # Arrival check
        if (abs(self.doc1_pos[0] - target[0]) <= 2 and abs(self.doc1_pos[1] - target[1]) <= 2 and
                abs(self.doc2_pos[0] - target[0]) <= 2 and abs(self.doc2_pos[1] - target[1]) <= 2):
            # Pause animation and show a message
            self.paused = True
            self.timer.stop()
            self.draw_message(
                surface,
                "Both docs sent to the same printer (Singleton)",
                (0, 255, 0),
                (self.printer_pos[0], self.printer_pos[1], printer_img.get_width(), printer_img.get_height())
            )
            QTimer.singleShot(2000, self.resume)

        # Finalize frame
        self.finalize_frame(surface)

    def resume(self):
        """Restart animation after a pause."""
        self.reset_positions()
        self.paused = False
        self.timer.start(1000 // 60)
