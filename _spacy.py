import coreferee, spacy
from spacy import displacy
from joblib import Memory

memory = Memory("cachedir")

nlp = spacy.load("de_dep_news_trf")
nlp2 = spacy.load("de_core_news_lg")
nlp2.add_pipe('coreferee')

@memory.cache
def spacify(text):
    return nlp(text)

#ToDo: Warum Cache?
@memory.cache
def spacify_with_coref(text):
    doc2 = nlp2(text)
    doc = nlp(text)

    doc._.coref_chains = doc2._.coref_chains

    return doc


def displayc(text):
    doc = spacify(text)

    displacy.serve(doc, style="dep")

#
# for word in doc:
#     print(word.text + "," + word.tag_ + "," + word.pos_)
#
#print(spacy.explain("ag"))
#
#
#
#
# #nlp.add_pipe('coreferee')
#
# #sentence = "Wann die Spiele auf den Markt kommen sollen , ist bisher ebensowenig bekannt , wie die Höhe der Summe , die Electronic Arts an den Besitzer der Rechte an Harry Potter , Time Warner , bezahlt hat ."
# #sentence = "Richard, dessen Vater krank war, geht ein Eis essen. Danach ging er spielen."
# #sentence = "Die kleine Jennifer, deren Vater Elektriker ist, schaut die Sendung mit der Maus."
# #sentence = "Klesch und Kleber sind bereits neuer Betreiber in Hessen."
# sentence = "Klesch und Kleber sind bereits neue Betreiber in Hessen."
# sentence = "Seit dem heutigen Mittwochmorgen kursierten an der Frankfurter Börse Gerüchte, denen zufolge Telekom-Chef Ron Sommer zurücktreten wird."
# sentence = "Die Met@box 1000 soll interaktives Fernsehen ermöglichen , MP3-Dateien abspielen und über einen eingebauten DVD-Spieler verfügen ."
# sentence = "Und auch die zahlreichen T-Online-Flatrate-Kunden hätten das Netz bisher nicht überlasten können."
# doc = nlp(sentence)
#
# #doc._.coref_chains.print()
#
# for word in doc:
#     print(word)
#
#
#
# displacy.serve(doc, style='dep')



