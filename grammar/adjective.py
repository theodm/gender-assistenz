from loguru import logger

# https://www.deutschplus.net/pages/Demonstrativpronomen_derselbe
from grammar.shared import unbestimmte_artikel, bestimmte_artikel, for_target

derselb_formen = [
    "derselbe",  # maskulin, nominativ
    "demselben",  # maskulin, dativ
    "denselben",  # maskulin, akkusativ
    "desselben",  # maskulin, genitiv

    "dasselbe",  # neutrum, nominativ
    "demselben",  # neutrum, dativ
    "dasselbe",  # neutrum, akkusativ
    "desselben",  # neutrum, genitiv

    "dieselbe",  # feminin, nominativ
    "derselben",  # feminin, dativ
    "dieselbe",  # feminin, akkusativ
    "derselben",  # feminin, genitiv

    "dieselben",  # plural, nominativ
    "denselben",  # plural, dativ
    "dieselben",  # plural, akkusativ
    "derselben"  # plural, genitiv
]

starke_deklination = [
    "er",  # maskulin, nominativ
    "em",  # maskulin, dativ
    "en",  # maskulin, akkusativ
    "en",  # maskulin, genitiv

    "es",  # neutrum, nominativ
    "em",  # neutrum, dativ
    "es",  # neutrum, akkusativ
    "en",  # neutrum, genitiv

    "e",  # feminin, nominativ
    "er",  # feminin, dativ
    "e",  # feminin, akkusativ
    "er",  # feminin, genitiv

    "e",  # plural, nominativ
    "en",  # plural, dativ
    "e",  # plural, akkusativ
    "er"  # plural, genitiv
]

gemischte_deklination = [
    "er",  # maskulin, nominativ
    "en",  # maskulin, dativ
    "en",  # maskulin, akkusativ
    "en",  # maskulin, genitiv

    "es",  # neutrum, nominativ
    "en",  # neutrum, dativ
    "es",  # neutrum, akkusativ
    "en",  # neutrum, genitiv

    "e",  # feminin, nominativ
    "en",  # feminin, dativ
    "e",  # feminin, akkusativ
    "en",  # feminin, genitiv

    "en",  # plural, nominativ
    "en",  # plural, dativ
    "en",  # plural, akkusativ
    "er"  # plural, genitiv
]

schwache_deklination = [
    "er",  # maskulin, nominativ
    "en",  # maskulin, dativ
    "en",  # maskulin, akkusativ
    "en",  # maskulin, genitiv

    "es",  # neutrum, nominativ
    "en",  # neutrum, dativ
    "es",  # neutrum, akkusativ
    "en",  # neutrum, genitiv

    "e",  # feminin, nominativ
    "en",  # feminin, dativ
    "e",  # feminin, akkusativ
    "en",  # feminin, genitiv

    "en",  # plural, nominativ
    "en",  # plural, dativ
    "en",  # plural, akkusativ
    "er"  # plural, genitiv
]


