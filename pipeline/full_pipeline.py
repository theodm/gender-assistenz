import loguru

from _spacy import spacify_with_coref
from fiw import find_initial_words
from ntbg import needs_to_be_gendered
from pipeline.correction.correction import generate_possible_corrections
from pipeline.correction.correction_pron import generate_possible_corrections_for_pron
from wordlib import follow_parent_dep


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
                "reasonNotGendered": [("", "Fehler: " + str(e))],
                "errors": [str(e)]
            })

            continue

        if ntbg[0]:
            #
            # 2b. Schritt: Wenn es sich um ein Pronomen handelt, welches bereits durch die Korrektur
            # eines Nomens korrigiert wird, dann muss es selbst keine Korrekturvorschläge enthalten.
            # Es wird im Ergebnis indirekt über das Nomen gegendert. Das ganze kann aber nicht
            # in die needs_to_be_gendered-Methode eingebaut werden, da dort die tatsächliche
            #
            # Bsp.: Fortschritt wird erreicht, wenn jeder volljährige Bürger, der eine Meinung hat, wählen geht.
            #                                                         ______  ___
            #
            # => "der" darf hierbei selbst nicht als Korrekturvorschlag auftauchen.
            #
            try:
                # Das Wort ist ein Pronomen, wenn es sich nicht um eine Nomen handelt.
                if word[0].pos_ != "NOUN":
                    exceptional_not_gendered = False

                    #
                    # Fall 1: Das Pronomen ist Teil der Relativklausel.
                    #
                    # Bsp.: Fortschritt wird erreicht, wenn jeder volljährige Bürger, der eine Meinung hat, wählen geht.
                    #
                    parent_of_subject = follow_parent_dep(word[0], "sb")
                    if parent_of_subject:
                        parent_of_relative_clause = follow_parent_dep(parent_of_subject, "rc")

                        if parent_of_relative_clause:
                            exceptional_not_gendered = True

                    if exceptional_not_gendered:
                        result.append({
                            "from": word[0].idx,
                            "to": word[0].idx + len(word[0].text),
                            "possibleCorrections": [],
                            "shouldBeGendered": False,
                            "reasonNotGendered": [("", "Das Vorkommen wird nicht verändert, da es durch ein anderes Vorkommen bereits abgedeckt wird.")],
                            "errors": []
                        })

                        continue
            except Exception as e:
                loguru.logger.error(f"Das Wort {word[0].text} wurde nicht erfolgreich verarbeitet.")
                loguru.logger.error(e)

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
                    "reasonNotGendered": ["Fehler: " + str(e)],
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


