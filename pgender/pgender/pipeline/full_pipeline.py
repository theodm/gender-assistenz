from pgender._spacy import spacify_with_coref
from pgender.fiw import find_initial_words
from pgender.ntbg import needs_to_be_gendered
from pgender.pipeline.correction.correction import generate_possible_corrections

def full_pipeline(text):
    #
    # Zunächst führen wir SpacY aus um Grammatikinformationen initial
    # zu erhalten.
    #
    doc = spacify_with_coref(text)

    #
    # 1. Schritt: Suche nach allen maskulinen Formen
    #
    initial_words = find_initial_words(doc)

    #
    # 2. Schritt: Überprüfung der gefundenen Vorkommen, ob es sich um das generische Maskulinum handelt.
    #
    result = []
    for word in initial_words:
        ntbg = needs_to_be_gendered(doc, word[0])

        if ntbg[0]:
            #
            # 3. Schritt: Erstellung von Korrekturvorschlägen.
            #
            result.append({
                "from": word[0].idx,
                "to": word[0].idx + len(word[0].text),
                "possibleCorrections": generate_possible_corrections(word[0]),
                "shouldBeGendered": ntbg[0],
                "reasonNotGendered": []
            })

            continue

        result.append({
            "from": word[0].idx,
            "to": word[0].idx + len(word[0].text),
            "possibleCorrections": [],
            "shouldBeGendered": ntbg[0],
            "reasonNotGendered": ntbg[1]
        })

    return result


