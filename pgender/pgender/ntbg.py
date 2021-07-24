
# Gibt an, ob ein Nomen gegendert werden muss.
from wordlib import follow_child_dep, follow_parent_dep, follow_child_dep_single_or_none
from loguru import logger

EIGENNAME_GEFUNDEN = 1
EIGENNAME_KOPULA_SATZ_GEFUNDEN = 2

# Ausgehend von einem Nomen überprüfen wir,
# ob dieses Vorkomniss gegendert werden muss.
def needs_to_be_gendered(word):
    # Das Nomen wird durch einen Namen spezifiziert,
    # daher gehen wir davon aus, dass das Gendern
    # nicht nötig ist.
    #
    # Bsp.: Bundeswirtschaftsminister Werner Müller freut sich über solche Aussichten.
    #
    # Dabei ist der Name (Werner Müller) ein sogenannter noun kernel modifier (nk) der
    # dem Nomen zusätzliche Informationen hinzufügt. Das könnten auch beispielsweise
    # Adjektive sein, diese schließen wir durch das Tag PROPN (proper noun) aus, welches grammatikalisch einen Namen
    # eines Ortes, Subjekts oder Objekts beschreibt.
    #
    # Siehe auch:
    # https://universaldependencies.org/u/pos/PROPN.html
    # https://www.coli.uni-saarland.de/projects/sfb378/negra-corpus/kanten.html#NK
    #
    noun_kernel_modifiers = follow_child_dep(word, "nk")

    for nkm in noun_kernel_modifiers:
        if nkm.pos_ == "PROPN":
            return False, EIGENNAME_GEFUNDEN, f"Vorkommen {str(word)} muss nicht angepasst werden, da ein Eigenname " \
                                              f"gefunden wurde: {str(nkm)} "

    # Kopulasätze (vgl.: https://de.wikipedia.org/wiki/Kopula_(Grammatik))
    #
    # Nomen wird durch ein Kopulaverb einem Namen zugeordnet.
    # Bsp.: Klesch ist bereits neuer Betreiber in Hessen.
    #
    # Reguläre Kopulaverben: sein, werden, bleiben Irreguläre Kopulaverben: aussehen, erscheinen, dünken, klingen,
    # schmecken, heißen, gelten, sich vorkommen, sich erweisen, ...
    #

    # 1. Schritt wir suchen das Kopulaverb des Nomen
    kopula_verb = follow_parent_dep(word, "pd")
    if kopula_verb:
        # 2. Schritt wir suchen das Subjekt und falls es sich um
        # ein "Proper Noun" handelt, müssen wir nicht gendern,
        # da sich das Nomen auf etwas Konkretes bezieht.
        subject = follow_child_dep_single_or_none(kopula_verb, "sb")
        if subject and subject.pos_ == "PROPN":
            return False, EIGENNAME_KOPULA_SATZ_GEFUNDEN, f"Vorkommen {str(word)} muss nicht angepasst werden, da ein "\
                                                          f"Eigenname in einer Kopula-Konstruktion gefunden wurde: "\
                                                          f"{str(subject)} "




    return True, None, None