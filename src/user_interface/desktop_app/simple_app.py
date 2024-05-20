import tkinter as tk

class SimpleApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Simple App")
        self.geometry("400x300")  # Initial size
        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self, text="", font=("Arial", 20))
        self.label.pack(fill=tk.BOTH, expand=True)

        button_frame = tk.Frame(self)
        button_frame.pack(fill=tk.BOTH, expand=True)

        self.button1 = tk.Button(button_frame, text="Button 1", command=lambda: self.display_text("Word 1"))
        self.button1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.button2 = tk.Button(button_frame, text="Button 2", command=lambda: self.display_text("Word 2"))
        self.button2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.button3 = tk.Button(button_frame, text="Button 3", command=lambda: self.display_text("Word 3"))
        self.button3.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.button4 = tk.Button(button_frame, text="Button 4", command=lambda: self.display_text("Word 4"))
        self.button4.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.button5 = tk.Button(button_frame, text="Button 5", command=lambda: self.display_text("Word 5"))
        self.button5.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def display_text(self, text):
        self.label.config(text=text)

if __name__ == "__main__":
    app = SimpleApp()
    app.mainloop()
