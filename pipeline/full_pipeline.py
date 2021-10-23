import loguru

from _spacy import spacify_with_coref
from fiw import find_initial_words
from ntbg import needs_to_be_gendered
from pipeline.correction.correction2 import generate_possible_corrections
from wordlib import follow_parent_dep, get_coref_words_in_sentence


def full_pipeline(text):
    #
    # Zunächst führen wir SpacY aus um Grammatikinformationen initial
    # zu erhalten.
    #
    doc = spacify_with_coref(text)

    #
    # 1. Schritt: Suche nach allen maskulinen Formen
    #
    initial_words = find_initial_words(doc)

    result = []

    while initial_words:
        word = initial_words.pop()

        try:
            #
            # 2. Schritt: Überprüfung der gefundenen Vorkommen, ob es sich um das generische Maskulinum handelt.
            #
            ntbg = needs_to_be_gendered(doc, word[0])
        except Exception as e:
            loguru.logger.error(f"Es konnte für das Wort {word[0].text} nicht festgestellt werden, ob es einer Änderung bedarf.")

            result.append({
                "word": word[0].text,
                "from": word[0].idx,
                "to": word[0].idx + len(word[0].text),
                "possibleCorrections": [],
                "shouldBeGendered": False,
                "reasonNotGendered": [("", "Fehler: " + str(e))],
                "errors": [str(e)]
            })

            continue

        #
        # Es handelt sich nicht um generisches Maskulinum. Wir geben jedoch das
        # Vorkommen für Debugging-Zwecke per API weiter.
        #
        if not ntbg[0]:
            result.append({
                "word": word[0].text,
                "from": word[0].idx,
                "to": word[0].idx + len(word[0].text),
                "possibleCorrections": [],
                "shouldBeGendered": False,
                "reasonNotGendered": ntbg[1],
                "errors": []
            })

            continue

        #
        # 3. Schritt: Erstellung von Korrekturvorschlägen.
        #
        try:
            possible_corrections, errors = generate_possible_corrections(get_coref_words_in_sentence(doc, word[0]))

            result.append({
                "word": word[0].text,
                "from": word[0].idx,
                "to": word[0].idx + len(word[0].text),
                "possibleCorrections": possible_corrections,
                "shouldBeGendered": ntbg[0],
                "reasonNotGendered": [],
                "errors": errors
            })
        except Exception as e:
            loguru.logger.exception(e)

            result.append({
                "word": word[0].text,
                "from": word[0].idx,
                "to": word[0].idx + len(word[0].text),
                "possibleCorrections": [],
                "shouldBeGendered": True,
                "reasonNotGendered": [],
                "errors": [str(e)]
            })



    return sorted(result, key=lambda x: x["from"])


