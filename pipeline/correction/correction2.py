from itertools import chain

import loguru

from db_extender import feminine_noun_forms_and_convert
from pipeline.correction.adj.change_adj_form import change_adj_form
from pipeline.correction.noun.select_noun_form import select_noun_form
from pipeline.correction.pposs.change_pposs_form import select_pposs_form
from pipeline.correction.pron_art.select_pron_form import select_pron_art_form
from pipeline.correction.verb.change_verb_form import change_verb_form
from wordlib import follow_parent_dep, follow_child_dep_single_or_none
from wordlib2 import find_art_and_pron, find_verb, find_adj

TYPE_NOUN = "NOUN"
TYPE_CONJ = "CONJ"
TYPE_DET = "DET"
TYPE_VERB = "VERB"
TYPE_ADJ = "ADJ"

def preserve_case(new_str, old_str):
    if old_str[0:1].isupper():
        return new_str[0:1].upper() + "" + new_str[1:]

    return new_str

def flatten(listOfLists):
    # ToDo: sorted gehört hier nicht hin
    return sorted(list(chain.from_iterable([x for x in listOfLists if x is not None])), key=lambda x: x["from"])


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
    if word.morph.get("Poss") and word.morph.get("Poss")[0]:
        new_pron = select_pposs_form(word, target_gender, target_number)
    else:
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
        "type": TYPE_DET,
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

    for x in result:
        del x['text']

    return result


def transform_noun(
        #
        # Wort, das transformiert werden soll.
        # Bsp.: Bäcker
        #
        word,

        #
        # Lexikon-Eintrag des neuen Nomens, mit dem das alte Nomen ersetzt werden soll.
        # Also in der Regel die weibliche Form des Wortes.
        # Bsp.: Bäcker -> Bäckerin
        #
        lex_new_word,

        #
        # In welchen Numerus soll das Nomen nach der Transformation stehen?
        #
        target_number,

        #
        # In welchem Sexus soll das Nomen bzw. die zugehörigen Wörter nach der Transformation stehen?
        #
        target_gender,


        #
        # Zusätzliche Methode, mit der das neue entstehende Nomen noch nachbearbeitet werden kann.
        #
        transform_noun,

        #
        # Zusätzliche Methode, mit der neue entstehende Artikel noch nachbearbeitet werden kann.
        #
        transform_det,

        #
        # Zusätzliche Methode, mit der neue entstehende Pronomen noch nachbearbeitet werden kann.
        #
        transform_pron,

):
    result = []

    # Steht das bestehende Wort im Plural oder im Singular?
    existing_number = word.morph.get("Number")[0]
    # In welchem Kasus steht das bestehende Wort?
    existing_case = word.morph.get("Case")[0]

    #
    # Wenn Singular -> Singular oder Singular -> Plural umgewandelt wird, dann müssen wir
    # Artikel und Adjektive modifizieren.
    #
    if existing_number == "Sing":
        #
        # Artikel und Pronomen modifizieren:
        # Der Schüler geht ein Eis essen. -> Die Schüler*in geht ein Eis essen.
        # ___                                ___
        #
        # Der Schüler, dessen Bein gebrochen war, ging ein Eis essen.
        #              ______
        #
        for pron in find_art_and_pron(word):
            new_pron = select_pron_art_form(pron, target_gender, target_number)

            if not new_pron and not len(new_pron) == 0:
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
        # Der Schüler geht ein Eis essen. -> Die Schüler*innen gehen ein Eis essen.
        #             ____                                     _____
        #
        # Außerdem muss das Adjektiv geändert werden.
        #
        # Der schnelle Schüler geht ein Eis essen. -> Die schnellen Schüler*innen gehen ein Eis essen.
        #     ________                                    _________
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

            adjs = find_adj(word)

            for adj in adjs:
                corrected = change_adj_form(adj, target_gender, "Plur")
                corrected = preserve_case(corrected, adj.text)

                result.append({
                    "text": adj.text,
                    "from": adj.idx,
                    "to": adj.idx + len(adj.text) + (1 if len(corrected) == 0 else 0),
                    "type": TYPE_ADJ,
                    "replace_with": corrected
                })

    #
    # Das Nomen selbst muss verändert werden. Dabei muss der richtige Kasus und
    # der richtige Numerus ausgewählt werden. Diese sind genau die, in denen auch
    # das ursprüngliche Wort steht.
    #
    new_noun = select_noun_form(lex_new_word, existing_case, target_number)

    result.append({
        "text": word.text,
        "from": word.idx,
        "to": word.idx + len(word.text),
        "type": TYPE_NOUN,
        "replace_with": transform_noun(new_noun)
    })

    return preserve_case_over_changes(result)

