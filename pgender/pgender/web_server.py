import json

from bottle import route, run, request, template, post, get

from pgender._spacy import spacify_with_coref
from pgender.fiw import find_initial_words
from pgender.ntbg import needs_to_be_gendered

@post('/analyze')
def index():
    body = request.body.read().decode("UTF-8")

    doc = spacify_with_coref(body)

    iw = find_initial_words(doc)

    result = []
    for f in iw:
        ntbg = needs_to_be_gendered(doc, f[0])

        result.append({
            "from": f[0].idx,
            "to": f[0].idx + len(f[0].text),
            "shouldBeGendered": ntbg[0],
            "reasonNotGendered": ntbg[1]
        })

    print(json.dumps({"text": body, "infos": result}))
    return json.dumps({"text": body, "infos": result})


run(host='localhost', port=8080)
