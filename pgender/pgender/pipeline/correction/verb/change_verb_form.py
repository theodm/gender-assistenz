import loguru

from pgender.wiktionary.api import find_verb_by_title


def change_verb_form(word, target_number):
    lex_target_verb = find_verb_by_title(word.lemma_)

    res = select_verb_form(
        lex_target_verb,
        word.morph.get("Mood")[0],
        target_number,
        word.morph.get("Person")[0],
        word.morph.get("Tense")[0]
    )

    return res

def select_verb_form(lex_target_verb, target_mood, target_number, target_person, target_tense):
    map_mood = {
        "Ind": "ind"
    }

    map_number = {
        "Sing": "sing",
        "Plur": "plur"
    }

    map_tense = {
        "Pres": "praes"
    }

    key = f"{map_tense[target_tense]}_akt_{map_mood[target_mood]}_{target_person}_{map_number[target_number]}"

    loguru.logger.debug(f"key: {key}")

    return lex_target_verb[key]