import coreferee, spacy
from spacy import displacy

nlp = spacy.load("de_dep_news_trf")

nlp.add_pipe('coreferee')

sentence = "Wann die Spiele auf den Markt kommen sollen , ist bisher ebensowenig bekannt , wie die Höhe der Summe , die Electronic Arts an den Besitzer der Rechte an Harry Potter , Time Warner , bezahlt hat ."

doc = nlp(sentence)

for word in doc:
    print(word)

displacy.serve(doc, style='dep')