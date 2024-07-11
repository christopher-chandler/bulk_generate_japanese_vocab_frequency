# Standard 
# None 

# Pip
# None 

# Custom 
# None 

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


if __name__ == '__main__':
    pass
