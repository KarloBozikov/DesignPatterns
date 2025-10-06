import pygame
from PySide6.QtWidgets import QLabel, QGraphicsProxyWidget
from PySide6.QtCore import QTimer
from PySide6.QtGui import QImage


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

        pygame.init()

    # ---------------- Helpers ----------------

    def resize_to_view(self):
        """Resize QLabel to exactly match DiagramView viewport without expanding scene."""
        w, h = self.view.viewport().width(), self.view.viewport().height()
        if w <= 0 or h <= 0:
            return

        # Resize the QLabel
        self.label.resize(w, h)

        # Position the proxy at (0, 0) in scene coordinates
        self.proxy.setPos(0, 0)

        # Force scene rect = viewport size (prevents scrollbars)
        self.view.setSceneRect(0, 0, w, h)

        # Let the subclass handle repositioning of its own elements
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

    def scale_factor(self):
        """Return scaling factors relative to design resolution."""
        w, h = self.view.width(), self.view.height()
        return w / self.DESIGN_WIDTH, h / self.DESIGN_HEIGHT

    # ---------------- To Override ----------------

    def update_frame(self):
        """Subclasses must override this to draw their animation frame."""
        pass
