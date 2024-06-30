# -*- coding: utf-8 -*-
"""
Created on 09/12/2014
@author: Myxoma

updated on 01/09/2022
@author: christopherchandler

This add-on inserts the frequency for a given Japanese word to a given
Anki field.
"""

# Standard
import re
import sqlite3
from sqlite3 import OperationalError

# Custom
# None

# Pip
from anki.hooks import addHook
from aqt import mw
from aqt.utils import showInfo

freq_dict = ""
vocab_dict = ""
note_type = ""
vocab_input_field = ""
frequency_field = ""
word_type_field = ""
overwrite_destination_field = True

re_xml_tag = re.compile(r"<.*?>")


def reload_json_config():
    global freq_dict
    global vocab_dict
    global note_type
    global vocab_input_field
    global frequency_field
    global word_type_field
    global overwrite_destination_field

    config = mw.addonManager.getConfig(__name__)
    vocab_dict = config["0_jm_dict"]
    freq_dict = config["0_freq_dict"]
    note_type = config["01_note_type"]
    vocab_input_field = config["02_vocab_input_field"]
    frequency_field = config["03_frequency_output_field"]
    word_type_field = config["03_word_type_output_field"]
    overwrite_destination_field = config["04_overwrite_destination_field"]


def bulk_generate_vocab_frequency_fg(note_identifiers):

    reload_json_config()
    freq_db = sqlite3.connect(freq_dict)

    i = 0

    for identifier in note_identifiers:

        note = mw.col.getNote(identifier)
        note_model = note.model()["name"]

        error_msg = {
            1: f"Note type mismatch: {note_type}",
            2: f"Vocab field '{vocab_input_field}' not found!",
            3: f"Destination field '{frequency_field}' not found!",
            4: f"{vocab_input_field} is not empty. Skipping!",
        }

        if note_type not in note_model:
            showInfo(error_msg.get(1))
            break

        source = None
        if vocab_input_field in note:
            source = vocab_input_field
        if not source:
            showInfo(error_msg.get(2))
            break

        destination = None
        if frequency_field in note:
            destination = frequency_field
        if not destination:
            showInfo(error_msg.get(3))
            break

        if note[destination] and not overwrite_destination_field:
            showInfo(error_msg.get(4))
            break

        try:
            i += 1
            if i == 1:
                showInfo("Frequency data added")

            vocab_query = note[source]
            vocab_query = re_xml_tag.sub("", vocab_query)  # Remove HTML/XML tags
            if vocab_query != "":
                sql_query = f"""select freq from freq_dict 
                    where expression ='{vocab_query}';"""
                try:
                    cursor = freq_db.cursor()
                    cursor.execute(sql_query)
                    single_result = cursor.fetchone()
                    if single_result is not None:
                        note[destination] = single_result[0]
                    else:
                        note[destination] = "UNK"

                except OperationalError:
                    pass
        except:
            raise

        note.flush()
    freq_db.close()
    mw.progress.finish()
    mw.reset()


def bulk_generate_word_type_fg(note_identifiers):

    reload_json_config()
    freq_db = sqlite3.connect(vocab_dict)

    i = 0

    for identifier in note_identifiers:

        note = mw.col.getNote(identifier)
        note_model = note.model()["name"]

        error_msg = {
            1: f"Note type mismatch: {note_type}",
            2: f"Vocab field '{vocab_input_field}' not found!",
            3: f"Destination field '{word_type_field}' not found!",
            4: f"{vocab_input_field} is not empty. Skipping!",
        }

        if note_type not in note_model:
            showInfo(error_msg.get(1))
            break

        source = None
        if vocab_input_field in note:
            source = vocab_input_field
        if not source:
            showInfo(error_msg.get(2))
            break

        destination = None
        if word_type_field in note:
            destination = word_type_field
        if not destination:
            showInfo(error_msg.get(3))
            break

        if note[destination] and not overwrite_destination_field:
            showInfo(error_msg.get(4))
            break

        try:
            i += 1
            if i == 1:
                showInfo("Word type data added")

            vocab_query = note[source]
            vocab_query = re_xml_tag.sub("", vocab_query)  # Remove HTML/XML tags
            if vocab_query != "":
                sql_query = f"""select Meaning from jmdict 
                    where expression='{vocab_query}';"""
                try:
                    cursor = freq_db.cursor()
                    cursor.execute(sql_query)
                    single_result = cursor.fetchone()
                    if single_result is not None:
                        note[destination] = single_result[0]
                    else:
                        note[destination] = "UNK"

                except OperationalError:
                    pass
        except:
            raise

        note.flush()
    freq_db.close()
    mw.progress.finish()
    mw.reset()


def set_up_edit_menu(browser):
    menu = browser.form.menuEdit
    menu.addSeparator()
    bulk_generate_frequency = menu.addAction("Bulk Generate Vocab Frequency")
    bulk_generate_frequency.triggered.connect(lambda _, brow=browser: on_bulk_generate_vocab(brow))

    bulk_generate_word_type = menu.addAction("Bulk Generate Word Type Data")
    bulk_generate_word_type.triggered.connect(lambda _, brow=browser: on_generate_word_type(brow))


def on_bulk_generate_vocab(browser):
    showInfo(f"Frequency: Beginning with the following config:\n\nNote type: {note_type}"
             f"\nVocab: {vocab_input_field}\nDestination field: {frequency_field}"
             f"\nOverwrite destination field: {overwrite_destination_field}")
    bulk_generate_vocab_frequency_fg(browser.selectedNotes())


def on_generate_word_type(browser):
    showInfo(f"Word Type: Beginning with the following config:\n\nNote type: {note_type}"
             f"\nVocab: {vocab_input_field}\nDestination field: {word_type_field}"
             f"\nOverwrite destination field: {overwrite_destination_field}")
    bulk_generate_word_type_fg(browser.selectedNotes())


addHook("browser.setupMenus", set_up_edit_menu)

if __name__ == "__main__":
    pass
