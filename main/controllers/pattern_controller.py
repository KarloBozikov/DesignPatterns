class PatternController:
    def __init__(self, data, view):
        self.data = data
        self.view = view

        # Connect signals
        self.view.type_combo.currentTextChanged.connect(self.type_selected)
        self.view.run_button.clicked.connect(self.run_pattern)

    def type_selected(self, pattern_type):
        # Skip placeholder
        if pattern_type == "Select pattern type":
            self.view.update_pattern_dropdown([])
            return
        patterns = self.data.get_patterns_by_type(pattern_type)
        self.view.update_pattern_dropdown(patterns)

    def run_pattern(self):
        pattern_name = self.view.pattern_combo.currentText()

        if not pattern_name or pattern_name.startswith("--") or pattern_name == "Select pattern":
            # Always show a bold red error
            self.view.show_message("Select a pattern!")
            return

        pattern_data = self.data.get_pattern(pattern_name)

        if pattern_data:
            self.view.clear_message()
            # Load diagram image
            self.view.draw_pattern(pattern_data)
            # Show code
            self.view.show_code(pattern_data.get("code", ""))

