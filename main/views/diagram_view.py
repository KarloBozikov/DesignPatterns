from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QLabel
from PySide6.QtGui import QPixmap, QMovie
from PySide6.QtCore import Qt, QTimer
import os

from .pattern_diagrams.creational.singleton import SingletonAnimation
from .pattern_diagrams.creational.factoryMethod import FactoryAnimation
from .pattern_diagrams.creational.abstractFactory import AbstractAnimation
from .pattern_diagrams.creational.prototype import PrototypeAnimation
from .pattern_diagrams.creational.builder import BuilderAnimation

from .pattern_diagrams.behavioral.state import StateAnimation

class DiagramView(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.setAlignment(Qt.AlignCenter)

        self.diagram_path = os.path.join(os.path.dirname(__file__), "..", "resources", "diagram")
        self.singleton_anim = None
        self.factory_anim = None
        self.factory_animation = None
        self.prototype_anim = None
        self.builder_anim = None

        self.state_anim = None

    def draw_pattern_from_data(self, pattern_data):
        """Load diagram image or animation based on pattern name"""
        # Clear previous
        self.scene.clear()

        # Stop previous animations if any
        if self.singleton_anim:
            self.singleton_anim.timer.stop()
            self.singleton_anim = None
        if self.factory_anim:
            self.factory_anim.timer.stop()
            self.factory_anim = None
        if self.factory_animation:
            self.factory_animation.timer.stop()
            self.factory_animation = None
        if self.prototype_anim:
            self.prototype_anim.timer.stop()
            self.prototype_anim = None
        if self.builder_anim:
            self.builder_anim.timer.stop()
            self.builder_anim = None
        if self.state_anim:
            self.state_anim.timer.stop()
            self.state_anim = None

        pattern_name = (pattern_data.get("name") or
                        pattern_data.get("pattern_name") or
                        "Unknown").lower()

        match pattern_name:
            case "singleton":
                self.singleton_anim = SingletonAnimation(self)
                QTimer.singleShot(0, self.singleton_anim.resize_to_view)
            case "factory method":
                self.factory_anim = FactoryAnimation(self)
                QTimer.singleShot(0, self.factory_anim.resize_to_view)
            case "abstract factory":
                self.factory_animation = AbstractAnimation(self)
                QTimer.singleShot(0, self.factory_animation.resize_to_view)
            case "prototype":
                self.prototype_anim = PrototypeAnimation(self)
                QTimer.singleShot(0, self.prototype_anim.resize_to_view)
            case "builder":
                self.builder_anim = BuilderAnimation(self)
                QTimer.singleShot(0, self.builder_anim.resize_to_view)
            case "state":
                self.state_anim = StateAnimation(self)
                QTimer.singleShot(0, self.state_anim.resize_to_view)
            case _:
                self.scene.addText(f"Diagram for {pattern_name} not found.")


    def resizeEvent(self, event):
        super().resizeEvent(event)
        if hasattr(self, "singleton_anim") and self.singleton_anim:
            self.singleton_anim.resize_to_view()
        else:
            # Prevent scrollbars for static diagrams too
            self.setSceneRect(0, 0, self.viewport().width(), self.viewport().height())

