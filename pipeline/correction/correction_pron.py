import loguru

from pipeline.correction.correction import preserve_case, TYPE_DET, TYPE_NOUN, TYPE_VERB
from pipeline.correction.pron_art.select_pron_form import select_pron_art_form
from pipeline.correction.verb.change_verb_form import change_verb_form
from wordlib2 import find_art_and_pron, find_verb


def transform_pron_base(
        #
        # Wort, das transformiert werden soll.
        # Bsp.: Er
        #
        word,

        #
        # In welchen Numerus soll das Pronomen nach der Transformation stehen?
        #
        target_number,

        #
        # In welchem grammatischen Geschlecht soll das Pronomen bzw. die zugehörigen Wörter nach der Transformation stehen?
        #
        target_gender,

        #
        # Zusätzliche Methode, mit der neue entstehende Pronomen noch nachbearbeitet werden kann.
        #
        transform_pron,
):
    result = []

    #
    # Das Pronomen selbst verändern.
    #
    new_pron = select_pron_art_form(word, target_gender, target_number)

    if not new_pron:
        # Pronomen kann nicht umgewandelt werden, dann brauchen wir auch sonst nichts mehr versuchen.
        return []

    new_pron = preserve_case(new_pron, word.text)
    new_pron = transform_pron(new_pron, word.text)

    result.append({
        "text": word.text,
        "from": word.idx,
        "to": word.idx + len(word.text) + (1 if len(new_pron) == 0 else 0),
        "type": TYPE_NOUN,
        "replace_with": new_pron
    })

    #
    # Artikel und Pronomen, die sich auf das substituirende Pronomen beziehen, modifizieren:
    # Er, dessen Bein gebrochen war, geht ein Eis essen. -> Er*Sie, dessen/deren Bein gebrochen war, geht ein Eis essen.
    #     ______                                                    ____________
    #
    for pron in find_art_and_pron(word):
        new_pron = select_pron_art_form(pron, target_gender, target_number)

        if not new_pron:
            loguru.logger.debug(f"{pron.text} wurde nicht umgewandelt.")
            continue

        new_pron = preserve_case(new_pron, pron.text)
        new_pron = transform_pron(new_pron, pron.text)

        result.append({
            "text": pron.text,
            "from": pron.idx,
            "to": pron.idx + len(pron.text) + (1 if len(new_pron) == 0 else 0),
            "type": TYPE_DET,
            "replace_with": new_pron
        })

    #
    # Wenn Singular -> Plural, dann muss auch das übergeordnete Verb des Satzes,
    # in dem das Nomen verwendet wird, geändert werden.
    #
    # Er geht ein Eis essen. -> Sie gehen ein Eis essen.
    #             ____                                     _____
    #
    if target_number == "Plur":
        verbs = find_verb(word)

        for verb in verbs:
            corrected = change_verb_form(verb, "Plur")
            corrected = preserve_case(corrected, verb.text)

            result.append({
                "text": verb.text,
                "from": verb.idx,
                "to": verb.idx + len(verb.text),
                "type": TYPE_VERB,
                "replace_with": corrected
            })

    return result


#
# Erstelle Korrekturvorschläge für substituirende Pronomen, also solche, die
# anstelle eines Nomens stehen.
#
# Bsp.: Er geht ein Eis essen.
#       __
#
def generate_possible_corrections_for_pron(word):
    if not word.morph.get("Number"):
        # ToDo: Fehler zurückgeben?
        return [], [f"Für das Wort {word.text} konnten keine Korrekturen erstellt werden, da es nicht die erforderlichen morphologischen Eigenschaften erhält."]

    #
    # Für Plural-Vorkomnisse macht eine Umwandlung keinen Sinn, hier unterscheiden sich Maskulinum und Femininum nicht. (wir, ihr, sie, ...)
    #
    if word.morph.get("Number")[0] == "Plur":
        return None, []

    errors = []
    possible_corrections = []

    try:
        def tranform_pron(new, old):
            # Bsp.: Er?Sie
            #
            # Durch was das ? ersetzt wird, kann wieder durch
            # den Benutzer entschieden werden.
            return old + "?" + new

        possible_corrections.append({
            "type": "*",
            "changes": transform_pron_base(word, "Sing", "Fem", transform_pron=tranform_pron)
        })
    except Exception as e:
        errors.append(f"Konnte Korrekturvorschlag '*' nicht erstellen: {e}")
        loguru.logger.info(f"Konnte Korrekturvorschlag '*' nicht erstellen: {e}")
        loguru.logger.exception(e)

    try:
        def tranform_pron(new, old):
            return new

        possible_corrections.append({
            "type": "PLURAL_*",
            "changes": transform_pron_base(word, "Plur", "Fem", transform_pron=tranform_pron)
        })
    except Exception as e:
        errors.append(f"Konnte Korrekturvorschlag 'PLURAL_*' nicht erstellen: {e}")
        loguru.logger.info(f"Konnte Korrekturvorschlag 'PLURAL_*' nicht erstellen: {e}")
        loguru.logger.exception(e)


    return possible_corrections, errors
  #  return generate_possible_corrections_singular(word)