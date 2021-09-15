import json
import pathlib

from bottle import route, run, request, template, post, get, static_file
from spacy import displacy

from _spacy import spacify_with_coref
from fiw import find_initial_words
from ntbg import needs_to_be_gendered
from pipeline.full_pipeline import full_pipeline


@post('/analyze')
def index():
    body = request.body.read().decode("UTF-8")

    return json.dumps({"text": body, "infos": full_pipeline(body)})


@get('/displacy')
def _displacy():
    doc = spacify_with_coref(request.query['doc'])

    return displacy.render(doc, style="dep")


@get('/tagging')
def _tagging():
    doc = spacify_with_coref(request.query['doc'])

    result = "<table>"

    for word in doc:
        result = result + f"<tr><td>{word.text}</td><td>{word.pos_}</td><td>{word.tag_}</td><td>{word.morph}</td><td>{word.lemma_}</td></tr>"

    result = result + "</table>"

    return result


@route('/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root=pathlib.Path(__file__).parent.joinpath("client").joinpath("build").resolve())


run(host='localhost', port=8080)
