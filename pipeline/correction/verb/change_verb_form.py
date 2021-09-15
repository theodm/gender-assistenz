import loguru

from wiktionary.api import find_verb_by_title, find_verb_by_any_form


def change_verb_form(word, target_number):
    lex_target_verb = find_verb_by_title(word.lemma_)

    if not lex_target_verb:
        lex_target_verb = find_verb_by_any_form(word.text)

    if not lex_target_verb:
        loguru.logger.info("lex_target_verb not found: " + word.text)

        raise Exception(f"Das Verb konnte im Lexikon nicht gefunden werden: {word.text}")

    res = select_verb_form(
        lex_target_verb,
        word.morph.get("Mood")[0],
        target_number,
        word.morph.get("Person")[0],
        word.morph.get("Tense")[0]
    )

    return res

def select_verb_form(lex_target_verb, target_mood, target_number, target_person, target_tense):
    map_number = {
        "Sing": "sing",
        "Plur": "plur"
    }

    map_tense = {
        "Pres": "praes",
        "Past": "praet"
    }

    map_mood = {
        "Ind": "ind",
        "Sub": "konj1" if target_tense == "Pres" else "konj2"
    }

    key = f"{map_tense[target_tense]}_akt_{map_mood[target_mood]}_{target_person}_{map_number[target_number]}"

    loguru.logger.debug(f"key: {key}")

    return lex_target_verb[key]

