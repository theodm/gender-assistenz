def _find_binnenI_pos(word_text):
    # aber: Nur solche I, die kein '-' als vorheriges Zeichen haben,
    # da es sich dann vermutlich um ein zusammengesetztes Nomen,
    # nicht um ein Binnen-I handelt.
    pos = -1
    while True:
        pos = word_text.find('I', pos + 1)

        if pos == -1:
            break

        if pos > 0 and word_text[pos - 1] != '-':
            return pos

    return pos



def is_gendered_word(word_text):
    # Binnen-I
    if _find_binnenI_pos(word_text) != -1:
        return True

    # *
    if "*" in word_text[1:]:
        return True

    # :
    if ":" in word_text[1:]:
        return True

    # (
    if "(" in word_text[1:]:
        return True

    # _
    if "_" in word_text[1:]:
        return True

    return False

def gendered_form_to_feminine_form(word_text):
    if not is_gendered_word(word_text):
        raise Exception(f"Das Wort {word_text} ist nicht in Gender-Form.")

    word_text = word_text.replace("*", "")
    word_text = word_text.replace(":", "")
    word_text = word_text.replace("_", "")
    word_text = word_text.replace("(", "")
    word_text = word_text.replace(")", "")

    binnen_i_pos = _find_binnenI_pos(word_text)

    if binnen_i_pos != -1:
        word_text = word_text[0:binnen_i_pos] + "i" + word_text[(binnen_i_pos+1):]

    return word_text

