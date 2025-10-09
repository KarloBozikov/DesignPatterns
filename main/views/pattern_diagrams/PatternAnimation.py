import pygame
from PySide6.QtWidgets import QLabel, QGraphicsProxyWidget
from PySide6.QtCore import QTimer
from PySide6.QtGui import QImage, QPixmap

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
        """Resize QLabel to exactly match the DiagramView viewport without expanding the scene."""
        w, h = self.view.viewport().width(), self.view.viewport().height()
        if w <= 0 or h <= 0:
            return

        self.label.resize(w, h)
        self.proxy.setPos(0, 0)
        self.view.setSceneRect(0, 0, w, h)

        if hasattr(self, "reset_positions"):
            self.reset_positions()

    def create_surface(self):
        """Create a transparent surface sized to DiagramView."""
        w, h = self.view.width(), self.view.height()
        return pygame.Surface((w, h), pygame.SRCALPHA)

    @staticmethod
    def to_qimage(surface):
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

    def reset_positions(self):
        """Compute absolute pixel positions from relative config."""
        w, h = self.view.width(), self.view.height()
        sx, sy = self.scale_factor()

        self.positions = {}
        for name, (rx, ry) in self.config["positions"].items():
            self.positions[name] = (int(w * rx), int(h * ry))

    def scale_elements(self):
        """Scale icons according to config sizes."""
        scaled = {}
        for name, (w, h) in self.config["sizes"].items():
            scaled[name] = self.scale_image(self.imgs[name], w, h)
        return scaled

    # ---------------- Drawing helpers ----------------

    def draw_labels(self, surface, labels: dict, color=(255, 255, 255)):
        """Draw text labels above elements."""
        for text, pos in labels.items():
            surface.blit(self.font.render(text, True, color), pos)

    def draw_message(self, surface, text, color, anchor_rect, margin=20):
        """Draw a centered message below an element (like socket)."""
        msg = self.font.render(text, True, color)
        msg_pos = (
            anchor_rect[0] + anchor_rect[2] // 2 - msg.get_width() // 2,
            anchor_rect[1] + anchor_rect[3] + margin
        )
        surface.blit(msg, msg_pos)

    @staticmethod
    def draw_growing_arrow(surface, start, end, progress,
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

    @staticmethod
    def get_center(pos, surface, y_anchor="center"):
        x = pos[0] + surface.get_width() // 2

        if y_anchor == "center":
            y = pos[1] + surface.get_height() // 2
        elif y_anchor == "bottom":
            y = pos[1] + surface.get_height()
        elif y_anchor == "top":
            y = pos[1]
        else:
            raise ValueError(f"Unknown y_anchor: {y_anchor}")

        return x, y

    @staticmethod
    def get_anchor(pos, surface, anchor="center"):
        x, y = pos
        w, h = surface.get_width(), surface.get_height()

        if anchor == "center":
            x += w // 2
            y += h // 2
        elif anchor in ("midtop", "top"):
            x += w // 2
        elif anchor in ("midbottom", "bottom"):
            x += w // 2
            y += h
        elif anchor == "midleft":
            y += h // 2
        elif anchor == "midright":
            x += w
            y += h // 2
        else:
            raise ValueError(f"Unknown anchor: {anchor}")

        return x, y

    # ---------------- Animation helpers ----------------

    @staticmethod
    def move_linear(start_pos, frame, speed, max_frames, final_offset=(0, 0)):
        """Animate X movement for limited frames, else snap to the final offset."""
        if frame < max_frames:
            return start_pos[0] + int(frame * speed), start_pos[1]
        return start_pos[0] + final_offset[0], start_pos[1] + final_offset[1]

    def scale_image(self, image, width, height):
        """Scale an image based on view scaling factors."""
        sx, sy = self.scale_factor()
        return pygame.transform.scale(image, (int(width * sx), int(height * sy)))

    # in PatternAnimation
    @staticmethod
    def move_towards(current, target, step):
        """Move a numeric value (x or y) towards the target with a fixed step."""
        if current < target:
            return current + min(step, target - current)
        elif current > target:
            return current - min(step, current - target)
        return current

    # ---------------- To Override ----------------

    def update_frame(self):
        """Subclasses must override this to draw their animation frame."""
        raise NotImplementedError
