import spacy

nlp = spacy.load("de_dep_news_trf")

sentence = "Dies ist ein Satz."

doc = nlp(sentence)

for sent in doc.sents:
    for word in sent.words:
        print(word)
