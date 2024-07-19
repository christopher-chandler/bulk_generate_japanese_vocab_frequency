# Standard
# None

# Pip
# None

# Custom
from .dialog import UpdateDialog


def show_update_message() -> None:
    global global_window
    global_window = UpdateDialog()
    global_window.show()
