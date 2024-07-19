from PyQt6 import QtCore, QtGui, QtWidgets
from .main_window import Ui_MainWindow


class UpdateDialog(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.ui = Ui_MainWindow()
