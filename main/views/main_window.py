import os

from PySide6 import QtCore
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QComboBox, QSplitter, QTextEdit, QPushButton, QLabel, QToolButton
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont, QIcon, QAction, QCursor

from .diagram_view import DiagramView
from .pattern_view import PatternView
from models.pattern_data import PatternData
from controllers.pattern_controller import PatternController


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Design Patterns Visualizer")
        self.resize(1400, 900)

        # --- Window icon ---
        window_icon = QIcon()
        window_icon.addFile('resources/icons/logo_guru.png')
        self.setWindowIcon(window_icon)

        # --- Hamburger button in toolbar ---
        self.hamburger_btn = QToolButton()
        self.hamburger_btn.setText("☰")
        self.hamburger_btn.setFont(QFont("Arial", 14, QFont.Bold))
        self.hamburger_btn.setFixedSize(40, 40)
        self.hamburger_btn.setStyleSheet("""
            QPushButton { color: #ffffff; border: none; }
            QPushButton:hover { color: #d1d0cd; }
        """)
        self.hamburger_btn.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.hamburger_btn.clicked.connect(self.toggle_left_panel)

        # --- Title in toolbar ---
        self.toolbar_title = QLabel(self)
        self.toolbar_title.setText("Design Patterns Visualizer")
        self.toolbar_title.setFont(QFont("Arial", 14, QFont.Bold))
        self.toolbar_title.setStyleSheet("border: none;")

        # Put it inside the window toolbar
        toolbar = self.addToolBar("Main")
        toolbar.setMovable(False)
        toolbar.setFloatable(False)
        toolbar.setIconSize(QSize(32, 32))
        toolbar.addWidget(self.hamburger_btn)
        toolbar.addWidget(self.toolbar_title)

        # --- Selector widgets ---
        self.type_combo = QComboBox()
        self.type_combo.setMinimumHeight(35)
        self.type_combo.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.type_combo.setFont(QFont("Arial", 12))
        self.type_combo.addItem("-- Select pattern type --")
        self.type_combo.addItems(["Creational", "Structural", "Behavioral"])

        self.pattern_combo = QComboBox()
        self.pattern_combo.setMinimumHeight(35)
        self.pattern_combo.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.pattern_combo.setFont(QFont("Arial", 12))
        self.pattern_combo.addItem("-- Select pattern --")

        self.message_label = QLabel("")
        self.message_label.setFont(QFont("Arial", 12, QFont.Bold))
        self.message_label.setStyleSheet("color: red;")
        self.message_label.setAlignment(Qt.AlignCenter)

        self.run_button = QPushButton()
        self.run_button.setIcon(QIcon.fromTheme("media-playback-start"))
        self.run_button.setIconSize(QSize(32, 32))
        self.run_button.setMinimumHeight(40)
        self.run_button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.run_button.setStyleSheet("""
            QPushButton { background-color: #28a745; border-radius: 5px; }
            QPushButton:hover { background-color: #218838; }
        """)

        # --- Left panel layout ---
        left_panel = QWidget()
        left_layout = QVBoxLayout()
        left_layout.setContentsMargins(10, 10, 10, 10)
        left_layout.addWidget(self.type_combo)
        left_layout.addWidget(self.pattern_combo)
        left_layout.addWidget(self.run_button)
        left_layout.addWidget(self.message_label)
        left_layout.addStretch()
        left_panel.setLayout(left_layout)

        # --- Diagram views ---
        self.diagram_view = DiagramView()
        self.diagram_view.setStyleSheet("""padding: 5px;""")

        # --- Code views ---
        self.code_view = QTextEdit()
        self.code_view.setReadOnly(True)
        self.code_view.setFont(QFont("Ariel", 12))
        self.code_view.setStyleSheet("""padding: 5px;""")

        # --- Splitter ---
        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.addWidget(left_panel)
        self.splitter.addWidget(self.diagram_view)
        self.splitter.addWidget(self.code_view)
        self.splitter.setSizes([250, 500, 300])
        self.setCentralWidget(self.splitter)

        # --- store reference to left_panel ---
        self.left_panel = left_panel
        self.left_panel_width = 250  # initial width

        # --- hook up MVC ---
        data = PatternData()
        view = PatternView(
            diagram_view=self.diagram_view,
            code_view=self.code_view,
            message_label=self.message_label,
            type_combo=self.type_combo,
            pattern_combo=self.pattern_combo,
            run_button=self.run_button
        )
        self.controller = PatternController(data, view)

    def toggle_left_panel(self):
        """Collapse/expand left panel when hamburger is clicked."""
        sizes = self.splitter.sizes()

        if sizes[0] == 0:
            # --- Expand back to saved width ---
            self.splitter.setSizes([self.left_panel_width, sizes[1], sizes[2]])
        else:
            # --- Collapse left panel ---
            self.left_panel_width = sizes[0]

            # Remaining width after collapsing
            remaining = sizes[1] + sizes[2] + self.left_panel_width

            # 60% for diagram, 40% for code view
            diagram_width = int(remaining * 0.6)
            code_width = remaining - diagram_width

            self.splitter.setSizes([0, diagram_width, code_width])
