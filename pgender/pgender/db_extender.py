from charsplit import Splitter

from pgender.wiktionary.api import find_by_any_form, find_by_title

splitter = Splitter()

def find_in_db(word, search_every_form=False):
    lemma = word
    if not isinstance(word, str):
        lemma = word.lemma_

    if search_every_form:
        lemma_in_db = find_by_any_form(lemma)
    else:
        lemma_in_db = find_by_title(lemma)

    if not lemma_in_db:
        return None

    return lemma_in_db


def find_in_db_and_convert(iword):
    if not isinstance(iword, str):
        iword = iword.lemma_

    word = find_in_db(iword, False)

    if word:
        return word

    word = find_in_db(iword, True)

    if word:
        return word

    splits = splitter.split_compound(iword)

    if not splits:
        return None

    last_part = splits[0][-1]

    last_part_word = find_in_db(last_part, False)

    if not last_part_word:
        return None

    return {
        "title": splits[0][-2] + last_part_word["title"].lower(),
        "genus": last_part_word["genus"],
        "nominativ_singular": splits[0][-2] + last_part_word["nominativ_singular"].lower(),
        "nominativ_plural": splits[0][-2] + last_part_word["nominativ_plural"].lower(),
        "genitiv_singular": splits[0][-2] + last_part_word["genitiv_singular"].lower(),
        "genitiv_plural": splits[0][-2] + last_part_word["genitiv_plural"].lower(),
        "dativ_singular": splits[0][-2] + last_part_word["dativ_singular"].lower(),
        "dativ_plural": splits[0][-2] + last_part_word["dativ_plural"].lower(),
        "akkusativ_singular": splits[0][-2] + last_part_word["akkusativ_singular"].lower(),
        "akkusativ_plural": splits[0][-2] + last_part_word["akkusativ_plural"].lower(),
        "maennliche_formen": [splits[0][-2] + x.lower() for x in last_part_word["maennliche_formen"]] if last_part_word["maennliche_formen"] else None,
        "weibliche_formen": [splits[0][-2] + x.lower() for x in last_part_word["weibliche_formen"]] if last_part_word["weibliche_formen"] else None,
    }

def feminine_noun_forms_and_convert(word):
    if not isinstance(word, str):
        word = word.lemma_

    lemma_in_db = find_in_db_and_convert(word)

    if not lemma_in_db:
        return []

    feminine_forms_in_db = lemma_in_db["weibliche_formen"]

    if not feminine_forms_in_db:
        return []

    feminine_forms = [find_in_db_and_convert(f) for f in feminine_forms_in_db]

    if not feminine_forms:
        return []

    return feminine_forms