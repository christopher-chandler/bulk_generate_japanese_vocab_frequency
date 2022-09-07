# -*- coding: utf-8 -*-
"""
Created on 09/12/2014
@author: Myxoma

updated on 01/09/2022
@author: christopherchandler

This add-on inserts the frequency rating retrieved from the supplied frequency
Rikai-Sama dictionary for a given Japanese word to a given Anki field
both fields are specified by the user.
"""

# Standard
import platform
import sqlite3
from sqlite3 import OperationalError

# Custom
# None

# Pip
from aqt import mw
from aqt.utils import showInfo

# Check os system
os_name = platform.system()

if os_name == "Darwin":
    freq_dict = "freq_dict/freq_dict.db"
else:
    freq_dict = "freq_dict\\freq_dict.db"

note_type = ""
vocab_input_field = ""
destination_field = ""
overwrite_destination_field = True
add_on_name = "Bulk Generate Japanese Vocab Frequency"

error_msg = {
    "incorrect_note_model": f"Note type mismatch: {note_type} vs. ",
    "incorrect_source_field": f"Source field '{vocab_input_field}' not found!",
    "incorrect_destination_field": f"Destination field '{destination_field}' not found!",
    4: f"{vocab_input_field} is not empty. Skipping!",
}


def reload_json_config() -> None:
    """
    The configs specified in the json file are loaded into the Anki add-on.

    The variables are set as globals so that they can be
    overwritten when reloading the button.

    :return:
        None
    """

    global freq_dict
    global note_type
    global vocab_input_field
    global destination_field
    global overwrite_destination_field

    # Json config file settings
    config = mw.addonManager.getConfig(__name__)

    if config["freq_dict"]:
        freq_dict = config["freq_dict"]
    else:
        freq_dict = freq_dict

    note_type = config["01_note_type"]
    vocab_input_field = config["02_vocab_input_field"]
    destination_field = config["03_frequency_output_field"]
    overwrite_destination_field = config["04_overwrite_destination_field"]


def bulk_generate_vocab(note_identifiers) -> None:
    """
    The cards selected by the user are read into this function.
    If the vocab word selected by the user is present in the database,
    then its frequency will be added to the appropriate field.
    It should be noted that multiple coulds could possible have the same
    frequency due to how the database was created.

    :param note_identifiers: The cards selected by the users.

    :return:
        None
    """

    reload_json_config()
    freq_db = sqlite3.connect(freq_dict)  # Load SQL DB

    i = 0

    """
    If a field or card type has been improperly labeled, 
    then a warning code via a dialog box is presented to the user. 
    """
    for identifier in note_identifiers:

        # Note, i.e., card type is incorrect.
        note = mw.col.getNote(identifier)
        note_type = note.model()["name"]

        if note_type not in note_type:
            showInfo(error_msg.get("incorrect_note_type") + note_type)
            break

        # Target word, i.e., source field
        source = None
        if vocab_input_field in note:
            source = vocab_input_field
        if not source:
            showInfo(error_msg.get("incorrect_source_field"))
            break

        # Frequency field, i.e., destination field
        destination = None
        if destination_field in note:
            destination = destination_field
        if not destination:
            showInfo(error_msg.get("incorrect_destination_field"))
            break

        # Overwrite field
        if note[destination] and not overwrite_destination_field:
            showInfo(error_msg.get(4))
            break

        try:
            i += 1
            if i == 1:
                # if the settings are correct
                showInfo("Frequency data added to the selected cards.")

            vocab_query = note[source]
            if vocab_query != "":
                sql_query = (
                    f"""select freq from freq_dict where expression ='{vocab_query}';"""
                )
                try:
                    # Word frequency exists
                    cursor = freq_db.cursor()
                    cursor.execute(sql_query)
                    single_result = cursor.fetchone()
                    if single_result is not None:
                        note[destination] = single_result[0]
                    else:
                        # Word frequency does not exist
                        note[destination] = "UNK"

                except OperationalError:
                    pass
        # If vocab query fails for an unknown reason.
        except:
            raise

        note.flush()
    freq_db.close()
    mw.progress.finish()
    mw.reset()


def on_bulk_generate_vocab(browser) -> None:
    """
    This function is called by set_up_edit_menu
    when the corresponding menu item is clicked.

    :param browser: The menu in the card browser menu
    :return:
    """
    showInfo(
        f"Beginning with the following config:\n\nNote type: {note_type}"
        f"\nSource field: {vocab_input_field}\nDestination field: {destination_field}"
        f"\nOverwrite destination field: {overwrite_destination_field}"
    )
    bulk_generate_vocab(browser.selectedNotes())


def set_up_edit_menu(browser) -> None:
    """
    This adds the menu item to the browser edit menu. By clicking this menu item
    the add-on is activated.

    :param browser: The anki browser menu.
    :return:
        None
    """
    menu = browser.form.menuEdit
    menu.addSeparator()
    menu_item = menu.addAction(add_on_name)
    menu_item.triggered.connect(lambda _, brow=browser: on_bulk_generate_vocab(brow))