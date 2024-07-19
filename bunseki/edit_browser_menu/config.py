# Standard
# None

# Pip
from aqt import mw

# Custom
# None

# Base values are empty
FREQUENCY_DICTIONARY = ""
VOCABULARY_DICTIONARY = ""
NOTE_TYPE = ""
VOCABULARY_INPUT_FIELD = ""
FREQUENCY_FIELD = ""
WORD_TYPE_FIELD = ""
OVERWRITE_DESTINATION_FIELD = True


def reload_json_config() -> dict:
    """
    Reload the configuration settings from the Anki add-on manager.

    This function fetches the configuration settings for the add-on and updates
    global variables with the new values. It returns a dictionary containing the
    updated configuration field data.

    :return:
        config_field_data(dict): A dictionary containing the configuration field data with keys:
              'vocabulary_dict', 'frequency_dict', 'note_type', 'vocabulary_input_field',
              'frequency_field', 'word_type_field', 'overwrite_destination'.
    """
    # Global, so that the values can be overwritten
    global FREQUENCY_DICTIONARY
    global VOCABULARY_DICTIONARY
    global NOTE_TYPE
    global VOCABULARY_INPUT_FIELD
    global FREQUENCY_FIELD
    global WORD_TYPE_FIELD
    global OVERWRITE_DESTINATION_FIELD

    # Fetch data from the config file
    config = mw.addonManager.getConfig(__name__)
    VOCABULARY_DICTIONARY = config["0_jm_dict"]
    FREQUENCY_DICTIONARY = config["0_freq_dict"]
    NOTE_TYPE = config["01_note_type"]
    VOCABULARY_INPUT_FIELD = config["02_vocab_input_field"]
    FREQUENCY_FIELD = config["03_frequency_output_field"]
    WORD_TYPE_FIELD = config["03_word_type_output_field"]
    OVERWRITE_DESTINATION_FIELD = config["04_overwrite_destination_field"]

    # The new values inputted by the user
    config_field_data = {
        "vocabulary_dict": VOCABULARY_DICTIONARY,
        "frequency_dict": FREQUENCY_DICTIONARY,
        "note_type": NOTE_TYPE,
        "vocabulary_input_field": VOCABULARY_INPUT_FIELD,
        "frequency_field": FREQUENCY_FIELD,
        "word_type_field": WORD_TYPE_FIELD,
        "overwrite_destination": OVERWRITE_DESTINATION_FIELD,
    }

    return config_field_data
