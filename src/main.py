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
    func.checkPlatform()
    func.read_theme()
    func.read_font()
    root = ui.createWindow()

    ui.create_widgets(root)
    ui.refresh([])
    root.mainloop()


if __name__ == "__main__":
    main()
