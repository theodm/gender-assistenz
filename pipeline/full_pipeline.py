import loguru

from pgender._spacy import spacify_with_coref
from pgender.fiw import find_initial_words
from pgender.ntbg import needs_to_be_gendered
from pgender.pipeline.correction.correction import generate_possible_corrections
from pgender.pipeline.correction.correction_pron import generate_possible_corrections_for_pron


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

    #
    # 2. Schritt: Überprüfung der gefundenen Vorkommen, ob es sich um das generische Maskulinum handelt.
    #
    result = []
    for word in initial_words:
        try:
            ntbg = needs_to_be_gendered(doc, word[0])
        except Exception as e:
            result.append({
                "from": word[0].idx,
                "to": word[0].idx + len(word[0].text),
                "possibleCorrections": [],
                "shouldBeGendered": False,
                "reasonNotGendered": "Fehler: " + str(e),
                "errors": [str(e)]
            })

            continue

        if ntbg[0]:
            #
            # 3. Schritt: Erstellung von Korrekturvorschlägen.
            #
            try:
                def _generate_possible_corrections(word):
                    # ToDo in das Correction Package
                    if word.pos_ == "NOUN":
                        return generate_possible_corrections(word)

                    return generate_possible_corrections_for_pron(word)

                possible_corrections, errors = _generate_possible_corrections(word[0])
            except Exception as e:
                loguru.logger.exception(e)
                result.append({
                    "from": word[0].idx,
                    "to": word[0].idx + len(word[0].text),
                    "possibleCorrections": [],
                    "shouldBeGendered": False,
                    "reasonNotGendered": "Fehler: " + str(e),
                    "errors": [str(e)]
                })

                continue

            result.append({
                "from": word[0].idx,
                "to": word[0].idx + len(word[0].text),
                "possibleCorrections": possible_corrections,
                "shouldBeGendered": ntbg[0],
                "reasonNotGendered": [],
                "errors": errors
            })

            continue

        result.append({
            "from": word[0].idx,
            "to": word[0].idx + len(word[0].text),
            "possibleCorrections": [],
            "shouldBeGendered": ntbg[0],
            "reasonNotGendered": ntbg[1],
            "errors": []
        })

    return result


