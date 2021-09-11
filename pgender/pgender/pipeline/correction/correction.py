import loguru

from pgender.db_extender import feminine_noun_forms_and_convert
from pgender.fnf import feminine_noun_forms
from pgender.pipeline.correction.adj.change_adj_form import change_adj_form
from pgender.pipeline.correction.noun.select_noun_form import select_noun_form
from pgender.pipeline.correction.pron_art.select_pron_form import select_pron_art_form
from pgender.pipeline.correction.verb.change_verb_form import change_verb_form
from pgender.wordlib import follow_parent_dep, follow_child_dep, follow_child_dep_single_or_none
from pgender.wordlib2 import find_verb, find_adj, find_art_and_pron

TYPE_NOUN = "NOUN"
TYPE_CONJ = "CONJ"
TYPE_DET = "DET"
TYPE_VERB = "VERB"
TYPE_ADJ = "ADJ"

def preserve_case(new_str, old_str):
    if old_str[0:1].isupper():
        return new_str[0:1].upper() + "" + new_str[1:]

    return new_str


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

        #
        # In welchen Numerus soll das Nomen nach der Transformation stehen?
        #
        target_number,

        #
        # In welchem Sexus soll das Nomen bzw. die zugehörigen Wörter nach der Transformation stehen?
        #
        target_gender
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

def transform_noun_plural(
        word,
        lex_new_word,
        _transform_noun
):
    #
    # Im Plural muss außer dem Nomen selbst, sonst nichts weiteres verändert werden.
    #
    def nothing(x, y):
        return x

    return transform_noun(word, lex_new_word, _transform_noun, nothing, nothing, "Plur", "Fem")


def generate_possible_corrections_singular(word):
    errors = []

    fnf = feminine_noun_forms_and_convert(word)

    if not fnf:
        return None, [] # [f"Es konnte keine feminine Wortform für das Wort {word.text} gefunden werden."]

    possible_corrections = []

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

        possible_corrections.append({
                "type": "*",
                "changes": transform_noun(word, fnf[0], genderify_feminine_form, genderify_det_form, genderify_pron_form, "Sing", "Fem")
        })
    except Exception as e:
        errors.append(f"Konnte Korrekturvorschlag '*' nicht erstellen: {e}")
        loguru.logger.info(f"Konnte Korrekturvorschlag '*' nicht erstellen: {e}")

    try:
        def genderify_feminine_form(word_str):
            if word_str.endswith("innen"):
                return word_str[0:-5] + "?Innen"

            return word_str

        def genderify_det_form(det, old_det):
            return det

        def genderify_pron_form(pron, old_pron):
            return pron

        possible_corrections.append({
                "type": "PLURAL_*",
                "changes": transform_noun(word, fnf[0], genderify_feminine_form, genderify_det_form, genderify_pron_form, "Plur", "Fem")
        })
    except Exception as e:
        errors.append(f"Konnte Korrekturvorschlag 'PLURAL_*' nicht erstellen: {e}")
        loguru.logger.info(f"Konnte Korrekturvorschlag 'PLURAL_*' nicht erstellen: {e}")


    return possible_corrections, errors



def generate_possible_corrections_plural(word):
    errors = []

    fnf = feminine_noun_forms_and_convert(word)

    if not fnf:
        return None, [] # [f"Es konnte keine feminine Wortform für das Wort {word.text} gefunden werden."]

    possible_corrections = []

    try:
        #
        # Zunächst bieten wir als Korrektur die *_:/-Formen an.
        #
        # Dabei arbeiten wir mit dem Platzhalter ?Innen bzw. ?In. Auf der Oberfläche
        # kann diese Form dann bequem in die vom Benutzer gewünschte Form,
        # bspsw. :innen, /innen, *innen, Innen wählen.
        #
        def genderify_feminine_form(word_str):
            if word_str.endswith("innen"):
                return word_str[0:-5] + "?Innen"

            return word_str

        possible_corrections.append({
            "type": "*",
            "changes": transform_noun_plural(word, fnf[0], genderify_feminine_form)
        })
    except Exception as e:
        errors.append(f"Konnte Korrekturvorschlag '*' nicht erstellen: {e}")
        loguru.logger.info(f"Konnte Korrekturvorschlag '*' nicht erstellen: {e}")


    try:
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
        def both_word_forms(word_str):
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

        changes = transform_noun_plural(word, fnf[0], both_word_forms)

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
            changes.append(
                {
                    "from": conjunction_word.idx - 1,
                    "to": conjunction_word.idx + len(conjunction_word.text) + 1,
                    "type": TYPE_CONJ,
                    "replace_with": ", "
                }
            )

        possible_corrections.append({
                "type": "BOTH_FORMS",
                "changes": changes
        })
    except Exception as e:
        errors.append(f"Konnte Korrekturvorschlag 'BOTH_FORMS' nicht erstellen: {e}")
        loguru.logger.info(f"Konnte Korrekturvorschlag 'BOTH_FORMS' nicht erstellen: {e}")

    return possible_corrections, errors

def generate_possible_corrections(word):
    if not word.morph.get("Number"):
        # ToDo: Fehler zurückgeben?
        return [], [] #[f"Für das Wort {word.text} konnten keine Korrekturen erstellt werden, da es nicht die erforderlichen morphologischen Eigenschaften erhält."]

    if word.pos_ != "NOUN":
        return None, [] #[f"Für das Wort {word.text} konnten keine Korrekturen erstellt werden, da es sich nicht um ein Nomen handelt."]

    if word.morph.get("Number")[0] == "Plur":
        return generate_possible_corrections_plural(word)

    return generate_possible_corrections_singular(word)