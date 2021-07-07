import json

import stanza

# stanza.download('de')
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
        return self.find_multiple_rel([deprel])

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

        # target_gender=Masc|Neut|Fem
        # target_number=Sing|Plur

        gender_as_index = {
            "Masc": 0,
            "Neut": 1,
            "Fem": 2
        }

        case_as_index = {
            "Nom": 0,
            "Dat": 1,
            "Acc": 2,
            "Gen": 3
        }

        def modify_det(det, target_gender, target_number):
            if det.word.xpos == "ART":
                modify_art(det, target_gender, target_number)
            elif det.word.xpos in ["PRELAT", "PRELS"]:
                modify_prelat(det, target_gender, target_number)
            else:
                assert False

            return

        def modify_prelat(det, target_gender, target_number):
            assert det.word.xpos == "PRELAT" or det.word.xpos == "PRELS"

            # https://www.deutschplus.net/pages/Relativpronomen_der_die_das
            relativ_pronomen_derdiedas = [
                "der",  # maskulin, nominativ
                "dem",  # maskulin, dativ
                "den",  # maskulin, akkusativ
                "dessen",  # maskulin, genitiv

                "das",  # neutrum, nominativ
                "dem",  # neutrum, dativ
                "das",  # neutrum, akkusativ
                "dessen",  # neutrum, genitiv

                "die",  # feminin, nominativ
                "der",  # feminin, dativ
                "die",  # feminin, akkusativ
                "deren",  # feminin, genitiv

                "die",  # plural, nominativ
                "denen",  # plural, dativ
                "die",  # plural, akkusativ
                "deren"  # plural, genitiv
            ]

            relativ_pronomen_welche = [
                "welcher",  # maskulin, nominativ
                "welchem",  # maskulin, dativ
                "welchen",  # maskulin, akkusativ
                "-",  # maskulin, genitiv

                "welches",  # neutrum, nominativ
                "welchem",  # neutrum, dativ
                "welches",  # neutrum, akkusativ
                "-",  # neutrum, genitiv

                "welche",  # feminin, nominativ
                "welcher",  # feminin, dativ
                "welches",  # feminin, akkusativ
                "-",  # feminin, genitiv

                "welche",  # plural, nominativ
                "welchen",  # plural, dativ
                "welche",  # plural, akkusativ
                "-"  # plural, genitiv
            ]

            lower_det = det.word.text.lower()

            derdiedas_det = lower_det in relativ_pronomen_derdiedas
            welche_det = lower_det in relativ_pronomen_welche

            # Kasus soll gleich bleiben
            target_case = det.Case

            assert derdiedas_det | welche_det

            neuer_det = ""
            if derdiedas_det:
                if target_number == "Plur":
                    neuer_det = relativ_pronomen_derdiedas[3 * 4 + case_as_index[target_case]]
                else:
                    neuer_det = relativ_pronomen_derdiedas[gender_as_index[target_gender] * 4 + case_as_index[target_case]]

            if welche_det:
                if target_number == "Plur":
                    neuer_det = relativ_pronomen_welche[3 * 4 + case_as_index[target_case]]
                else:
                    neuer_det = relativ_pronomen_welche[gender_as_index[target_gender] * 4 + case_as_index[target_case]]

            print("neuer det: " + neuer_det)

        def modify_art(det, target_gender, target_number):
            assert det.word.xpos == "ART"

            # https://de.serlo.org/deutsch-als-fremdsprache/31129/unbestimmter-artikel
            unbestimmte_artikel = [
                "ein",  # maskulin, nominativ
                "einem",  # maskulin, dativ
                "einen",  # maskulin, akkusativ
                "eines",  # maskulin, genitiv

                "ein",  # neutrum, nominativ
                "einem",  # neutrum, dativ
                "ein",  # neutrum, akkusativ
                "eines",  # neutrum, genitiv

                "eine",  # feminin, nominativ
                "einer",  # feminin, dativ
                "eine",  # feminin, akkusativ
                "einer",  # feminin, genitiv

                "", # plural, nominativ
                "", # plural, dativ
                "", # plural, akkusativ
                "" # plural, genitiv
            ]

            # https://de.serlo.org/deutsch-als-fremdsprache/31114/bestimmter-artikel
            bestimmte_artikel = [
                "der",  # maskulin, nominativ
                "dem",  # maskulin, dativ
                "den",  # maskulin, akkusativ
                "des",  # maskulin, genitiv

                "das",  # neutrum, nominativ
                "dem",  # neutrum, dativ
                "das",  # neutrum, akkusativ
                "des",  # neutrum, genitiv

                "die",  # feminin, nominativ
                "der",  # feminin, dativ
                "die",  # feminin, akkusativ
                "der",  # feminin, genitiv

                "die", # plural, nominativ
                "den", # plural, dativ
                "die", # plural, akkusativ
                "der" # plural, genitiv
            ]

            lower_det = det.word.text.lower()

            unbestimmter_det = lower_det in unbestimmte_artikel
            bestimmter_det = lower_det in bestimmte_artikel

            # Kasus soll gleich bleiben
            target_case = det.Case

            assert unbestimmter_det | bestimmter_det


            neuer_det = ""
            if unbestimmter_det:
                if target_number == "Plur":
                    neuer_det = unbestimmte_artikel[3 * 4 + case_as_index[target_case]]
                else:
                    neuer_det = unbestimmte_artikel[gender_as_index[target_gender] * 4 + case_as_index[target_case]]

            if bestimmter_det:
                if target_number == "Plur":
                    neuer_det = bestimmte_artikel[3 * 4 + case_as_index[target_case]]
                else:
                    neuer_det = bestimmte_artikel[gender_as_index[target_gender] * 4 + case_as_index[target_case]]

            print("neuer det: " + neuer_det)

        for d in self.find_det():
            modify_det(d, "Fem", "Sing")

        for d in self.find_det_in_adnominal_clauses():
            modify_det(d, "Fem", "Sing")


