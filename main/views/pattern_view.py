class PatternView:
    def __init__(self, diagram_view, code_view, message_label, type_combo, pattern_combo, run_button):
        self.diagram_view = diagram_view
        self.code_view = code_view
        self.message_label = message_label
        self.type_combo = type_combo
        self.pattern_combo = pattern_combo
        self.run_button = run_button

    def update_pattern_dropdown(self, patterns):
        self.pattern_combo.clear()
        self.pattern_combo.addItem("-- Select pattern --")
        self.pattern_combo.addItems(patterns)

    def draw_pattern(self, pattern_data):
        self.diagram_view.draw_pattern_from_data(pattern_data)

    def show_code(self, code):
        self.code_view.setPlainText(code)

    def show_message(self, msg):
        self.message_label.setStyleSheet("color: red; font-weight: bold;")
        self.message_label.setText(msg)

    def clear_message(self):
        self.message_label.clear()
