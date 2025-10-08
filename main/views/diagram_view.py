from PySide6.QtWidgets import QGraphicsView, QGraphicsScene
from PySide6.QtCore import Qt, QTimer
import os

# Importing creational patterns
from .pattern_diagrams.creational.singleton import SingletonAnimation
from .pattern_diagrams.creational.factoryMethod import FactoryAnimation
from .pattern_diagrams.creational.abstractFactory import AbstractAnimation
from .pattern_diagrams.creational.prototype import PrototypeAnimation
from .pattern_diagrams.creational.builder import BuilderAnimation

# Importing structural patterns
from .pattern_diagrams.structural.adapter import AdapterAnimation
from .pattern_diagrams.structural.bridge import BridgeAnimation
from .pattern_diagrams.structural.composite import CompositeAnimation
from .pattern_diagrams.structural.decorator import DecoratorAnimation
from .pattern_diagrams.structural.facade import FacadeAnimation
from .pattern_diagrams.structural.flyweight import FlyweightAnimation
from .pattern_diagrams.structural.proxy import ProxyAnimation

# Importing behavioral patterns
from .pattern_diagrams.behavioral.state import StateAnimation

class DiagramView(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.setAlignment(Qt.AlignCenter)

        self.diagram_path = os.path.join(os.path.dirname(__file__), "..", "resources", "diagram")

        # Currently running animation
        self.current_anim = None

        # Pattern → Animation class mapping
        self.animations = {
            "singleton": SingletonAnimation,
            "factory method": FactoryAnimation,
            "abstract factory": AbstractAnimation,
            "prototype": PrototypeAnimation,
            "builder": BuilderAnimation,
            "adapter": AdapterAnimation,
            "bridge": BridgeAnimation,
            "composite": CompositeAnimation,
            "decorator": DecoratorAnimation,
            "facade": FacadeAnimation,
            "flyweight": FlyweightAnimation,
            "proxy": ProxyAnimation,
            "state": StateAnimation,
        }

    def draw_pattern_from_data(self, pattern_data):
        """Load diagram image or animation based on pattern name"""
        # Clear previous
        self.scene.clear()

        # Stop previous animation
        if self.current_anim:
            self.current_anim.timer.stop()
            self.current_anim = None

        pattern_name = (pattern_data.get("name") or
                        pattern_data.get("pattern_name") or
                        "Unknown").lower()

        # Look up animation class
        anim_class = self.animations.get(pattern_name)

        if anim_class:
            self.current_anim = anim_class(self)
            QTimer.singleShot(0, self.current_anim.resize_to_view)
        else:
            self.scene.addText(f"Diagram for {pattern_name} not found.")

    def resizeEvent(self, event):
        super().resizeEvent(event)

        if self.current_anim:
            # Let the active animation resize itself
            self.current_anim.resize_to_view()
        else:
            # Prevent scrollbars for static diagrams
            self.setSceneRect(0, 0, self.viewport().width(), self.viewport().height())
