import tkinter as tk

class View(tk.Tk):
    def __init__(self, controller):
        super().__init__()

        self.controller = controller
        self.title("Simple App")
        self.geometry("400x300")  # Initial size

        self.label = tk.Label(self, text="", font=("Arial", 20))
        self.label.pack(fill=tk.BOTH, expand=True)

        button_frame = tk.Frame(self)
        button_frame.pack(fill=tk.X, expand=False)

        self.buttons = []
        for i in range(5):
            button = tk.Button(button_frame, text=f"Button {i + 1}", command=lambda i=i: self.controller.handle_button_click(i))
            button.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            self.buttons.append(button)

    def update_label(self, text):
        self.label.config(text=text)