def make_tree(sent):
    root_word = get_root_word(sent)

    return RecWord(sent, root_word, None)


def do_correct(sentence):
    nlp = stanza.Pipeline(lang='de', processors='tokenize,mwt,pos,lemma,depparse')
    doc = nlp(sentence)

    print(*[
        f'id:{word.id}\tword: {word.text}\tdeprel: {word.deprel}\thead: {word.head}\t lemma: {word.lemma}\t upos: {word.upos}\txpos: {word.xpos}\tfeats: {word.feats if word.feats else "_"}\t'
        for sent in doc.sentences for word in sent.words], sep='\n')

    changes = []

    for sent in doc.sentences:
        tree = make_tree(sent)

        inorder = tree.in_order_list()

        for n in inorder:
            if n.word.xpos == "NN":
                n.make_correction()
                print()

        # for word in sent.words:
        #     print(f'id:{word.id}\tword: {word.text}\tdeprel: {word.deprel}\thead: {word.head}\t lemma: {word.lemma}\t upos: {word.upos}\txpos: {word.xpos}\tfeats: {word.feats if word.feats else "_"}\t')
        #
        #     if not word.feats:
        #         changes.append({
        #             "type": "INFO",
        #             "taglevel": "5",
        #             "start_char": word.start_char,
        #             "end_char": word.end_char,
        #             "word": word.text,
        #             "short": "Keine Features",
        #             "long": "Das Wort wurde nicht beachtet, da es keine morphologischen Eigenschaften zugewiesen bekommen hat."
        #         })
        #         continue
        #
        #     word_is_plural = "Number=Plur" in word.feats
        #     word_is_masc = "Gender=Masc" in word.feats
        #
        #     if not word_is_plural:
        #         changes.append({
        #             "type": "INFO",
        #             "taglevel": "4",
        #             "start_char": word.start_char,
        #             "end_char": word.end_char,
        #             "word": word.text,
        #             "short": "Nicht Plural",
        #             "long": "Das Wort wurde ignoriert, da es nicht in Plural geschrieben wurde. (Bisher wird nur Plural unterstützt)"
        #         })
        #         continue
        #
        #     if not word_is_masc:
        #         changes.append({
        #             "type": "INFO",
        #             "taglevel": "2",
        #             "start_char": word.start_char,
        #             "end_char": word.end_char,
        #             "word": word.text,
        #             "short": "Nicht Maskulin",
        #             "long": "Das Wort wurde ignoriert, da es nicht in maskuliner Form geschrieben wurde."
        #         })
        #         continue
        #
        #     lemma_in_db = find_by_lemma(word.lemma)
        #
        #     if not lemma_in_db:
        #         changes.append({
        #             "type": "INFO",
        #             "taglevel": "2",
        #             "start_char": word.start_char,
        #             "end_char": word.end_char,
        #             "word": word.text,
        #             "short": "Nicht in Datenbank",
        #             "long": "Das Wort wurde ignoriert, da es nicht in der Wort-Datenbank gefunden wurde."
        #         })
        #         continue
        #
        #     weibliche_formen = json.loads(lemma_in_db["weibliche_formen"])
        #     weibliche_formen = [find_by_lemma(x) for x in weibliche_formen]
        #
        #     case = regex_first_or_none("Case=(Gen|Nom|Dat|Acc)", word.feats)
        #
        #     mapping = {
        #         "Nom": "nominativ_plural",
        #         "Gen": "genitiv_plural",
        #         "Dat": "dativ_plural",
        #         "Acc": "akkusativ_plural",
        #     }
        #
        #     changes.append({
        #         "type": "REPLACE",
        #         "taglevel": "1",
        #         "start_char": word.start_char,
        #         "end_char": word.end_char,
        #         "word": word.text,
        #         "replace_with": [w[mapping[case]] for w in weibliche_formen],
        #     })

    print([x for x in changes if x["type"] == "REPLACE"])

    return changes


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
sentence = "Ein verwirrter Schüler, dessen Arm gebrochen ist, ging schlafen"

do_correct(sentence)
