import nltk
from HanTa import HanoverTagger as ht

tagger = ht.HanoverTagger('morphmodel_ger.pgz')

def analyze_without_tokenization(words):
    tags = tagger.tag_sent(words, taglevel=7)

    return tags


def analyze(text):
    words = nltk.word_tokenize(text)

    tags = tagger.tag_sent(words, taglevel=7)

    return tags