import json

import stanza

# stanza.download('de')
from loguru import logger

from grammar.adjective import transform_adjective
from grammar.determiner import transform_determiner
from grammar.noun import transform_noun
from utils.regex import regex_first_or_none
from wiktionary.api import find_by_lemma


# def get_word_by_id(sent, id):
#     return sent.words[id + 1]


def get_root_word(sent):
    for w in sent.words:
        if w.head == 0:
            return w


def get_children(sent, word):
    result = []
    for w in sent.words:
        if w.head == word.id:
            result.append(w)
    return result


def flatten(t):
    return [item for sublist in t for item in sublist]


class RecWord:
    def __init__(self, sent, word, parent_as_rec_word):
        self.word = word

        self.parent = parent_as_rec_word
        self.children = [RecWord(sent, x, self) for x in get_children(sent, word)]

        w = word
        self.Case = regex_first_or_none(f"Case=([a-zA-Z]*)\\|?", str(w.feats))
        self.Definite = regex_first_or_none(f"Definite=([a-zA-Z]*)\\|?", str(w.feats))
        self.Gender = regex_first_or_none(f"Gender=([a-zA-Z]*)\\|?", str(w.feats))
        self.Number = regex_first_or_none(f"Number=([a-zA-Z]*)\\|?", str(w.feats))
        self.PronType = regex_first_or_none(f"PronType=([a-zA-Z]*)\\|?", str(w.feats))

    def in_order_list(self):
        left = flatten([x.in_order_list() for x in self.children if x.word.id < self.word.id])
        right = flatten([x.in_order_list() for x in self.children if x.word.id > self.word.id])

        return left + [self] + right

    # Suche die Kinder nach einer bestimmten
    # Relationseigenschaft (det, amod, ...) ab.
    def find_multiple_rel(self, deprel_list):
        result = []

        for c in self.children:
            if c.word.deprel in deprel_list:
                result.append(c)

        return result

    # Suche die Kinder nach einer bestimmten
    # Relationseigenschaft (det, amod, ...) ab.
    def find_rel(self, deprel):
        if type(deprel) is list:
            return self.find_multiple_rel(deprel)

        return self.find_multiple_rel([deprel])

    def find_rel_first(self, deprel):
        res = self.find_multiple_rel(deprel)

        if not res:
            return None

        return res[0]

    def needs_to_be_gendered(self):
        # Wenn der Elternknoten bereits ein Name ist,
        # dann brauchen wir nicht gendern.
        #
        # Bsp.: Bundeswirtschaftsminister Werner Müller freut sich über solche Aussichten
        #
        # Negativ-Bsp.: Ziel ist es , dass sich T-DSL-Kunden auf dem Wege von Netz-Zusammenschaltungen einen Internet-Provider frei aussuchen dürfen .
        if self.find_parent_if_rel("dep") and self.parent.word.upos == "PROPN":
            return False

        # Wenn ein Compound nicht gegendert werden muss, dann muss
        # dieses Wort auch nicht gegendert werden. Beispielsweise ist
        # in "AOL - Sprecher" AOL ein Compound von "Sprecher".
        #
        # Bsp.: AOL-Sprecher Stefan Michalk bestätigte dies gegenüber c't , meinte jedoch , dass derzeit noch nichts Konkretes geplant ist :
        if self.find_rel_first("compound") and not self.find_rel_first("compound").needs_to_be_gendered():
            return False

        # Wenn ein Kindknoten sich auf das Nomen bezieht, und diese
        # Beschreibung ein Name ist, dann brauchen wir nicht gendern.
        #
        # Bsp.: Klesch ist bereits neuer Betreiber in Hessen.
        if self.find_rel_first("nsubj") and self.find_rel_first("nsubj").word.upos == "PROPN":
            return False

        # Wenn ein Kindknoten eine genauere Beschreibung des Nomen
        # gibt (appos) und diese Beschreibung ein Name ist,
        # dann brauchen wir nicht gendern.
        #
        # Bsp.: Seit dem heutigen Mittwochmorgen kursierten an der Frankfurter Börse Gerüchte , denen zufolge Telekom - Chef Ron Sommer zurücktreten wird .
        if self.find_rel_first("appos") and self.find_rel_first("appos").word.upos == "PROPN":
            return False

        res = self.parent.find_parent_if_rel("appos") if self.parent else None

        if not res:
            return True

        if res.word.upos == "PROPN":
            return False



        return True


    # Ein Substantiv wird meist von einem Determinativ begleitet.
    #
    # der Firma
    # ___
    #
    # die Vertreter der US-Regierung
    #               ___
    def find_det(self):
        assert self.word.xpos == "NN"

        # nmod:poss wegen: Die Firma, deren Bauarbeiter mit seiner Tochter streikte, ging schlafen.
        return self.find_multiple_rel(["det", "det:poss", "nmod:poss"])

    # Ein Adjektiv, welches auf das Substantiv bezogen ist.
    #
    # der neuen Firma
    #     _____
    def find_amod(self):
        assert self.word.xpos == "NN"

        return self.find_rel("amod")

    # Gibt den Parent zurück, falls er mit
    # der Relationseigenschaft (nsubj, ...) verknüpft ist.
    def find_parent_if_rel(self, deprel):
        if self.parent and self.word.deprel == deprel:
            return self.parent

        return None

    # Findet das Verb in der übergeordneten Satzstruktur,
    # dessen Form von dem aktuellen Nomen abhängt, insofern
    # das aktuelle Nomen das Subjekt des Satzes ist.
    #
    # Mitarbeiter steht
    #             _____
    def find_parent_verb(self):
        assert self.word.xpos == "NN"

        return self.find_parent_if_rel("nsubj")

    # Findet Determinative innerhalb von Adnominal-Klauseln,
    # auf die das aktuelle Nomen wegen seiner Eigenschaften: Geschlecht, Kasus und Numerus,
    # Einfluss hat.
    #
    # Der Schüler, dessen Arm gebrochen ist, ging schlafen.
    #              ______
    #
    def find_det_in_adnominal_clauses(self):
        adnominal_clauses = self.find_rel("acl")

        result = []
        for c in adnominal_clauses:
            subj = c.find_multiple_rel(["nsubj", "nsubj:pass"])

            for s in subj:
                det = s.find_det()

                for d in det:
                    result.append(d)

        return result

    def __str__(self):
        return self.word.text

    def __repr__(self):
        return self.word.text

    # Gibt die weiblichen Formen dieses Nomens zurück,
    # falls es sich um ein Nomen handelt, falls dieses
    # in unserer Datenbank überhaupt zu finden ist
    # und falls es dann dazu weibliche Formen gibt.
    def weibliche_formen(self):
        # Gibt es das Wort in unserer Wort-Datenbank?
        lemma_in_db = find_by_lemma(self.word.lemma)

        if not lemma_in_db:
            return None

        weibliche_form_in_db = lemma_in_db["weibliche_formen"]

        if not weibliche_form_in_db:
            return None

        weibliche_formen = json.loads(weibliche_form_in_db)
        weibliche_formen = [find_by_lemma(x) for x in weibliche_formen]

        if not weibliche_formen:
            return None

        return weibliche_formen

    def make_correction(self):
        # Gibt es das Wort in unserer Wort-Datenbank?
        lemma_in_db = find_by_lemma(self.word.lemma)

        if not lemma_in_db:
            print(f"IGNORIERT: word: {self.word.id} {self.word.text}")

            return
            # return {
            #     "type": "INFO",
            #     "taglevel": "2",
            #     "start_char": self.word.start_char,
            #     "end_char": self.word.end_char,
            #     "word": self.word.text,
            #     "short": "Nicht in Datenbank",
            #     "long": "Das Wort wurde ignoriert, da es nicht in der Wort-Datenbank gefunden wurde."
            # }

        weibliche_form_in_db = lemma_in_db["weibliche_formen"]

        if not weibliche_form_in_db:
            print(f"IGNORIERT: word: {self.word.id} {self.word.text}")
            return

        weibliche_formen = json.loads(weibliche_form_in_db)
        weibliche_formen = [find_by_lemma(x) for x in weibliche_formen]

        if not weibliche_formen:
            print(f"IGNORIERT: word: {self.word.id} {self.word.text}")
            return

        print(f"word: {self.word.id} {self.word.text}")
        print(f"parent verb: {self.find_parent_verb()}")
        print(f"amod: {self.find_amod()}")
        print(f"direct det: {self.find_det()}")
        print(f"adnominal det: {self.find_det_in_adnominal_clauses()}")

        logger.debug("Verwendetes Wort (Lemma): {}", self.word.lemma)

        # Der$Die Bäcker?in
        # Die Bäcker?Innen (Singular -> Plural)
        # Bäcker und Bäckerinnen

        def transform(word, new_word, target_gender, target_number, additional_transform_noun, additional_transform_by_words):
            def define_change(word, new_text):
                return {
                    "start_char": word.word.start_char,
                    "end_char": word.word.end_char,
                    "word": word.word.text,
                    "replace_with": new_text,
                }

            changes = []

            # Nomen manipulieren
            new_noun = additional_transform_noun(
                self,
                transform_noun(new_word, self.Case, target_number)
            )

            changes.append(
                define_change(
                    word,
                    new_noun
                )
            )

            # Adjektive manipulieren
            for amod in self.find_amod():
                new_adj = additional_transform_by_words(
                    transform_adjective(amod, self.Case, target_gender, target_number)
                )

                changes.append(
                    define_change(
                        amod,
                        new_adj
                    )
                )

            # Determiner bzw. Artikel manipulieren
            for det in self.find_det():
                new_det = additional_transform_by_words(
                    transform_determiner(det, self.Case, target_gender, target_number)
                )

                changes.append(
                    define_change(
                        det,
                        new_det
                    )
                )

            for det in self.find_det_in_adnominal_clauses():
                changes.append(
                    define_change(
                        det,
                        transform_determiner(det, self.Case, target_gender, target_number),
                        after_transform
                    )
                )

            return changes

        possible_corrections = []

        def after_transform(word, new_text):
            if word.word.xpos == "NN":
                if new_text.endswith("innen"):
                    return new_text[0:-5] + "?Innen"
                elif new_text.endswith("in"):
                    return new_text[0:-2] + "?In"

                return new_text
            else:
                if word.word.text != new_text:
                    return word.word.text + "$" + new_text

            return new_text

        if self.Number == "Sing":
            possible_corrections.append(transform(self, weibliche_formen[0], "Fem", "Sing", after_transform))
            possible_corrections.append(transform(self, weibliche_formen[0], "Fem", "Plur", after_transform))
        else:
            possible_corrections.append(transform(self, weibliche_formen[0], "Fem", "Plur", after_transform))

        return possible_corrections

