# Standard
# None

# Pip
from aqt import mw
from aqt.qt import QMenu, QAction, qconnect

# Custom
from .main_window import MainWindow

menu = QMenu("Bunseki Frequency and Word Type", mw)

# Keep a reference to the window to prevent it from being garbage collected
global_window = None


def about_add_on() -> None:
    """
    Create and display the main window for the Bunseki Frequency and Word Type add-on.

    This function initializes a new instance of the MainWindow class and displays it,
    ensuring the window is not garbage collected by keeping a global reference.

    :return: None
    """
    global global_window
    global_window = MainWindow()
    global_window.show()


def show_about_add_on() -> None:
    """
    Create and add the 'About Bunseki' action to the tools menu.

    This function creates an action that, when triggered, calls the about_add_on function
    to display information about the Bunseki Frequency and Word Type add-on. The action is
    added to the specified menu.

    :return: None
    """
    action = QAction("About Bunseki", menu)
    qconnect(action.triggered, about_add_on)
    menu.addAction(action)
    mw.form.menuTools.addMenu(menu)


if __name__ == "__main__":
    pass
