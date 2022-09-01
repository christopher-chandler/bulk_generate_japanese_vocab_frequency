# Standard
import sqlite3

# Custom
# None

# Pip
from anki.hooks import addHook
from aqt import mw
from aqt.utils import showInfo, showWarning
from aqt.qt import *

FrequencyDBname = "freq.sqlite"

freq_dict = ""
note_type = ""
vocab_input_field = ""
destination_field = ""
overwrite_destination_field = True


def reload_json_config():
    global freq_dict
    global note_type
    global vocab_input_field
    global destination_field
    global overwrite_destination_field

    config = mw.addonManager.getConfig(__name__)
    freq_dict = config["0_freq_dict"]
    note_type = config["01_note_type"]
    vocab_input_field = config["02_vocab_input_field"]
    destination_field = config["03_frequency_output_field"]
    overwrite_destination_field = config['04_overwrite_destination_field"']


def bulk_generate_vocab_fg(nids):
    mw.checkpoint("bulk-Generate Vocab Fq")
    mw.progress.start()
    reload_json_config()
    freq_db = sqlite3.connect(freq_dict)
    for nid in nids:
        note = mw.col.getNote(nid)
        if note_type not in note.model()["name"]:
            continue
        source = None
        if vocab_input_field in note:
            source = vocab_input_field
        if not source:
            continue
        destination = None
        if destination_field in note:
            destination = destination_field
        if not destination:
            continue
        if note[destination] and not overwrite_destination_field:
            continue
        try:
            vocab_query = note[source]
            if vocab_query != "":
                m_query = f"select freq from Dict where expression = {vocab_query}"
                cursor = freq_db.cursor()
                cursor.execute(m_query)
                single_result = cursor.fetchone()
                if single_result is not None:
                    note[destination] = single_result[0]

        except Exception as error:
            raise
        note.flush()
    freq_db.close()
    mw.progress.finish()
    mw.reset()


def set_up_menu(browser):
    menu = browser.form.menuEdit
    menu.addSeparator()
    a = menu.addAction("Bulk Generate Vocab Frequency")
    a.triggered.connect(lambda _, b=browser: on_bulk_generate_vocab(b))


def on_bulk_generate_vocab(browser):
    bulk_generate_vocab_fg(browser.selectedNotes())


addHook("browser.setupMenus", set_up_menu)


if __name__ == "__main__":
    pass