def make_tree(sent):
    root_word = get_root_word(sent)

    return RecWord(sent, root_word, None)


def do_correct(sentence):
    nlp = stanza.Pipeline(lang='de', processors='tokenize,mwt,pos,lemma,depparse')
    doc = nlp(sentence)

    print(*[
        f'id:{word.id}\tword: {word.text}\tdeprel: {word.deprel}\thead: {word.head}\t lemma: {word.lemma}\t upos: {word.upos}\txpos: {word.xpos}\tfeats: {word.feats if word.feats else "_"}\t'
        for sent in doc.sentences for word in sent.words], sep='\n')

    result = []

    for sent in doc.sentences:
        tree = make_tree(sent)

        inorder = tree.in_order_list()
        for n in inorder:
            if n.word.xpos == "NN":
                corrections = n.make_correction()

                if not corrections:
                    continue

                result.append({
                        "start_char": n.word.start_char,
                        "end_char": n.word.end_char,
                        "word": n.word.text,
                        "possible_corrections": corrections
                })


    return result


# sentence = 'Die Fußspuren der hungrigen Täter sind zu sehen. Zwielichtige Drogenhändler wurden für ihre Informanten-Dienste fürstlich entlohnt.'

# sentence = """Der Übergang in ein neues Millennium hat die Fantasie der Menschen immer zu besonderen Ausflügen angespornt .
# Auch vor dem Sprung ins dritte Jahrtausend ist dies nicht anders .
# Und schon gar nicht , wenn es sich um ein Forschungs- und Anwendungsgebiet handelt , das ohnehin in revolutionärer Wandlung begriffen ist : die Medizin .
# Neue Computerverfahren und molekularbiologische Techniken werden den Körper des Menschen seiner letzten Geheimnisse berauben , ihn genetisch decodieren und durchleuchten , ihn in Computeranimation abbilden und bearbeiten , bis in die letzte Zelle hinein , dreidimensional und farbig .
# Grund genug , danach zu fragen , wie die Medizin des dritten Jahrtausends daherkommen wird : Maschine kontra Mensch , Forschung versus Menschenwürde , Schulmedizin gegen Alternativheilkunde , ungebändigter Pioniergeist oder neue Bescheidenheit ?
# Wohin die Entwicklung der modernen Medizin führen kann und soll , wie sie zu steuern ist und dem Patienten zum Nutzen gereichen kann , machte der Kongreß `` Kultur und Technik im 21. Jahrhundert - Medizin der Zukunft '' jetzt in Düsseldorf zwei Tage lang zum Thema .
# Organisator war das Wissenschaftszentrum Nordrhein-Westfalen .
# Der Versuch einer Einordnung gelang nur streckenweise ;
# zu viele Themen wurden aufgegriffen , Wesentliches blieb unausgesprochen .
# Es gab brilliante Beiträge , manche Diskussionsrunde aber ließ die nötige Schärfe vermissen .
# Doch gerade darin war der Kongreß auch ein Spiegel der Realität .
# Denn die moderne Medizin ist ein buntes Nebeneinander , Gegeneinander und Miteinander von Entwicklungen .
# Als zentrales Gedanken-Motiv schälte sich aber die Sorge um die Stellung des Menschen , des Patienten und des Arztes , in der Heilkunde von morgen heraus .
# Für dieses Problem gibt es allerdings keine allgemeingültige Antwort :
# Die Forschung zugunsten kommender Generationen an alten und verwirrten Menschen , die sich nicht wehren können , das Einbringen von Zellen als Medikament in das Gehirn von Menschen , das erst durch den Zugriff auf abgetriebene Föten möglich wird , und die gerechte Verteilung von medizinischen Leistungen angesichts sich leerender Kassen sind da nur einige Herausforderungen für ein humanes Menschenbild .
# Andere Spannungsfelder sind die Veränderung des Krankheitsbegriffes und die stärkere Betonung der individuellen Veranlagung für eine Krankheit sowie der Wunsch nach einer leidensfreien Gesellschaft , was Hand in Hand mit einer in die Selektion führenden vorgeburtlichen Diagnostik geht und die Sorge Behinderter um ihr Lebensrecht wachsen läßt .
# All dies vermittelt nicht zu Unrecht den Eindruck , daß es mit der Menschlichkeit in der Medizin nicht zum besten steht .
# Das Verhalten der Patienten zur High-Tech-Medizin ist dabei durchaus ambivalent .
# Neben der verbreiteten Kritik an Apparaten und Technik gibt es ein starkes Verlangen von Kranken nach optimaler maschinengestützter Behandlung .
# Weil Vorbeugung und Gesundheitserziehung viel zu kurz kommen , wächst der medizinischen Forschung und der Therapie eine gefährlich hohe Bedeutung zu , weil sie mit zu vielen Hoffnungen befrachtet werden .
# Und manchmal steht dabei der Einsatz in keinem sinnvollen Verhältnis zum Nutzen .
# In Düsseldorf wurde in Erinnerung gerufen , daß die Erhöhung der durchschnittlichen Lebenszeit der Menschen in erster Linie nicht neuen Medikamenten , Operationsverfahren und Therapien zu verdanken ist , sondern der gegenüber früher besseren Ernährung und Hygiene .
# Selbst wenn es Krebs nicht gäbe , läge die Lebenserwartung der Deutschen insgesamt nur zwei Jahre höher , sagte der Heidelberger Krebsforscher Harald zur Hausen .
# Gerade das Thema Krebs zeigt exemplarisch , wo es Fehlentwicklungen im Arzt-Patient-Verhältnis gibt und wo ein rein schulmedizinisch ausgerichteter Denkansatz in der Therapie und in der menschlichen Betreuung der Patienten zu kurz greift .
# Obwohl mehr als 90 Prozent der Bundesbürger auf die Schulmedizin vertrauen , wie eine im Vorfeld des Kongresses durchgeführte Emnid-Umfrage belegt , ist die konventionelle Heilkunde inzwischen stark unter Druck geraten .
# Wie sich alte Frontstellungen allmählich aufzulösen beginnen , zeigte das Kongreß-Symposium über die Grenzen der Schulmedizin in einer `` aggressionsfreien '' Atmosphäre , wie sie - so Gerhard A. Nagel von der Klinik für Tumorbiologie an der Universität Freiburg - noch vor einigen Jahren nicht denkbar gewesen wäre .
# Nagel forderte die Schulmediziner auf , sich mit der inneren Logik der unkonventionellen und der Para-Medizin zu befassen , um die dahinterstehenden Fragen der Patienten aufnehmen zu können .
# Krankheit als Strafe ?"""

# sentence = "Der Beamte, dessen fehlerhafte aber vertrauenswürdige Arbeit seines Kollegen nicht erkannt wurde, geht tanken."
# sentence = "Die Firma, deren pünklicher Bauarbeiter mit seiner Tochter streikte, ging schlafen."
# sentence = "Ein großer Schüler, dessen Arm gebrochen ist, ging schlafen"
# #
# result = do_correct(sentence)
#
# print(sentence)
#
# def replace_in_str(old_str, _from, _to, new_str):
#     first_part = old_str[:_from]
#     middle_part = old_str[_from:_to]
#     last_part = old_str[_to:]
#
#     return first_part + new_str + last_part
#
# for word in result:
#     print(f"Mögliche Korrekturen für das Wort {word['word']}:")
#     print("")
#     for alt in word["possible_corrections"]:
#         alt_sentence = sentence
#
#         for correction in sorted(alt, key=lambda x: x["end_char"], reverse=True):
#             alt_sentence = replace_in_str(alt_sentence, correction["start_char"], correction["end_char"], correction["replace_with"])
#
#         print(alt_sentence)
#
#



