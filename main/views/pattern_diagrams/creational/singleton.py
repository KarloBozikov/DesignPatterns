import os
import pygame
from PySide6.QtCore import QTimer
from PySide6.QtGui import QPixmap
from ..PatternAnimation import PatternAnimation


class SingletonAnimation(PatternAnimation):
    """Singleton animation drawn directly into DiagramView."""

    def __init__(self, view: "DiagramView"):
        super().__init__(view)

        # Load resources
        current_dir = os.path.dirname(os.path.abspath(__file__))
        base_path = os.path.normpath(
            os.path.join(current_dir, "../../../../main/resources/diagrams/creational_patterns/singleton/")
        )
        self.printer_img_orig = pygame.image.load(os.path.join(base_path, "printer.png"))
        self.man_img_orig = pygame.image.load(os.path.join(base_path, "man.png"))
        self.woman_img_orig = pygame.image.load(os.path.join(base_path, "woman.png"))
        self.document_img_orig = pygame.image.load(os.path.join(base_path, "document.png"))

        # Initialize positions
        self.reset_positions()
        self.speed = 5
        self.paused = False

    # ---------------- Helpers ----------------

    def reset_positions(self):
        w, h = self.view.width(), self.view.height()
        sx, sy = self.scale_factor()

        self.printer_pos = (int(w * 0.5 - 75 * sx), int(50 * sy))
        self.man_pos = (int(150 * sx), int(h - 250 * sy))
        self.woman_pos = (int(w - 270 * sx), int(h - 250 * sy))
        self.doc1_pos_orig = [self.man_pos[0] + int(80 * sx), self.man_pos[1] + int(40 * sy)]
        self.doc2_pos_orig = [self.woman_pos[0] + int(50 * sx), self.woman_pos[1] + int(40 * sy)]

        self.doc1_pos = list(self.doc1_pos_orig)
        self.doc2_pos = list(self.doc2_pos_orig)

    def move_towards(self, current, target, step):
        if current < target:
            return current + min(step, target - current)
        elif current > target:
            return current - min(step, current - target)
        return current

    def scale_elements(self):
        sx, sy = self.scale_factor()

        man_img = pygame.transform.scale(self.man_img_orig, (int(150 * sx), int(200 * sy)))
        woman_img = pygame.transform.scale(self.woman_img_orig, (int(120 * sx), int(150 * sy)))
        printer_img = pygame.transform.scale(self.printer_img_orig, (int(150 * sx), int(150 * sy)))
        document_img = pygame.transform.scale(self.document_img_orig, (int(60 * sx), int(80 * sy)))

        return man_img, self.man_pos, woman_img, self.woman_pos, printer_img, self.printer_pos, document_img

    # ---------------- Frame Update ----------------

    def update_frame(self):
        if self.paused:
            return

        w, h = self.view.width(), self.view.height()
        frame_surface = self.create_surface()

        man_img, man_pos, woman_img, woman_pos, printer_img, printer_pos, document_img = self.scale_elements()
        frame_surface.blit(man_img, man_pos)
        frame_surface.blit(woman_img, woman_pos)
        frame_surface.blit(printer_img, printer_pos)

        # Move docs
        self.doc1_pos[0] = self.move_towards(self.doc1_pos[0], printer_pos[0] + 60, self.speed)
        self.doc1_pos[1] = self.move_towards(self.doc1_pos[1], printer_pos[1] + 40, self.speed)
        self.doc2_pos[0] = self.move_towards(self.doc2_pos[0], printer_pos[0] + 60, self.speed)
        self.doc2_pos[1] = self.move_towards(self.doc2_pos[1], printer_pos[1] + 40, self.speed)

        # Draw docs
        frame_surface.blit(document_img, self.doc1_pos)
        frame_surface.blit(document_img, self.doc2_pos)

        # Reset loop if both docs reach printer
        if (self.doc1_pos[0] == printer_pos[0] + 60 and self.doc1_pos[1] == printer_pos[1] + 40 and
                self.doc2_pos[0] == printer_pos[0] + 60 and self.doc2_pos[1] == printer_pos[1] + 40):
            self.paused = True
            self.timer.stop()
            QTimer.singleShot(2000, self.resume)

        # Convert → QImage → QLabel
        qimg = self.to_qimage(frame_surface)
        self.label.setPixmap(QPixmap.fromImage(qimg))

    def resume(self):
        self.reset_positions()
        self.paused = False
        self.timer.start(1000 // 60)
