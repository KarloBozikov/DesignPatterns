from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsPixmapItem
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
import os

class DiagramView(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.setAlignment(Qt.AlignCenter)

        # Path to diagrams
        self.diagram_path = os.path.join(os.path.dirname(__file__), "..", "resources", "diagram")

    def draw_pattern_from_data(self, pattern_data):
        """Load diagram image based on pattern name"""
        self.scene.clear()

        pattern_name = pattern_data.get("name") or pattern_data.get("pattern_name") or "Unknown"
        filename = f"{pattern_name.replace(' ', '')}.png"  # remove spaces in filename
        filepath = os.path.join(self.diagram_path, filename)

        if os.path.exists(filepath):
            pixmap = QPixmap(filepath)
            item = QGraphicsPixmapItem(pixmap)
            self.scene.addItem(item)
            # center image
            item.setPos(-pixmap.width()/2, -pixmap.height()/2)
            self.setSceneRect(item.boundingRect())
        else:
            # fallback message if image not found
            self.scene.addText(f"Diagram for {pattern_name} not found.")
