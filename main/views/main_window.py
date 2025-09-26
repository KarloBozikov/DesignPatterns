from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QComboBox, QSplitter, QTextEdit, QPushButton, QLabel
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont, QIcon
from .diagram_view import DiagramView

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Design Patterns Visualizer")
        self.resize(1400, 900)

        # Pattern mapping
        self.patterns = {
            "Creational": ["Singleton", "Factory Method", "Abstract Factory", "Builder", "Prototype"],
            "Structural": ["Adapter", "Bridge", "Composite", "Decorator", "Facade", "Flyweight", "Proxy"],
            "Behavioral": ["Chain of Responsibility", "Command", "Interpreter", "Iterator",
                           "Mediator", "Memento", "Observer", "State", "Strategy", "Template Method", "Visitor"]
        }

        # Dropdowns
        self.type_combo = QComboBox()
        self.type_combo.setMinimumHeight(35)
        self.type_combo.setFont(QFont("Arial", 12))
        self.type_combo.addItem("Select pattern type")
        self.type_combo.addItems(self.patterns.keys())
        self.type_combo.currentTextChanged.connect(self.update_pattern_combo)

        self.pattern_combo = QComboBox()
        self.pattern_combo.setMinimumHeight(35)
        self.pattern_combo.setFont(QFont("Arial", 12))
        self.pattern_combo.addItem("Select pattern")

        # Message label (bold red)
        self.message_label = QLabel("")
        self.message_label.setFont(QFont("Arial", 12, QFont.Bold))
        self.message_label.setStyleSheet("color: red;")
        self.message_label.setAlignment(Qt.AlignCenter)

        # Run/Play button (always enabled, icon only)
        self.run_button = QPushButton()
        self.run_button.setIcon(QIcon.fromTheme("media-playback-start"))
        self.run_button.setIconSize(QSize(32, 32))
        self.run_button.setMinimumHeight(40)
        self.run_button.setStyleSheet(
            """
            QPushButton {
                background-color: #28a745;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
            """
        )
        self.run_button.clicked.connect(self.run_visualization)

        # Left panel layout
        left_panel = QWidget()
        left_layout = QVBoxLayout()
        left_layout.addWidget(self.type_combo)
        left_layout.addWidget(self.pattern_combo)
        left_layout.addWidget(self.run_button)
        left_layout.addWidget(self.message_label)
        left_layout.addStretch()
        left_panel.setLayout(left_layout)

        # Diagram and code view
        self.diagram_view = DiagramView()
        self.code_view = QTextEdit()
        self.code_view.setReadOnly(True)
        self.code_view.setFont(QFont("Courier", 10))

        # Main splitter
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(left_panel)
        splitter.addWidget(self.diagram_view)
        splitter.addWidget(self.code_view)
        splitter.setSizes([250, 500, 300])
        self.setCentralWidget(splitter)

    def update_pattern_combo(self, pattern_type):
        self.pattern_combo.clear()
        self.pattern_combo.addItem("Select pattern")
        if pattern_type in self.patterns:
            self.pattern_combo.addItems(self.patterns[pattern_type])
        self.message_label.setText("")  # clear message on type change

    def run_visualization(self):
        pattern_name = self.pattern_combo.currentText()
        if pattern_name and pattern_name != "Select pattern":
            self.message_label.setText("")  # clear previous message
            self.diagram_view.play_animation(pattern_name)
        else:
            self.message_label.setText("Select a pattern to run!")  # show bold red message
