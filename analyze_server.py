import json

from bottle import route, run, request, template, post,get
from nltk.corpus import udhr

from analyze import analyze, analyze_without_tokenization
from corpus_analyze import read_tiger_corpus
from stanza_test import do_correct


def flatten(list_of_lists):
    return [item for sublist in list_of_lists for item in sublist]

@get('/analyze')
def index():
    # text = "Dies ist ein Zeitungsartikel und hier könnte Ihre Werbung stehen! Friseure, hier ein Test!" #request.body.read()

    words = read_tiger_corpus()

    result = analyze_without_tokenization(words[0:50000])

    return json.dumps(result)

@post('/do_correction')
def do_correction():
    text = str(request.body.read(), encoding="utf-8")

    result = do_correct(text)

    return json.dumps({
        "text": text,
        "result": result
    })

run(host='localhost', port=8080)