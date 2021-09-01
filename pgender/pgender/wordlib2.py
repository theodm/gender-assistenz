
# Artikel eines Nomen finden.
from pgender.wordlib import follow_child_dep, follow_parent_dep


#
# Gibt alle Artikel für ein Nomen zurück.
#
def find_det(word):
    if word.pos_ != "NOUN":
        raise Exception("Nur Nomen können Artikel besitzen.")

    noun_kernels = follow_child_dep(word, "nk")

    result = []

    for nk in noun_kernels:
        if nk.pos_ == "DET":
            result.append(nk)

    return result

#
# Gibt das (übergeordnete) Verb des Nomen im Satz zurück.
# Bsp.: Der Lehrer geht ein Eis essen.
#           ______
#       --> geht
#
def find_verb(word):
    if word.pos_ != "NOUN":
        raise Exception("Nur zu Nomen kann das zugehörige Verb gefunden werden.")

    parent = follow_parent_dep(word, "sb")

    if parent and parent.pos_ == "VERB":
        return parent

    return None