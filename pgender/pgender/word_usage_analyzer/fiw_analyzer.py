import sys

from conllu import parse_incr
from loguru import logger

from pgender._spacy import spacify, spacify_with_coref
from pgender.fiw import find_initial_words
from pgender.ntbg import needs_to_be_gendered

logger.remove()
logger.add(sys.stderr, level="INFO")

data_file = open("corpora/de_hdt-ud-train.conllu", "r", encoding="utf-8")

i = 0
for tokenlist in parse_incr(data_file):
    sentence = [x["form"] for x in tokenlist]
    sentence = " ".join(sentence)

    i = i + 1

    doc = spacify_with_coref(sentence)

    result = find_initial_words(doc)
    if result:
        s = ""
        for f in result:
            s = s + str(f) + f":{needs_to_be_gendered(doc, f[0], [x[0] for x in result])}), "

        print(f"{sentence} : {s}")
    # doc._.coref_chains.print()


# Die Mitnahme der Handy-Nummer bei einem Wechsel des Mobilfunkanbieters wird nun erst ab dem November nächsten Jahres möglich sein . ??
# Das zwischen den beiden Unternehmen vereinbarte Entgelt soll " deutlich " unter dem derzeitigen regulierten Preis liegen , den Telekommunikationsunternehmen für die gleiche Leistung an die Deutsche Telekom zahlen müssen .
# Doch ein Fehler erlaubte es jedermann , E-Mails an einen großen Teil der eingetragenen Nutzer zu verschicken .
# In dem zweiten Vergütungsbericht der Bundesregierung an den Bundestag , der vom Kabinett verabschiedet wurde , wird gefordert , dass digitale Speichermedien zukünftig der Vergütungspflicht unterliegen sollen . <-- Cooles Beispiel
# Wer vom Online-Auftritt des Szenesprachen-Dudens viel erwartet , wird wohl eher enttäuscht sein
# Siehe dazu auch den Bericht " Saudi Arabien sperrt wegen Pornographie Zugang zu den Yahoo-Clubs - Die Bürger des Königreichs können nur über einen Proxy , auf dem Filter installiert sind , ins Internet " in Telepolis .
# Das am heutigen Donnerstag von der Telekom vorgelegte Angebot zur Großhandelsflatrate stößt beim Verband der Anbieter von Telekommunikations- und Mehrwertdiensten ( VATM ) auf Kritik .