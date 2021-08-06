
# Gibt an, ob ein Nomen gegendert werden muss.
import loguru

from pgender.wordlib import follow_child_dep, follow_parent_dep, follow_child_dep_single_or_none
from loguru import logger

EIGENNAME_GEFUNDEN = 1
NO_FEMININE_FORM = 6

NOUN_KERNEL_NAME_FOUND = 2
KOPULA_SENTENCE = 3
APPOSITION = 4
GENITIVE_ATTRIBUTE = 5
RELATIVE_CLAUSE = 7
COREF_CHAIN = 8


# Ausgehend von einem initialen Wort überprüfen wir,
# ob dieses Vorkomniss gegendert werden muss.
def needs_to_be_gendered(doc, word, initial_words=None, check_coref=True):
    if initial_words is None:
        initial_words = [word]

    if word.pos_ == "PROPN":
        return False, [(EIGENNAME_GEFUNDEN, f"Eigenname gefunden: {word}")],

    if word.pos_ == "NOUN" and word not in initial_words:
        return False, [(NO_FEMININE_FORM, f"Keine feminine Wortform gefunden: {word}")]


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
        result = needs_to_be_gendered(doc, nkm, initial_words)

        if not result[0]:
            return False, [(NOUN_KERNEL_NAME_FOUND, f"Noun-Kernel weist auf Eigenname hin: {nkm}")] + result[1]

    # Kopulasätze (vgl.: https://de.wikipedia.org/wiki/Kopula_(Grammatik))
    #
    # Nomen wird durch ein Kopulaverb einem Namen zugeordnet.
    # Bsp.: Klesch ist bereits neuer Betreiber in Hessen.
    #
    # Reguläre Kopulaverben: sein, werden, bleiben Irreguläre Kopulaverben: aussehen, erscheinen, dünken, klingen,
    # schmecken, heißen, gelten, sich vorkommen, sich erweisen, ...
    #

    # 1. Schritt wir suchen das Kopulaverb des Wortes
    kopula_verb = follow_parent_dep(word, "pd")
    if kopula_verb:
        # 2. Schritt wir suchen das Subjekt und falls es
        #    sich auf einen Eigennamen bezieht, dann
        #    gendern wir nicht.
        subject = follow_child_dep_single_or_none(kopula_verb, "sb")
        if subject:
            result = needs_to_be_gendered(doc, subject, initial_words)

            if not result[0]:
                return False, [(KOPULA_SENTENCE, f"Kopula-Satzbau: {subject} (Kopula-Verb: {kopula_verb})")] + result[1]


    # Einschubsätze (App)
    #
    # Ein Einschubsatz beschreibt ein Subjekt oder Objekt genauer. Die dadurch notwendigen Adjektive
    # müssen dann nicht gegendert werden, wenn das Subjekt oder Objekt selbst nicht gegendert werden müssen.
    # Bsp.: Hinter der neuen Firma steht unter anderem Lucent Technologies, einer der größten Anbieter von Equipment für Netzwerke und Telekommunikation.
    #                                                  ___________________  _____
    app = follow_parent_dep(word, "app")
    if app:
        result = needs_to_be_gendered(doc, app, initial_words)

        if not result[0]:
            return False, [(APPOSITION, f"Einschubsatz: {app}")] + result[1]


    # Erweiterung von Nominalphrase mittels Genitiv-Attribut
    #
    # Wenn ein Nominal
    # TODO:
    # Bsp.: Hinter der neuen Firma steht unter anderem Lucent Technologies , einer der größten Anbieter von Equipment für Netzwerke und Telekommunikation .
    ag = follow_parent_dep(word, "ag")
    if ag and word.pos_ == "PRON":
        result = needs_to_be_gendered(doc, ag, initial_words)

        if not result[0]:
            return False, [(GENITIVE_ATTRIBUTE, f"Genitiv-Attribut: {app} (für: {ag})")] + result[1]


    # Subjekt der Relativklausel
    #
    # Wenn ein Pronomen als Subjekt eines Relativsatzes steht,
    # dann bezieht es sich wahrscheinlich auf das Subjekt des
    # äußeren Satzes. Wir übernehmen das Ergebnis des Wortes,
    # auf den sich das Pronomen bezieht.
    #
    # Bsp.: Der Duden für Szenesprachen , der bereits seit dem Frühjahr im Handel ist , wird nun online fortgeschrieben .
    #           _____                     ___
    parent_of_subject = follow_parent_dep(word, "sb")
    if parent_of_subject:
        parent_of_relative_clause = follow_parent_dep(parent_of_subject, "rc")

        if parent_of_relative_clause:
            result = needs_to_be_gendered(doc, parent_of_relative_clause, initial_words)

            if not result[0]:
                return False, [(RELATIVE_CLAUSE, f"Pronomen des Relativsatzes: {result} (für: {word})")] + result[1]


    if check_coref:
        # Coreference Chains
        #
        #
        doc._.coref_chains.print()
        for chain in doc._.coref_chains:
            mention_indices = [x.root_index for x in chain]

            logger.debug("mention indices: {}", mention_indices)
            logger.debug("word offset: {}", word.i)

            if word.i in mention_indices:
                for owi in mention_indices:
                    if owi == word.i:
                        continue

                    result = needs_to_be_gendered(doc, doc[owi], initial_words, False)

                    if not result[0]:
                        return False, [(COREF_CHAIN, f"Koreferenz-Kette: {doc[owi]} (für: {word})")] + \
                               result[1]

    return True, None