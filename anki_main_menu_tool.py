from aqt import mw
from aqt.qt import *

menu = QMenu("Pika", mw)

def on_action():
    data  = str(os.listdir(os.curdir))
    open(
        file="/Users/christopherchandler/Library/Application Support/Anki2/addons21/1004691625/test.txt",
        mode="w+"
    ).write(data)

action = QAction("Some action", menu)
qconnect(action.triggered, on_action)
menu.addAction(action)

another_action = QAction("Another action", menu)
qconnect(another_action.triggered, on_action)
menu.addAction(another_action)

mw.form.menuTools.addMenu(menu)
