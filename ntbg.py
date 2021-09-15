
# Gibt an, ob ein Nomen gegendert werden muss.
import loguru
from charsplit import splitter, Splitter

from pgender.db_extender import find_in_db_and_convert
from pgender.fnf import has_feminine_noun_form, feminine_noun_forms, find_in_db
from pgender.utils.string import remove_prefix
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

BOTH_FORMS = 9

splitter = Splitter()


def _feminine_noun_forms(word):
    fnf = feminine_noun_forms(word, False)
    if fnf:
        return fnf
    else:
        fnf = feminine_noun_forms(word, True)

        if fnf:
            return fnf
        else:
            splits = splitter.split_compound(word.text)

            logger.debug(f"splits found: {splits}")

            if splits:
                fnf = feminine_noun_forms(splits[0][-1], True)
                return fnf

    return []

def _has_feminine_noun_form(word):
    return _feminine_noun_forms(word)

#
# Gibt an, ob das Wort [feminine_form] eine weibliche Form von [of_word]
# ist. Auch nur Übereinstimmungen des letzten Teil eines zusammengesetzten Nomens werden gefunden.
#
# Es ist gedacht um im Falle, dass beide Formen explizit genannt werden, keinen Korrekturvorschlag zu
# erstellen.
#
# Bsp.:
#  - [Wissenschaftlerin, Wissenschaftler] -> true
#  - [Raketenwissenschaftlerin, Wissenschaftler] -> true
#  - [Raktenwissenschaftlerin, -Wissenschaftler] -> true (Bsp: Rakentenwissenschaftlerinnen und -Wissenschaftler)
#
# of_word
def _is_feminine_noun_form_of_extended(feminine_form, of_word):
    #
    # Wort normalisieren, es könnte in folgender Konstruktion stehen: Rakentenwissenschaftlerinnen und -Wissenschaftler
    #
    lex_ff = find_in_db_and_convert(feminine_form)

    if not lex_ff:
        return False

    fnf = _feminine_noun_forms(of_word)

    if lex_ff["title"].lower() in [x["title"].lower() for x in fnf]:
        return True

    splits = splitter.split_compound(lex_ff["title"])

    if splits:
        if splits[0][-1].lower() in [x["title"].lower() for x in fnf]:
            return True

    return False


def _is_feminine_noun_form_of(feminine_form, of_word):
    db = find_in_db(feminine_form)

    if not db:
        db = find_in_db(feminine_form, True)

        if not db:
            splits = splitter.split_compound(feminine_form.text)

            logger.debug(f"splits found: {splits}")

            if splits:
                db = find_in_db(splits[0][-1], True)

                if not db:
                    return False

            else:
                return False

    fnf = _feminine_noun_forms(of_word)

    logger.debug("db: {}", db)
    logger.debug("fnf: {}", fnf)

    if db["title"] in [x["title"] for x in fnf]:
        return True

    return False

# Ausgehend von einem initialen Wort überprüfen wir,
# ob dieses Vorkomniss gegendert werden muss.
def needs_to_be_gendered(doc, word, check_coref=True):
    if word.pos_ == "PROPN":
        return False, [(EIGENNAME_GEFUNDEN, f"Eigenname gefunden: {word}")],

    if word.pos_ == "NOUN":
        if not _has_feminine_noun_form(word):
            return False, [(NO_FEMININE_FORM, f"Keine feminine Wortform gefunden: {word}")]

    #
    # Und-Konjunktion
    #
    # Sowohl die männliche Form als auch die weibliche Form wird genannt. Also muss
    # keine Korrektur erfolgen.
    #
    # Wissenschaftler und Wissenschaftlerinnen gehen ein Eis essen.
    # _______________     ____________________
    #
    # Hier die Richtung: Wissenschaftler -> und -> Wissenschaftlerinnen
    #
    conjunctions = follow_child_dep(word, ["cd", "cj"])
    while conjunctions:
        new_conjunctions = []
        for conj in conjunctions:
            if conj.pos_ == "NOUN" and _is_feminine_noun_form_of(conj, word):
                return False, [(BOTH_FORMS, "Beide Formen")]

            new_conjunctions.extend(follow_child_dep(conj, ["cd", "cj"]))

        conjunctions = new_conjunctions

    #
    # Und-Konjunktion
    #
    # Wissenschaftlerinnen und Wissenschaftler gehen ein Eis essen.
    # ____________________     _______________
    #
    # Hier die Richtung: Wissenschaftlerinnen -> Wissenschaftler
    #
    conj = word
    while True:
        conj = follow_parent_dep(conj, ["cj", "cd"])

        if not conj:
            break

        if conj.pos_ == "NOUN" and _is_feminine_noun_form_of_extended(conj, word):
            return False, [(BOTH_FORMS, "Beide Formen")]


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
        result = needs_to_be_gendered(doc, nkm, check_coref)

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
            result = needs_to_be_gendered(doc, subject, check_coref)

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
        result = needs_to_be_gendered(doc, app, check_coref)

        if not result[0]:
            return False, [(APPOSITION, f"Einschubsatz: {app}")] + result[1]


    # Erweiterung von Nominalphrase mittels Genitiv-Attribut
    #
    # Wenn ein Nominal
    # TODO:
    # Bsp.: Hinter der neuen Firma steht unter anderem Lucent Technologies , einer der größten Anbieter von Equipment für Netzwerke und Telekommunikation .
    ag = follow_parent_dep(word, "ag")
    if ag and ag.pos_ == "PRON":
        result = needs_to_be_gendered(doc, ag, check_coref)

        if not result[0]:
            return False, [(GENITIVE_ATTRIBUTE, f"Genitiv-Attribut: {ag} (für: {word})")] + result[1]


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
            result = needs_to_be_gendered(doc, parent_of_relative_clause, check_coref)

            if not result[0]:
                return False, [(RELATIVE_CLAUSE, f"Pronomen des Relativsatzes: {result} (für: {word})")] + result[1]


    if check_coref:
        # Coreference Chains
        #
        #
        #doc._.coref_chains.print()
        for chain in doc._.coref_chains:
            mention_indices = [x.root_index for x in chain]

            logger.debug("mention indices: {}", mention_indices)
            logger.debug("word offset: {}", word.i)

            if word.i in mention_indices:
                for owi in mention_indices:
                    if owi == word.i:
                        continue

                    result = needs_to_be_gendered(doc, doc[owi], False)

                    if not result[0]:
                        return False, [(COREF_CHAIN, f"Koreferenz-Kette: {doc[owi]} (für: {word})")] + \
                               result[1]


    return True, None