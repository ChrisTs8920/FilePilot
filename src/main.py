import os
import func
import globals
import ui

# TODO:
# Further tests and fixes on linux,
# Add move file function,
# editable path,
# code improvements, refactoring

def main():
    # globals.file_path = os.path.join(os.path.dirname(__file__), "../icons/") # old
    globals.file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../icons/")) + "/"
    func.check_platform()
    func.read_theme()
    func.read_font()
    root = ui.create_window()

    ui.create_widgets(root)
    ui.refresh([])
    root.mainloop()


if __name__ == "__main__":
    main()