def transform_adjective(adj, target_case, target_gender, target_number):
    logger.debug("Adjektiv {} soll in Kasus: {}, Geschlecht: {}, Numerus: {} umgewandelt werden.", adj, target_case, target_gender, target_number)

    # Ein adverbiales oder prädikatives Adjektiv, also ein solches, welches neben einem Verb vorkommt,
    # muss niemals umgewandelt werden.
    #
    # Beispiel:
    #
    # Er spricht schnell.
    #            _______
    #
    # Sein Sprechen ist schnell.
    #                   _______
    if adj.word.xpos == "ADJD":
        logger.debug("{} ist ein adverbiales oder prädikatives Adjektiv und wird nicht umgewandelt.", adj)
        return adj.word.text

    # Dann verbleibt nur ein attributives Adjektiv.
    assert adj.word.xpos == "ADJA"

    logger.trace("{} ist ein attributiertes Adjektiv", adj)

    # ToDo: Berücksichtigung Komparativ und Superlativ

    # Wir müssen nun anhand des Kontextes herausfinden,
    # ob das Adjektiv, stark dekliniert, schwach dekliniert oder gemischt dekliniert ist.

    def declination(adj, target_number_is_plural = False):
        # Gemischte Deklination
        # Quelle: https://www.cafe-lingua.de/deutsche-grammatik/gemischte-deklination-adjektiv.php

        #
        # Fall: "Kein" geht voraus, aber nur im Singular:
        # Beispiel: Kein fleißiger Schüler sollte das tun.
        # Abgrenzung: Keine fleißigen Schüler sollten das tun.
        #

        # nmod des Nomens, auf den sich das Adjektiv bezieht
        # https://universaldependencies.org/en/dep/nmod.html
        parent = adj.parent
        nmod = adj.parent.find_rel_first("nmod")

        if parent.Number == "Sing" and nmod and "kein" in nmod.word.text.lower():
            return "gemischt"

        #
        # Fall: Unbestimmter Artikel geht voraus
        # Beispiel: Ein fleißiger Schüler sollte das tun.
        #
        det = adj.parent.find_rel_first(["det", "det:poss"])

        # Im Falle, dass der Ziel-Kasus plural ist, fällt ein unbestimmter Artikel
        # weg, dann wäre es falsch, für dieses Adjektiv die gemischte Deklination
        # zu wählen. Als Workaround wird dieser Fall hier zusätzlich mittels Parameter berücksichtigt.
        #
        # Beispiel: Umwandlung zu: "Fleißige Schüler sollten das tun."
        #
        if det and det.word.text.lower() in unbestimmte_artikel and not target_number_is_plural:
            assert det.word.xpos == "ART"
            return "gemischt"

        #
        # Fall: Possesivpronomen geht voraus
        # Beispiel: Unser fleißiger Schüler sollte das tun.
        #
        if det and det.word.xpos == "PPOSAT":
            # PPOSAT: attribuierendes Possessivpronomen
            return "gemischt"

        #
        # Fall: "irgendein" geht voraus
        # Beispiel: Irgendein fleißiger Schüler sollte das tun.
        #
        if det and "irgendein" in det.word.text.lower():
            assert det.word.xpos == "ART"
            return "gemischt"

        # Schwache Deklination
        # Quelle: https://www.cafe-lingua.de/deutsche-grammatik/gemischte-deklination-adjektiv.php

        #
        # Fall: Bestimmter Artikel geht voraus
        # Beispiel: Der fleißige Schüler sollte das tun.
        #
        det = adj.parent.find_rel_first("det")
        if det and det.word.text.lower() in bestimmte_artikel:
            assert det.word.xpos == "ART"
            return "schwach"

        #
        # Fall: "Kein" geht voraus, aber nur im Plural
        # Beispiel: Keine fleißigen Schüler sollten das tun.
        #
        parent = adj.parent
        nmod = adj.parent.find_rel_first("nmod")

        if parent.Number == "Plur" and nmod and "kein" in nmod.word.text.lower():
            return "schwach"

        #
        # Fall: derselbe, dieser, jeder, jener, mancher, welcher geht voraus
        # Beispiel: Derselbe fleißige Schüler sollte das tun.
        #
        if det:
            det_text = det.word.text.lower()
            if (det_text in derselb_formen) or ("dies" in det_text) or ("jede" in det_text) or ("jene" in det_text) or ("manch" in det_text) or ("welch" in det_text):
                return "schwach"

        #
        # Fall: "alle", "sämtliche", "beide" geht voraus
        # Beispiel: Alle fleißigen Schüler sollten das tun.
        #
        # ToDo: Stanza scheint bei dem Satz "Sämtliche fleißigen Schüler sollte das tun." "Sämtliche" fehlerhafterweise als Adjektiv zu erkennen.
        # ToDo: Dieser Fall wird jedoch vorerst einfach ignoriert, und so getan, als ob die Klassifikation richtig erfolgen würde.
        #
        if parent.Number == "Plur" and det and ("alle" in det.word.text or "sämtlich" in det.word.text or "beid" in det.word.text):
            return "schwach"

        #
        # Ansonsten muss das Adjektiv stark sein.
        #
        return "stark"

    target_is_plural = target_number == "Plur"

    decl = declination(adj, target_is_plural)

    logger.debug("{} ist {} dekliniert (Spezialfall ggf. zu beachten: {})", adj, decl, target_is_plural)

    if decl == "stark":
        list_for_decl = starke_deklination
    elif decl == "schwach":
        list_for_decl = schwache_deklination
    else:
        list_for_decl = gemischte_deklination

    endung = for_target(list_for_decl, target_case, target_gender, target_number)

    logger.debug("Für den Kasus: {}, Geschlecht: {}, Numerus: {} ergibt sich die Endung {}", target_case, target_gender, target_number, endung)

    return adj.word.lemma + endung















