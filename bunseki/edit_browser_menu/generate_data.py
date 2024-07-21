# Standard
import sqlite3
from sqlite3 import OperationalError

# Pip
from aqt import mw
from aqt.utils import showInfo, showWarning

# Custom
from ..addon_configs import load_json_config_data
from .anki_fields import preprocess_field
from ..settings.messages.custom_error_messages import (
    CustomErrorMessages as CuErMe,
)

from ..settings.logger.basic_logger import catch_and_log_info, catch_and_log_error

# Reload the configuration data
config_data = load_json_config_data()

FREQUENCY_DICTIONARY = config_data.get("frequency_dict")
JMDICT = config_data.get("jmdict")
NOTE_TYPE = config_data.get("note_type")
VOCABULARY_INPUT_FIELD = config_data.get("vocabulary_input_field")
FREQUENCY_FIELD = config_data.get("frequency_field")
WORD_TYPE_FIELD = config_data.get("word_type_field")
OVERWRITE_DESTINATION_FIELD = True


def check_all_note_types(note_identifiers) -> bool:
    """

    :param note_identifiers:
    :return:
        bool - if all notes are valid, then return true, other return false.
    """

    for identifier in note_identifiers:
        note = mw.col.getNote(identifier)
        note_model_name = note.model()["name"]

        if NOTE_TYPE not in note_model_name:
            try:
                raise CuErMe.NoteTypeMismatch(NOTE_TYPE)
            except CuErMe.NoteTypeMismatch as e:
                showWarning(str(e))
                catch_and_log_error(error=e, custom_message=e)
            return False

        elif VOCABULARY_INPUT_FIELD not in note:
            try:
                raise CuErMe.VocabFieldNotFound(VOCABULARY_INPUT_FIELD)
            except CuErMe.VocabFieldNotFound as e:
                showWarning(str(e))
                catch_and_log_error(error=e, custom_message=e)
            return False

        elif FREQUENCY_FIELD not in note:
            try:
                raise CuErMe.DestinationFieldNotFound(FREQUENCY_FIELD)
            except CuErMe.DestinationFieldNotFound as e:
                showWarning(str(e))
                catch_and_log_error(error=e, custom_message=e)
            return False

        elif note[FREQUENCY_FIELD] and not OVERWRITE_DESTINATION_FIELD:
            try:
                raise CuErMe.VocabFieldNotEmpty(VOCABULARY_INPUT_FIELD)
            except CuErMe.VocabFieldNotEmpty as e:
                showWarning(str(e))
                catch_and_log_error(error=e, custom_message=e)
            return False

    return True


def pull_data_from_dictionary(note_identifiers, dictionary_source: str):
    """
    Process the given note identifiers to add frequency data.

    This function updates notes with frequency data by fetching the relevant data from a
    pre-defined database. It shows progress and handles errors appropriately.

    :param note_identifiers: List of note identifiers to process.
    :return: None
    """
    load_json_config_data()
    d = {"freq_dict": FREQUENCY_DICTIONARY, "jmdict": JMDICT}

    frequency_database = sqlite3.connect(d.get(dictionary_source))

    i = 0
    total_notes = len(note_identifiers)
    all_true = check_all_note_types(note_identifiers)

    if all_true:
        mw.progress.start(label="Updating vocabulary frequency...", max=total_notes)

        catch_and_log_info(custom_message="start generating vocabulary frequency...")
        SOURCE = VOCABULARY_INPUT_FIELD

        destination = {"freq_dict": FREQUENCY_FIELD, "jmdict": WORD_TYPE_FIELD}
        DESTINATION = destination.get(dictionary_source)

        for identifier in note_identifiers:
            note = mw.col.getNote(identifier)

            try:
                i += 1

                vocab_query = preprocess_field(note[SOURCE])

                if vocab_query != "":
                    # Look for word in the frequency dictionary
                    sql_query_freq_dict = f"""SELECT freq FROM freq_dict 
                                    WHERE expression ='{vocab_query}';"""

                    sql_query_jmdict = f"""select Meaning from jmdict 
                                        where expression='{vocab_query}';"""

                    query_dict = {
                        "freq_dict": sql_query_freq_dict,
                        "jmdict": sql_query_jmdict,
                    }

                    try:

                        cursor = frequency_database.cursor()
                        cursor.execute(query_dict.get(dictionary_source))
                        single_result = cursor.fetchone()

                        if single_result is not None:
                            note[DESTINATION] = single_result[0]
                        else:
                            note[DESTINATION] = "UNK"

                    except OperationalError as e:

                        catch_and_log_error(
                            error=e,
                            custom_message=f"There is a problem with the database",
                        )
            except Exception as e:
                catch_and_log_error(
                    error=e,
                    custom_message=f"There is a problem with the database",
                )

            note.flush()

            # Update progress
            mw.progress.update(value=i)

        mw.progress.finish()
        showInfo(f"Processed {total_notes} notes.")
        frequency_database.close()
        mw.reset()
