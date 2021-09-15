

#
# Findet anhand des Kontext des übergebenen Wortes heraus, ob das Adjektiv, stark dekliniert, schwach dekliniert oder gemischt dekliniert ist.
#
from pipeline.correction.special_word_forms import unbestimmte_artikel, bestimmte_artikel, starke_deklination, \
    schwache_deklination, gemischte_deklination, special_word_form, demonstrativ_pronomen_derselb
from wordlib import follow_parent_dep, follow_child_dep



def get_declination(adj, target_number_is_plural = False):
    parent = follow_parent_dep(adj, "nk")

    # Gemischte Deklination
    # Quelle: https://www.cafe-lingua.de/deutsche-grammatik/gemischte-deklination-adjektiv.php

    #
    # Fall 1: "Kein" geht voraus, aber nur im Singular:
    #
    # Beispiel: Kein fleißiger Schüler sollte das tun.
    # Abgrenzung: Keine fleißigen Schüler sollten das tun.
    #
    if parent.morph.get("Number")[0] == "Sing":
        other_nks = follow_child_dep(parent, "nk")
        for nk in other_nks:
            if "kein" in nk.text.lower():
                return "gemischt"


    #
    # Fall 2: Unbestimmter Artikel geht voraus
    # Beispiel: Ein fleißiger Schüler sollte das tun.
    #
    det = None

    # Artikel finden
    nks = follow_child_dep(parent, "nk")
    for nk in nks:
        if nk.pos_ == "DET":
            det = [nk]
            break

    # Im Falle, dass der Ziel-Kasus plural ist, fällt ein unbestimmter Artikel
    # weg, dann wäre es falsch, für dieses Adjektiv die gemischte Deklination
    # zu wählen. Als Workaround wird dieser Fall hier zusätzlich mittels Parameter berücksichtigt.
    #
    # Beispiel: Umwandlung zu: "Fleißige Schüler sollten das tun."
    #
    if det and det[0].text.lower() in unbestimmte_artikel and not target_number_is_plural:
        return "gemischt"

    #
    # Fall 3: Possesivpronomen geht voraus
    # Beispiel: Unser fleißiger Schüler sollte das tun.
    #
    if det and det[0].tag_ == "PPOSAT":
        # PPOSAT: attribuierendes Possessivpronomen
        return "gemischt"

    #
    # Fall 4: "irgendein" geht voraus
    # Beispiel: Irgendein fleißiger Schüler sollte das tun.
    #
    if det and "irgendein" in det[0].text.lower():
        return "gemischt"


    # Schwache Deklination
    # Quelle: https://www.cafe-lingua.de/deutsche-grammatik/gemischte-deklination-adjektiv.php

    #
    # Fall 5: Bestimmter Artikel geht voraus
    # Beispiel: Der fleißige Schüler sollte das tun.
    #
    if det and det[0].text.lower() in bestimmte_artikel:
        return "schwach"

    #
    # Fall 6: "Kein" geht voraus, aber nur im Plural
    # Beispiel: Keine fleißigen Schüler sollten das tun.
    #
    if parent.morph.get("Number")[0] == "Plur":
        other_nks = follow_child_dep(parent, "nk")
        for nk in other_nks:
            if "kein" in nk.text.lower():
                return "schwach"

    #
    # Fall 7: derselbe, dieser, jeder, jener, mancher, welcher geht voraus
    # Beispiel: Derselbe fleißige Schüler sollte das tun.
    #
    if det:
        det_text = det[0].text.lower()
        if (det_text in demonstrativ_pronomen_derselb) or ("dies" in det_text) or ("jede" in det_text) or ("jene" in det_text) or ("manch" in det_text) or ("welch" in det_text):
            return "schwach"

    #
    # Fall 8: "alle", "sämtliche", "beide" geht voraus
    # Beispiel: Alle fleißigen Schüler sollten das tun.
    #
    if parent.morph.get("Number")[0] == "Plur" and det and ("alle" in det[0].text.lower() or "sämtlich" in det[0].text.lower() or "beid" in det[0].text.lower()):
        return "schwach"

    #
    # Ansonsten muss das Adjektiv stark dekliniert sein.
    #
    return "stark"

def get_endung_for_declination(adj, target_case, target_gender, target_number):
    target_is_plural = target_number == "Plur"

    decl = get_declination(adj, target_is_plural)

    if decl == "stark":
        list_for_decl = starke_deklination
    elif decl == "schwach":
        list_for_decl = schwache_deklination
    else:
        list_for_decl = gemischte_deklination

    endung = special_word_form(list_for_decl, target_case, target_gender, target_number)

    return endung

def change_adj_form(adj, target_gender, target_number):
    #
    # # ToDo: Attributiertes Adjektiv + adverbiales Adjektiv
    # assert adj.word.tag_ == "ADJA"

    # ToDo: Trick hier beschreiben

    text = adj.text

    #
    # Workaround: Manche Adjektive erhalten keine morphologischen Informationen.
    # Ist das der Fall versuchen wir hilfsweise, die morphologischen Informationen aus
    # dem Nomen zu ziehen.
    #
    morph_case = adj.morph.get("Case")[0] if adj.morph.get("Case") else None
    morph_gender = adj.morph.get("Gender")[0] if adj.morph.get("Gender") else None
    morph_number = adj.morph.get("Number")[0] if adj.morph.get("Number") else None

    if not morph_case or not morph_gender or not morph_number:
        noun = follow_parent_dep(adj, "nk")

        morph_case = noun.morph.get("Case")[0] if noun.morph.get("Case") else None
        morph_gender = noun.morph.get("Gender")[0] if noun.morph.get("Gender") else None
        morph_number = noun.morph.get("Number")[0] if noun.morph.get("Number") else None

        if not morph_case or not morph_gender or not morph_number:
            raise Exception(f"Für das Adjektiv {noun.text} können die morphologischen Informationen nicht ermittelt werden.")

    endung_bestehnd = get_endung_for_declination(adj, morph_case, morph_gender, morph_number)
    endung_neu = get_endung_for_declination(adj, morph_case, target_gender, target_number)

    def remove_suffix(str, suffix):
        if str.endswith(suffix):
            return str[:-len(suffix)]

        return str

    # ToDo: Parallelflexion + Wechselflexion erklären
    # Wechselflexion berücksichtigen
    if text.endswith("en") and endung_bestehnd == "em":
        return remove_suffix(text, "en") + endung_neu

    return remove_suffix(text, endung_bestehnd) + endung_neu




