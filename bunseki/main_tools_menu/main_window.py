# Standard
import sys
import webbrowser

# Pip
from PyQt6 import QtGui, QtWidgets, QtCore
from PyQt6.QtWidgets import QMainWindow

# Custom
from .about_add_on import Ui_MainWindow
from ..settings.constants.constant_paths import GeneralPaths as Gp
from ..settings.logger.basic_logger import catch_and_log_info
from ..addon_configs import load_json_config_data

debug = load_json_config_data().get("debug")


class MainWindow(QMainWindow, Ui_MainWindow):
    """
    Main window class for the Bunseki Frequency and Word Type add-on.

    This class initializes the UI, connects buttons and events, and handles the
    functionality for displaying the about window and opening external links.
    """

    def __init__(self):
        """
        Initialize the MainWindow.

        This constructor sets up the UI components, connects signals to slots,
        and assigns functionalities to widgets.
        """
        super().__init__()
        self.setupUi(self)
        _translate = QtCore.QCoreApplication.translate

        # Connect the close button to its handler
        self.closeWindow.clicked.connect(self.close_about_window)
        self.githubLabel.setPixmap(QtGui.QPixmap(Gp.IMAGES.value + "github.png"))

        # ToolTips
        self.githubLabel.setToolTip(_translate("Dialog", "opens the github webpage"))

        # Assign the openLink method to the QLabel's mousePressEvent
        self.thumbsUpLikeAddOn.mousePressEvent = self.open_anki_like_page

        text = open(
            "/Users/christopherchandler/Library/Application Support/Anki2/addons21/1004691625/log/bunseki.log_2024_07_19.log"
        ).read()
        self.addonLogTextBrowser_2.setText(text)

        if debug == False:
            self.tabWidget.removeTab(2)

    def close_about_window(self) -> None:
        """
        Close the about window.

        This method closes the about window and logs the action.

        :return: None
        """
        self.close()
        catch_and_log_info(custom_message="Closed about window.")

    @staticmethod
    def open_anki_like_page() -> None:
        """
        Open the Anki like page.

        This method opens the specified URL in the default web browser and logs the action.

        :return: None
        """
        webbrowser.open("https://ankiweb.net/shared/review/1004691625")
        catch_and_log_info(custom_message="Anki web page opened.")


if __name__ == "__main__":
    """
    Main entry point for the application.

    This block initializes the QApplication, creates and shows the main window,
    and starts the application event loop.

    :return: None
    """
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
