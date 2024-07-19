# Standard
# None

# Pip
from aqt.utils import showInfo, askUser
from aqt.browser import Browser

# Custom
from .config import reload_json_config
from .generate_data import bulk_generate_word_type_fg, bulk_generate_vocab_frequency

config_data = reload_json_config()

FREQUENCY_DICTIONARY = config_data.get("frequency_dict")
VOCABULARY_DICTIONARY = config_data.get("vocabulary_dict")
NOTE_TYPE = config_data.get("note_type")
VOCABULARY_INPUT_FIELD = config_data.get("vocabulary_input_field")
FREQUENCY_FIELD = config_data.get("frequency_field")
WORD_TYPE_FIELD = config_data.get("word_type_field")
OVERWRITE_DESTINATION_FIELD = True


def on_bulk_generate_vocab(browser: Browser) -> None:
    len_notes = len(browser.selectedNotes())

    showInfo(
        title="Bulk Generate Frequency",
        text=f"The following configuration will be used for inserting the "
        f"frequency data for {len_notes} note(s):"
        f"\n\nNote type: {NOTE_TYPE}"
        f"\nVocab: {VOCABULARY_INPUT_FIELD}"
        f"\nDestination field: {FREQUENCY_FIELD}"
        f"\nOverwrite destination field: {OVERWRITE_DESTINATION_FIELD}",
    )

    if len_notes > 200:
        proceed = askUser(
            title="Multiple Cards Selected",
            text="You have selected a large amount of notes. "
            "Depending on your system, this could cause your Anki "
            "instance to crash. "
            "Would you like to proceed anyway?",
        )

        if proceed:
            bulk_generate_vocab_frequency(browser.selectedNotes())
        else:
            showInfo(title="No Card", text="No cards were processsed.")
    else:
        bulk_generate_vocab_frequency(browser.selectedNotes())


def on_generate_word_type(browser: Browser):
    len_notes = len(browser.selectedNotes())

    showInfo(
        title="Word Type",
        text=f"The following configuration will be used for inserting the "
        f"word type data for {len_notes} note(s):"
        f"\n\nNote type: {NOTE_TYPE}"
        f"\nVocab: {VOCABULARY_INPUT_FIELD}"
        f"\nDestination field: {FREQUENCY_FIELD}"
        f"\nOverwrite destination field: {OVERWRITE_DESTINATION_FIELD}",
    )

    if len_notes > 200:
        proceed = askUser(
            title="Multiple Cards Selected",
            text="You have selected a large amount of notes. "
            "Depending on your computer configures, this could cause your Anki "
            "instance to crash. "
            "Would you like to proceed anyway?",
        )

        if proceed:
            bulk_generate_word_type_fg(browser.selectedNotes())
        else:
            showInfo(title="No Card", text="No cards were processsed.")
    else:

        bulk_generate_word_type_fg(browser.selectedNotes())


def generate_information_for_selected_cards():
    pass
