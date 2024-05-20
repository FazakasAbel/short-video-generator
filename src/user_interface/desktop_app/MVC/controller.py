class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def handle_button_click(self, button_index):
        words = ["Word 1", "Word 2", "Word 3", "Word 4", "Word 5"]
        self.model.set_text(words[button_index])
        self.view.update_label(self.model.get_text())
