import coreferee, spacy
from spacy import displacy

nlp = spacy.load("de_dep_news_trf")

def spacify(text):
    return nlp(text)


#
# print(spacy.explain("nk"))
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
# sentence = "Und auch die zahlreichen T-Online-Flatrate-Kunden hätten das Netz bisher nicht überlasten können ."
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



