from wordlib import follow_child_dep, follow_parent_dep, follow_child_dep_single_or_none


#
# Gibt alle Adjektive für ein Nomen zurück.
#
def find_adj(word):
    if word.pos_ != "NOUN":
        raise Exception("Nur Nomen können Adjektive besitzen.")

    noun_kernels = follow_child_dep(word, "nk")

    result = []

    for nk in noun_kernels:
        if nk.pos_ == "ADJ":
            result.append(nk)

    return result


substituirende_pronomen = ["PDS", "PIS", "PPER", "PPOSS", "PRELS", "PRF", "PWS", "PWAV", "PROAV"]
# ART: bestimmter ODER unbestimmter Artikel
# PDAT: attribuierendes Demonstrativpronomen
# PIAT: attribuierendes Indefinitpronomen
# PPOSAT: attribuierendes Possessivpronomen
# PRELAT: attribuierendes Relativpronomen
# PWAT: attribuierendes Interrogativpronomen
attributierende_pronomen_und_artikel = ["ART", "PDAT", "PIAT", "PPOSAT", "PRELAT", "PWAT"]

alle_pronomen_und_artikel = substituirende_pronomen + attributierende_pronomen_und_artikel

#
# Gibt alle Artikel und Pronomen für ein Nomen zurück.
#
# Es werden sowohl attributierende und substituirende Pronomen erfasst sowie Artikel.
#
def find_art_and_pron(word):
    result = []

    # Artikel und Pronomen, die vor dem Nomen stehen, werden hiermit erfasst.
    noun_kernels = follow_child_dep(word, "nk")
    for nk in noun_kernels:
        if nk.tag_ in alle_pronomen_und_artikel:
            result.append(nk)

    # Pronomen in Relativsätzen
    #
    # Der Benutzer, dessen ...
    #               ______
    relative_clauses = follow_child_dep(word, "rc")
    for rc in relative_clauses:
        subjects = follow_child_dep(rc, "sb")

        for sj in subjects:
            if sj.tag_ in alle_pronomen_und_artikel:
                result.append(sj)
                continue

            #
            # Genitive-Attribut für Konstruktionen wie.
            # Bsp.: Der Vater, dessen...
            #
            genitive_attributes = follow_child_dep(sj, "ag")

            for ga in genitive_attributes:
                if ga.tag_ in alle_pronomen_und_artikel:
                    result.append(ga)

    #
    # Pronomen in Klausal-Sätzen.
    #
    # Bsp.: Der Benutzer sagte, er sei vorsichtig vorgegangen.
    #
    verb_of_sentence = follow_parent_dep(word, "sb")
    if verb_of_sentence:
        clausal_objects = follow_child_dep(verb_of_sentence, "oc")
        for co in clausal_objects:
            subjects = follow_child_dep(co, "sb")

            for sj in subjects:
                if sj.tag_ in alle_pronomen_und_artikel:
                    result.append(sj)

    return result

#
# Gibt alle Verb des Nomen im Satz zurück, die verändert werden müssen, wenn sich der Numerus des Wortes ändert.
#
# Bsp.: Der Lehrer geht ein Eis essen.
#           ______
#       --> geht
#
# Auch Relativsätze werden berücksichtigt.
# Bsp.: Es wuerden aber auch Gespraeche mit jedem anderen Anbieter gefuehrt, der meine, ein entsprechendes Angebot machen zu koennen.
#                                                         ________
#                                                     --> meine
#
# Auch Klausal-Sätze werden berücksichtigt:
# Bsp.: Der Benutzer sagte, er sei vorsichtig vorgegangen.
#                    _____     ___
#
def find_verb(word):
    result = []
    #
    # Das Verb, zu dem das Nomen das Subjekt ist.
    #
    # AUX sind die Hilfsverben: Bsp.: soll
    parent = follow_parent_dep(word, "sb")
    if parent and (parent.pos_ == "VERB" or parent.pos_ == "AUX"):
        result.append(parent)

    #
    # Das Verb in einem Relativsatz.
    #
    rc = follow_child_dep_single_or_none(word, "rc")
    if rc:
        if rc.pos_ == "VERB":
            result.append(rc)

    #
    # Das Verb in einem Klausal-Satz.
    #
    # Bsp.: Der Benutzer sagte, er sei vorsichtig vorgegangen.
    verb_of_sentence = follow_parent_dep(word, "sb")
    if verb_of_sentence:
        clausal_objects = follow_child_dep(verb_of_sentence, "oc")
        for co in clausal_objects:
            # ToDo: co.morph.get("Number") erklären,
            # Sonst gibt Ein fleißiger Rentner geht ein Eis essen. auch essen zurück.
            if (co.pos_ == "VERB" or co.pos_ == "AUX") and co.morph.get("Number"):
                result.append(co)


    return result