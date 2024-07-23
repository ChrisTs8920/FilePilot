import os
import func
import globals
import ui

# TODO:
# Linux compatibility,
# Add move file function,
# editable path,
# code improvements, refactoring

def main():
    # global file_path
    globals.file_path = os.path.join(os.path.dirname(__file__), "../icons/")
    
    func.AppInitializer()

    root = ui.create_window()
    ui.create_widgets(root)
    ui.refresh([])
    root.mainloop()


if __name__ == "__main__":
    main()