def preserve_case_over_changes(changes):
    changes.sort(key=lambda x: x["from"])

    if len(changes) >= 2 and len(changes[0]["replace_with"]) == 0 and changes[0]["text"][0].isupper():
        changes[1]["replace_with"] = changes[1]["replace_with"][0:1].upper() + "" + changes[1]["replace_with"][1:]

    for x in changes:
        del x['text']

    return changes




def transform_noun_or_pron(word, target_number, target_gender, noun_transformer, det_transformer, pron_transformer):
    if word.pos_ == "NOUN":
        fnf = feminine_noun_forms_and_convert(word)

        return transform_noun(word, fnf[0], target_number, target_gender, noun_transformer, det_transformer, pron_transformer)
    elif word.pos_ == "PRON" or word.pos_ == "DET":
        #
        # Für Plural-Vorkomnisse macht eine Umwandlung keinen Sinn, hier unterscheiden sich Maskulinum und Femininum nicht. (wir, ihr, sie, ...)
        #
        if word.morph.get("Number")[0] == "Plur":
            return None

        return transform_pron_base(word, target_number, target_gender, transform_pron=det_transformer)
    else:
        # ToDo: Ausgabe!
        return None


def nothing(x, y):
    return x

def generate_possible_corrections(coref_words):
    errors = []
    possible_corrections = []

    # for w in coref_words:
    #     if not w.morph.get("Number"):
    #         return [], [f"Für das Wort `{w.text}` konnten keine Korrekturen erstellt werden, da es die erforderliche morphologische Eigenschaft `Number` nicht enthält."]

    have_morph_number = any(w.morph.get("Number") and w.morph.get("Number")[0] for w in coref_words)

    if not have_morph_number:
        return [], [f"Für die Wörter `{str([x.text for x in coref_words])}` konnten keine Korrekturen erstellt werden, da mindestens ein Wort die erforderliche morphologische Eigenschaft `Number` nicht enthält."]

    are_plural = any(w.morph.get("Number") and w.morph.get("Number")[0] and w.morph.get("Number")[0] == "Plur" for w in coref_words)
    are_singular = any(w.morph.get("Number") and w.morph.get("Number")[0] and w.morph.get("Number")[0] == "Sing" for w in coref_words)

    if are_plural:
        #
        # Für Pluralvorkommen bieten wir hier die *_:/-Formen an.
        #
        # Bsp.: Die Schüler gehen ein Eis essen.
        #       Die Schülerinnen gehen ein Eis essen.
        #
        try:
            #
            # Wandelt die feminine Form eines Nomens in die geschlechtsneutrale
            # Form mit *_:/ um.
            #
            # Bsp.: Schülerinnen -> Schüler*innen
            #
            def noun_transformer(word_str):
                # Dabei arbeiten wir mit dem Platzhalter ?Innen bzw. ?In. Auf der Oberfläche
                # kann diese Form dann bequem in die vom Benutzer gewünschte Form,
                # bspsw. :innen, /innen, *innen, Innen wählen.
                if word_str.endswith("innen"):
                    return word_str[0:-5] + "?Innen"

                return word_str

            #
            # Wir stoßen eine Konvertierung der gefundenen Nomen in Plural und die feminine Form an. Das feminine Nomen wandeln
            # wir mithilfe der noun_transformer-Methode in eine geschlechterneutrale Form um. Ansonsten ändert sich nichts.
            #
            changes = flatten([transform_noun_or_pron(w, "Plur", "Fem", noun_transformer, nothing, nothing) for w in coref_words])

            possible_corrections.append({
                "type": "*",
                "changes": changes
            })
        except Exception as e:
            errors.append(f"Konnte Korrekturvorschlag '*' nicht erstellen: {e}")
            loguru.logger.info(f"Konnte Korrekturvorschlag '*' nicht erstellen: {e}")
            loguru.logger.exception(e)

        try:
            changes = []

            for word in coref_words:
                #
                # Wenn das Wort in einer Konjunktionskette ist, dann gibt
                # diese Methode an, ob das Wort nach der Konkunktion (und, oder)
                # steht. In diesem Fall wird das Konjunktionswort zurückgegeben.
                #
                # bsp.:
                # Schüler und Lehrer -> Rückgabe: "und"
                #             ______
                # Schüler und Lehrer -> Rückgabe: False
                # _______
                #
                def conjunction_word_before():
                    pand = follow_parent_dep(word, "cj")

                    # https://universaldependencies.org/u/pos/CCONJ.html
                    # Koordinierende Konjunktion: z.B.: und, oder
                    if pand and pand.pos_ == "CCONJ":
                        return pand

                    return False

                #
                # Wenn das Wort in einer Konjunktionskette ist, dann gibt
                # diese Methode an, ob das Wort vor der Konjunktion (und, oder)
                # steht.
                #
                # bsp.:
                # Schüler und Lehrer -> Rückgabe: False
                #             ______
                # Schüler und Lehrer -> Rückgabe: True
                # _______
                #
                def conjunction_word_after():
                    next = word

                    while True:
                        if follow_child_dep_single_or_none(next, "cd"):
                            return True

                        next = follow_child_dep_single_or_none(word, "cd")

                        if not next:
                            return False

                #
                # Wir bieten als Korrektur für Pluralformen die Form an,
                # die beide Wortformen explizit nennt.
                #
                def noun_transformer(word_str):
                    #
                    # Wort ist Teil einer Konjunktionskette, dann
                    # korrigieren wir nur mit Komma, da sich mehrere
                    # und-Verknüpfungen meist nicht gut anhören.
                    #
                    if conjunction_word_after():
                        return word_str + ", " + word.text

                    #
                    # Wenn das ganze Teil einer Konjunktionskette ist,
                    # dann müssen wir auch das Konjunktionswort (und, oder)
                    # berücksichtigen.
                    #
                    conjunction_word = conjunction_word_before()
                    if conjunction_word:
                        return word_str + " " + conjunction_word.text + " " + word.text

                    #
                    # Keine Konjunktionskette: Dann immer mittels "und" verbinden.
                    #
                    return word_str + " und " + word.text

                changes.append(transform_noun_or_pron(word, "Plur", "Fem", noun_transformer, nothing, nothing))

                #
                # Zusätzliche Korrektur, falls das Wort nach einer Konjunktion (und, oder) steht.
                #
                # bsp.: Schüler und Lehrer gehen ein Eis essen.
                #                   ______
                #
                # In diesem Fall muss das "und" oder ein anderes Konjunktionswort entfernt werden und durch eine Komma-Konstruktion ersetzt werden.
                #
                # Schüler, Lehrerinnen und Lehrer gehen ein Eis essen.
                #
                conjunction_word = conjunction_word_before()
                if conjunction_word:
                    changes.append([
                        {
                            "from": conjunction_word.idx - 1,
                            "to": conjunction_word.idx + len(conjunction_word.text) + 1,
                            "type": TYPE_CONJ,
                            "replace_with": ", "
                        }
                    ])

            possible_corrections.append({
                "type": "BOTH_FORMS",
                "changes": flatten(changes)
            })
        except Exception as e:
            errors.append(f"Konnte Korrekturvorschlag 'BOTH_FORMS' nicht erstellen: {e}")
            loguru.logger.info(f"Konnte Korrekturvorschlag 'BOTH_FORMS' nicht erstellen: {e}")
            loguru.logger.exception(e)

        return possible_corrections, errors
    elif are_singular:
        try:
            #
            # Zunächst bieten wir als Korrektur die *_:/-Formen an.
            #
            # Dabei arbeiten wir mit dem Platzhalter ?Innen bzw. ?In. Auf der Oberfläche
            # kann diese Form dann bequem in die vom Benutzer gewünschte Form,
            # bspsw. :in, /in, *in, In wählen.
            #
            def genderify_feminine_form(word_str):
                if word_str.endswith("in"):
                    return word_str[0:-2] + "?In"

                return word_str

            def genderify_det_form(det, old_det):
                # Bsp.: Der?Die
                #
                # Durch was das ? ersetzt wird, kann wieder durch
                # den Benutzer entschieden werden.
                return old_det + "?" + det

            def genderify_pron_form(pron, old_pron):
                # Bsp.: Dessen?Deren
                #
                # Durch was das ? ersetzt wird, kann wieder durch
                # den Benutzer entschieden werden.
                return old_pron + "?" + pron

            changes = flatten([transform_noun_or_pron(w, "Sing", "Fem", genderify_feminine_form, genderify_det_form, genderify_pron_form) for w in coref_words])

            possible_corrections.append({
                "type": "*",
                "changes": changes
            })

        except Exception as e:
            errors.append(f"Konnte Korrekturvorschlag '*' nicht erstellen: {e}")
            loguru.logger.info(f"Konnte Korrekturvorschlag '*' nicht erstellen: {e}")
            loguru.logger.exception(e)

        try:
            def genderify_feminine_form(word_str):
                if word_str.endswith("innen"):
                    return word_str[0:-5] + "?Innen"

                return word_str

            changes = flatten([transform_noun_or_pron(w, "Plur", "Fem", genderify_feminine_form, nothing, nothing) for w in coref_words])

            possible_corrections.append({
                "type": "PLURAL_*",
                "changes": changes
            })
        except Exception as e:
            errors.append(f"Konnte Korrekturvorschlag 'PLURAL_*' nicht erstellen: {e}")
            loguru.logger.info(f"Konnte Korrekturvorschlag 'PLURAL_*' nicht erstellen: {e}")
            loguru.logger.exception(e)

        return possible_corrections, errors

    else:
        return [], [f"Für die Wörter `{str([x.text for x in coref_words])}` konnten keine Korrekturen erstellt werden, da sie unterschiedlichen Numerus besitzen."]





