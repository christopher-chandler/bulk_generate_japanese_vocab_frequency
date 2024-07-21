# Standard
# None

# Pip
from aqt import mw

# Custom
# None

# Base values are empty
FREQUENCY_DICTIONARY = ""
JMDICT = ""
NOTE_TYPE = ""
VOCABULARY_INPUT_FIELD = ""
FREQUENCY_FIELD = ""
WORD_TYPE_FIELD = ""
OVERWRITE_DESTINATION_FIELD = True
DEBUG = True
DISABLE_WARNINGS = False


def load_json_config_data() -> dict:
    """
    Reload the configuration settings from the Anki add-on manager.

    This function fetches the configuration settings for the add-on and updates
    global variables with the new values. It returns a dictionary containing the
    updated configuration field data.

    :return:
        config_field_data(dict): A dictionary containing the configuration field
    """
    # Global, so that the values can be overwritten
    global FREQUENCY_DICTIONARY
    global JMDICT
    global NOTE_TYPE
    global VOCABULARY_INPUT_FIELD
    global FREQUENCY_FIELD
    global WORD_TYPE_FIELD
    global OVERWRITE_DESTINATION_FIELD
    global DEBUG
    global DISABLE_WARNINGS

    # Fetch data from the config file
    config = mw.addonManager.getConfig(__name__)
    JMDICT = config["0_jm_dict"]
    FREQUENCY_DICTIONARY = config["0_freq_dict"]
    NOTE_TYPE = config["01_note_type"]
    VOCABULARY_INPUT_FIELD = config["02_vocab_input_field"]
    FREQUENCY_FIELD = config["03_frequency_output_field"]
    WORD_TYPE_FIELD = config["03_word_type_output_field"]
    OVERWRITE_DESTINATION_FIELD = config["04_overwrite_destination_field"]
    DEBUG = config["05_debug"]
    DISABLE_WARNINGS = config["06_disable_warnings"]

    # The new values inputted by the user
    config_field_data = {
        "jmdict": JMDICT,
        "freq_dict": FREQUENCY_DICTIONARY,
        "note_type": NOTE_TYPE,
        "vocabulary_input_field": VOCABULARY_INPUT_FIELD,
        "frequency_field": FREQUENCY_FIELD,
        "word_type_field": WORD_TYPE_FIELD,
        "overwrite_destination": OVERWRITE_DESTINATION_FIELD,
        "debug": DEBUG,
        "disable_warnings": DISABLE_WARNINGS,
    }

    return config_field_data
