from controller import Controller
from model import Model
from view import View

def main():
    model = Model()
    controller = Controller(model, None)
    view = View(controller)
    controller.view = view
    view.mainloop()

if __name__ == "__main__":
    main()
