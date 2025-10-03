from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QLabel
from PySide6.QtGui import QPixmap, QMovie
from PySide6.QtCore import Qt, QTimer
import os

from .pattern_diagrams.creational.singleton import SingletonAnimation

class DiagramView(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.setAlignment(Qt.AlignCenter)

        self.diagram_path = os.path.join(os.path.dirname(__file__), "..", "resources", "diagram")
        self.singleton_anim = None

    def draw_pattern_from_data(self, pattern_data):
        """Load diagram image or animation based on pattern name"""
        # Clear previous
        self.scene.clear()
        if self.singleton_anim:
            self.singleton_anim.timer.stop()
            self.singleton_anim = None

        pattern_name = (pattern_data.get("name") or
                        pattern_data.get("pattern_name") or
                        "Unknown").lower()

        match pattern_name:
            case "singleton":
                self.singleton_anim = SingletonAnimation(self)
                QTimer.singleShot(0, self.singleton_anim.resize_to_view)

            case _:
                self.scene.addText(f"Diagram for {pattern_name} not found.")

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if hasattr(self, "singleton_anim") and self.singleton_anim:
            self.singleton_anim.resize_to_view()
        else:
            # Prevent scrollbars for static diagrams too
            self.setSceneRect(0, 0, self.viewport().width(), self.viewport().height())

