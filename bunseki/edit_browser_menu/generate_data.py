# Standard
import sqlite3
from sqlite3 import OperationalError

# Pip
from aqt import mw
from aqt.utils import showInfo, showWarning

# Custom
from .config import reload_json_config
from .anki_fields import preprocess_field
from ..settings.messages.custom_error_messages import (
    CustomErrorMessages as CuErMe,
    CustomErrorMessages,
)

from ..settings.logger.basic_logger import catch_and_log_info, catch_and_log_error

# Reload the configuration data
config_data = reload_json_config()

FREQUENCY_DICTIONARY = config_data.get("frequency_dict")
VOCABULARY_DICTIONARY = config_data.get("vocabulary_dict")
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
                raise CustomErrorMessages.NoteTypeMismatch(NOTE_TYPE)
            except CustomErrorMessages.NoteTypeMismatch as e:
                showWarning(str(e))
                catch_and_log_error(error=e, custom_message=e)
            return False

        elif VOCABULARY_INPUT_FIELD not in note:
            try:
                raise CustomErrorMessages.VocabFieldNotFound(VOCABULARY_INPUT_FIELD)
            except CustomErrorMessages.VocabFieldNotFound as e:
                showWarning(str(e))
                catch_and_log_error(error=e, custom_message=e)
            return False

        elif FREQUENCY_FIELD not in note:
            try:
                raise CustomErrorMessages.DestinationFieldNotFound(FREQUENCY_FIELD)
            except CustomErrorMessages.DestinationFieldNotFound as e:
                showWarning(str(e))
                catch_and_log_error(error=e, custom_message=e)
            return False

        elif note[FREQUENCY_FIELD] and not OVERWRITE_DESTINATION_FIELD:
            try:
                raise CustomErrorMessages.VocabFieldNotEmpty(VOCABULARY_INPUT_FIELD)
            except CustomErrorMessages.VocabFieldNotEmpty as e:
                showWarning(str(e))
                catch_and_log_error(error=e, custom_message=e)
            return False

    return True


def bulk_generate_vocab_frequency(note_identifiers):
    """
    Process the given note identifiers to add frequency data.

    This function updates notes with frequency data by fetching the relevant data from a
    pre-defined database. It shows progress and handles errors appropriately.

    :param note_identifiers: List of note identifiers to process.
    :return: None
    """
    reload_json_config()
    frequency_database = sqlite3.connect(FREQUENCY_DICTIONARY)

    i = 0
    total_notes = len(note_identifiers)

    all_true = check_all_note_types(note_identifiers)

    if all_true:
        mw.progress.start(label="Updating vocabulary frequency...", max=total_notes)

        for identifier in note_identifiers:
            note = mw.col.getNote(identifier)
            SOURCE = VOCABULARY_INPUT_FIELD
            DESTINATION = FREQUENCY_FIELD

            try:
                i += 1

                vocab_query = preprocess_field(note[SOURCE])

                if vocab_query != "":
                    sql_query = f"""SELECT freq FROM freq_dict 
                                    WHERE expression ='{vocab_query}';"""
                    try:
                        cursor = frequency_database.cursor()
                        cursor.execute(sql_query)
                        single_result = cursor.fetchone()
                        if single_result is not None:
                            note[DESTINATION] = single_result[0]
                        else:
                            note[DESTINATION] = "UNK"

                    except OperationalError:
                        pass
            except:
                raise

            note.flush()

            # Update progress
            mw.progress.update(value=i)

        mw.progress.finish()
        showInfo(f"Processed {total_notes} notes.")
        frequency_database.close()
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
