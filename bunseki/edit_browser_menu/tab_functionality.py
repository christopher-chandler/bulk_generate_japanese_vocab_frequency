# Standard
# None

# Pip
from aqt.utils import showInfo, askUser
from aqt.browser import Browser

# Custom
from ..addon_configs import load_json_config_data
from .generate_data import pull_data_from_dictionary

config_data = load_json_config_data()

FREQUENCY_DICTIONARY = config_data.get("frequency_dict")
JMDICT = config_data.get("jmdict")
NOTE_TYPE = config_data.get("note_type")
VOCABULARY_INPUT_FIELD = config_data.get("vocabulary_input_field")
FREQUENCY_FIELD = config_data.get("frequency_field")
WORD_TYPE_FIELD = config_data.get("word_type_field")
OVERWRITE_DESTINATION_FIELD = True
DISABLE_WARNINGS = config_data.get("disable_warnings")


def generate_information_for_selected_cards(
    browser: Browser, info_title: str, data_generation_type: str, dictionary_source: str
) -> None:
    """Generates information about the selected cards for data insertion.

    This function displays a dialog box showing the configuration that will be used
    to insert data of the specified type for the selected Anki notes. It also checks
    if a large number of notes are selected and displays a warning message to the user
    if enabled.

    Args:
        browser: The Anki browser object.
        info_title: The title of the information dialog box.
        data_generation_type: The type of data to be generated (e.g., frequency).
        func_type: The type of function to be used for data generation.

    Returns:
        None
    """
    len_notes = len(browser.selectedNotes())

    destination = {"freq_dict": FREQUENCY_FIELD, "jmdict": WORD_TYPE_FIELD}
    DESTINATION = destination.get(dictionary_source)

    showInfo(
        title=info_title,
        text=f"The following configuration will be used for inserting the "
        f"{data_generation_type} for {len_notes} note(s):"
        f"\n\nNote type: {NOTE_TYPE}"
        f"\nVocab: {VOCABULARY_INPUT_FIELD}"
        f"\nDestination field: {DESTINATION}"
        f"\nOverwrite destination field: {OVERWRITE_DESTINATION_FIELD}",
    )

    if len_notes > 200 and DISABLE_WARNINGS is False:
        proceed = askUser(
            title="Multiple Cards Selected",
            text="You have selected a large amount of notes. "
            "Depending on your computer configurations, this could cause your "
            "Anki"
            "instance to crash or it might take a while for all of the "
            "necessary data to load."
            "Would you like to proceed anyway?",
        )

        if proceed:

            pull_data_from_dictionary(browser.selectedNotes(), dictionary_source)
        else:
            showInfo(title="No Card", text="No cards were processsed.")
    else:
        pull_data_from_dictionary(browser.selectedNotes(), dictionary_source)
