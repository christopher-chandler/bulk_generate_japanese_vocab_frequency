# -*- coding: utf-8 -*-
"""
Created on 09/12/2014
@author: Myxoma

updated on 18/07/2024
@author: christopherchandler

This add-on inserts the frequency for a given Japanese word to a given
Anki field.
"""

# Standard
import re
import sqlite3
from sqlite3 import OperationalError

# Pip
from aqt import mw, QMenu, QAction

from anki.hooks import addHook
from aqt.utils import showInfo
from aqt.browser import Browser


# Custom

from .bunseki.main_tools_menu.anki_main_menu_tool import show_about_add_on

# Config fields
FREQUENCY_DICTIONARY = ""
VOCABULARY_DICTIONARY = ""
NOTE_TYPE = ""
VOCABULARY_INPUT_FIELD = ""
FREQUENCY_FIELD = ""
WORD_TYPE_FIELD = ""
OVERWRITE_DESTINATION_FIELD = True

# Regex
re_xml_tag = re.compile(r"<.*?>")  # HTML/XML tags
re_parenthesis = re.compile(r"[(（].*[)）]")  # Handle JP parenthesis too

show_about_add_on()


def reload_json_config():
    global FREQUENCY_DICTIONARY
    global VOCABULARY_DICTIONARY
    global NOTE_TYPE
    global VOCABULARY_INPUT_FIELD
    global FREQUENCY_FIELD
    global WORD_TYPE_FIELD
    global OVERWRITE_DESTINATION_FIELD

    config = mw.addonManager.getConfig(__name__)
    vocab_dict = config["0_jm_dict"]
    freq_dict = config["0_freq_dict"]
    note_type = config["01_note_type"]
    vocab_input_field = config["02_vocab_input_field"]
    frequency_field = config["03_frequency_output_field"]
    word_type_field = config["03_word_type_output_field"]
    overwrite_destination_field = config["04_overwrite_destination_field"]


def preprocess_field(content: str) -> str:
    """
    Performs the following operations on the given field content:
    - Remove HTML/XML tags
    - Remove parenthesis and their contents
    - Replace non-breaking space with actual space
    - Trim leading and trailing whitespace

    :param content: The field's content to preprocess
    :return: The vocab literal
    """

    # Replace non-breaking space
    content = content.replace("&nbsp;", " ")

    # Remove HTML/XML tags (just the tags, keep contents)
    content = re_xml_tag.sub("", content)

    # Remove parenthesis and their contents
    content = re_parenthesis.sub("", content)

    # Strip leading and trailing whitespace
    content = content.strip()

    return content


def bulk_generate_vocab_frequency_fg(note_identifiers):

    reload_json_config()
    freq_db = sqlite3.connect(FREQUENCY_DICTIONARY)

    i = 0

    for identifier in note_identifiers:

        note = mw.col.getNote(identifier)
        note_model = note.model()["name"]

        error_msg = {
            1: f"Note type mismatch: {NOTE_TYPE}. Please check your config file to set the correct note type.",
            2: f"Vocab field '{VOCABULARY_INPUT_FIELD}' not found!",
            3: f"Destination field '{FREQUENCY_FIELD}' not found!",
            4: f"{VOCABULARY_INPUT_FIELD} is not empty. Skipping!",
        }

        if NOTE_TYPE not in note_model:
            showInfo(error_msg.get(1))
            break

        source = None
        if VOCABULARY_INPUT_FIELD in note:
            source = VOCABULARY_INPUT_FIELD
        if not source:
            showInfo(error_msg.get(2))
            break

        destination = None
        if FREQUENCY_FIELD in note:
            destination = FREQUENCY_FIELD
        if not destination:
            showInfo(error_msg.get(3))
            break

        if note[destination] and not OVERWRITE_DESTINATION_FIELD:
            showInfo(error_msg.get(4))
            break

        try:
            i += 1
            if i == 1:
                showInfo("Frequency data added.")

            vocab_query = preprocess_field(note[source])

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
    freq_db = sqlite3.connect(VOCABULARY_DICTIONARY)

    i = 0

    for identifier in note_identifiers:

        note = mw.col.getNote(identifier)
        note_model = note.model()["name"]

        error_msg = {
            1: f"Note type mismatch: {NOTE_TYPE}",
            2: f"Vocab field '{VOCABULARY_INPUT_FIELD}' not found!",
            3: f"Destination field '{WORD_TYPE_FIELD}' not found!",
            4: f"{VOCABULARY_INPUT_FIELD} is not empty. Skipping!",
        }

        if NOTE_TYPE not in note_model:
            showInfo(error_msg.get(1))
            break

        source = None
        if VOCABULARY_INPUT_FIELD in note:
            source = VOCABULARY_INPUT_FIELD
        if not source:
            showInfo(error_msg.get(2))
            break

        destination = None
        if WORD_TYPE_FIELD in note:
            destination = WORD_TYPE_FIELD
        if not destination:
            showInfo(error_msg.get(3))
            break

        if note[destination] and not OVERWRITE_DESTINATION_FIELD:
            showInfo(error_msg.get(4))
            break

        try:
            i += 1
            if i == 1:
                showInfo("Word type data added")

            vocab_query = preprocess_field(note[source])

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


def set_up_edit_menu(browser: Browser):
    menu = browser.form.menuEdit
    submenu = QMenu("Japanese Frequency & Word Type Analyzer", browser)

    # Create actions
    bulk_generate_frequency = QAction("Generate Vocab Frequency", browser)
    bulk_generate_word_type = QAction("Generate Word Type Data", browser)

    # Connect actions to their handlers
    bulk_generate_frequency.triggered.connect(
        lambda _, brow=browser: on_bulk_generate_vocab(brow)
    )
    bulk_generate_word_type.triggered.connect(
        lambda _, brow=browser: on_generate_word_type(brow)
    )

    # Add actions to the submenu
    submenu.addAction(bulk_generate_frequency)
    submenu.addAction(bulk_generate_word_type)
    bulk_generate_word_type.setToolTip("This action generates word type data.")
    # Add submenu to the main edit menu
    menu.addSeparator()  # Optional: Add a separator for visual clarity
    menu.addMenu(submenu)


def on_bulk_generate_vocab(browser: Browser) -> None:

    if VOCABULARY_INPUT_FIELD or FREQUENCY_FIELD or WORD_TYPE_FIELD == "":
        showInfo(NOTE_TYPE, str(FREQUENCY_FIELD), OVERWRITE_DESTINATION_FIELD)

    else:
        showInfo(
            f"Frequency: Beginning with the following config:\n\nNote type: {NOTE_TYPE}"
            f"\nVocab: {VOCABULARY_INPUT_FIELD}\nDestination field: {FREQUENCY_FIELD}"
            f"\nOverwrite destination field: {OVERWRITE_DESTINATION_FIELD}"
        )
        bulk_generate_vocab_frequency_fg(browser.selectedNotes())


def on_generate_word_type(browser: Browser):
    showInfo(
        f"Word Type: Beginning with the following config:\n\nNote type: {NOTE_TYPE}"
        f"\nVocab: {VOCABULARY_INPUT_FIELD}\nDestination field: {WORD_TYPE_FIELD}"
        f"\nOverwrite destination field: {OVERWRITE_DESTINATION_FIELD}"
    )
    bulk_generate_word_type_fg(browser.selectedNotes())


# Hook into the browser setup menus
addHook("browser.setupMenus", set_up_edit_menu)
