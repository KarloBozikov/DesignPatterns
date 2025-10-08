import pygame
from PySide6.QtWidgets import QLabel, QGraphicsProxyWidget
from PySide6.QtCore import QTimer
from PySide6.QtGui import QImage, QPixmap, QColor, QFont


class PatternAnimation:
    """Base class for pattern animations rendered inside DiagramView."""

    DESIGN_WIDTH = 1280
    DESIGN_HEIGHT = 720

    def __init__(self, view: "DiagramView", fps: int = 60):
        self.view = view

        # QLabel inside DiagramView scene
        self.label = QLabel()
        self.label.setScaledContents(True)
        self.proxy: QGraphicsProxyWidget = self.view.scene.addWidget(self.label)

        # Timer for frame updates
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(1000 // fps)

        # Frame tracking
        self.frame_count = 0
        self.phase = 0
        self.paused = False

        # Fonts
        pygame.init()
        self.font = pygame.font.SysFont("Arial", 24, bold=True)

    # ---------------- Layout & scaling ----------------

    def resize_to_view(self):
        """Resize QLabel to exactly match DiagramView viewport without expanding scene."""
        w, h = self.view.viewport().width(), self.view.viewport().height()
        if w <= 0 or h <= 0:
            return

        self.label.resize(w, h)
        self.proxy.setPos(0, 0)
        self.view.setSceneRect(0, 0, w, h)

        if hasattr(self, "reset_positions"):
            self.reset_positions()

    def create_surface(self):
        """Create transparent surface sized to DiagramView."""
        w, h = self.view.width(), self.view.height()
        return pygame.Surface((w, h), pygame.SRCALPHA)

    def to_qimage(self, surface):
        """Convert Pygame surface to QImage."""
        w, h = surface.get_size()
        data = pygame.image.tostring(surface, "RGBA")
        return QImage(data, w, h, QImage.Format_RGBA8888)

    def finalize_frame(self, surface):
        """Render pygame surface into QLabel (end of each update_frame)."""
        qimg = self.to_qimage(surface)
        self.label.setPixmap(QPixmap.fromImage(qimg))

    def scale_factor(self):
        """Return scaling factors relative to design resolution."""
        w, h = self.view.width(), self.view.height()
        return w / self.DESIGN_WIDTH, h / self.DESIGN_HEIGHT

    # ---------------- Drawing helpers ----------------

    def draw_labels(self, surface, labels: dict, color=(255, 255, 255)):
        """Draw text labels above elements."""
        for text, pos in labels.items():
            surface.blit(self.font.render(text, True, color), pos)

    def draw_message(self, surface, text, color, anchor_rect, margin=20):
        """Draw centered message below an element (like socket)."""
        msg = self.font.render(text, True, color)
        msg_pos = (
            anchor_rect[0] + anchor_rect[2] // 2 - msg.get_width() // 2,
            anchor_rect[1] + anchor_rect[3] + margin
        )
        surface.blit(msg, msg_pos)

    def draw_growing_arrow(self, surface, start, end, progress,
                           color=(255, 255, 255), thickness=6, arrow_size=12):
        """Draw animated arrow from start to end with progress-based growth."""
        dx, dy = end[0] - start[0], end[1] - start[1]
        length = max(1, (dx ** 2 + dy ** 2) ** 0.5)
        ux, uy = dx / length, dy / length
        current_len = min(progress, length)
        mid = (start[0] + ux * current_len, start[1] + uy * current_len)

        # Line grows with progress
        pygame.draw.line(surface, color, start, mid, thickness)

        # Arrow head appears when full length reached
        if progress >= length:
            perp = (-uy, ux)
            p1 = (end[0] - ux * arrow_size + perp[0] * arrow_size / 2,
                  end[1] - uy * arrow_size + perp[1] * arrow_size / 2)
            p2 = (end[0] - ux * arrow_size - perp[0] * arrow_size / 2,
                  end[1] - uy * arrow_size - perp[1] * arrow_size / 2)
            pygame.draw.polygon(surface, color, [end, p1, p2])


    # ---------------- Animation helpers ----------------

    def move_linear(self, start_pos, frame, speed, max_frames, final_offset=(0, 0)):
        """Animate X movement for limited frames, else snap to final offset."""
        if frame < max_frames:
            return (start_pos[0] + int(frame * speed), start_pos[1])
        return (start_pos[0] + final_offset[0], start_pos[1] + final_offset[1])

    def scale_image(self, image, width, height):
        """Scale an image based on view scaling factors."""
        sx, sy = self.scale_factor()
        return pygame.transform.scale(image, (int(width * sx), int(height * sy)))

    # in PatternAnimation
    def move_towards(self, current, target, step):
        """Move a numeric value (x or y) towards target with fixed step."""
        if current < target:
            return current + min(step, target - current)
        elif current > target:
            return current - min(step, current - target)
        return current

    # ---------------- To Override ----------------

    def update_frame(self):
        """Subclasses must override this to draw their animation frame."""
        raise NotImplementedError
