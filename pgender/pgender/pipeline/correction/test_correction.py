from pgender._spacy import spacify_with_coref
from pgender.pipeline.correction.correction import generate_possible_corrections_plural, \
    generate_possible_corrections_singular


def test_simple_singular_with_case_preserve():
    doc = spacify_with_coref("Der Schüler geht ein Eis essen.")

    res = generate_possible_corrections_singular(doc[1])

    print(res)

    assert {
               "type": "*",
               "changes": [
                   {'from': 0, 'replace_with': 'Der?Die', 'to': 3, 'type': 'DET'},
                   {'from': 4, 'replace_with': 'Schüler?In', 'to': 11, 'type': 'NOUN'}
               ]
           } in res

    assert {
               "type": "PLURAL_*",
               "changes": [
                   {'from': 0, 'to': 3, 'type': 'DET', 'replace_with': 'Die'},
                   {'from': 12, 'to': 16, 'type': 'VERB', 'replace_with': 'gehen'},
                   {'from': 4, 'to': 11, 'type': 'NOUN', 'replace_with': 'Schüler?Innen'},
               ]
           } in res


def test_singular_unbestimmter_artikel():
    doc = spacify_with_coref("Ein Schüler geht ein Eis essen.")

    res = generate_possible_corrections_singular(doc[1])

    print(res)

    assert {
               "type": "*",
               "changes": [
                   {'from': 0, 'replace_with': 'Ein?Eine', 'to': 3, 'type': 'DET'},
                   {'from': 4, 'replace_with': 'Schüler?In', 'to': 11, 'type': 'NOUN'}
               ]
           } in res

    assert {
               "type": "PLURAL_*",
               "changes": [
                   {'from': 0, 'to': 4, 'type': 'DET', 'replace_with': ''},
                   {'from': 12, 'to': 16, 'type': 'VERB', 'replace_with': 'gehen'},
                   {'from': 4, 'to': 11, 'type': 'NOUN', 'replace_with': 'Schüler?Innen'}
               ]
           } in res


def test_simple_plural():
    doc = spacify_with_coref("Die Schüler gehen ein Eis essen.")

    res = generate_possible_corrections_plural(doc[1])

    print(res)

    assert {
               "type": "*",
               "changes": [{
                   'from': 4,
                   'to': 11,
                   'type': 'NOUN',
                   'replace_with': 'Schüler?Innen'
               }]
           } in res

    assert {
               "type": "BOTH_FORMS",
               "changes": [{'from': 4, 'to': 11, 'type': 'NOUN', 'replace_with': 'Schülerinnen und Schüler'}]
           } in res


def test_und_form_nach_dem_und_plural():
    doc = spacify_with_coref("Die Schüler und Lehrer gehen ein Eis essen.")

    res = generate_possible_corrections_plural(doc[3])

    print(res)

    assert {
               "type": "BOTH_FORMS",
               "changes": [
                   {'from': 16, 'replace_with': 'Lehrerinnen und Lehrer', 'to': 22, 'type': 'NOUN'},
                   {'from': 11, 'replace_with': ',', 'to': 16, 'type': 'CONJ'}
               ]
           } in res


def test_und_form_vor_dem_und_plural():
    doc = spacify_with_coref("Die Schüler und Lehrer gehen ein Eis essen.")

    res = generate_possible_corrections_plural(doc[1])

    print(res)

    assert {
               "type": "BOTH_FORMS",
               "changes": [{'from': 4, 'to': 11, 'type': 'NOUN', 'replace_with': 'Schülerinnen, Schüler'}]
           } in res


def test_oder():
    doc = spacify_with_coref("Die Schüler oder Lehrer gehen ein Eis essen.")

    res = generate_possible_corrections_plural(doc[3])

    print(res)

    assert {
        "type": "BOTH_FORMS",
        "changes": [
                       {'from': 17, 'replace_with': 'Lehrerinnen oder Lehrer', 'to': 23, 'type': 'NOUN'},
                       {'from': 11, 'replace_with': ',', 'to': 17, 'type': 'CONJ'}
                   ] in res
    }


def test_zusammengesetztes_unbekanntes_plural():
    doc = spacify_with_coref("Die Vielsurfer gehen ein Eis essen.")

    res = generate_possible_corrections_plural(doc[1])

    assert {
               "type": "*",
               "changes": [{
                   'from': 4,
                   'to': 14,
                   'type': 'NOUN',
                   'replace_with': 'Vielsurfer?Innen'
               }]
           } in res

    assert {
               "type": "BOTH_FORMS",
               "changes": [{'from': 4, 'to': 14, 'type': 'NOUN', 'replace_with': 'Vielsurferinnen und Vielsurfer'}]
           } in res

# ToDo: Plural mit Preserve Case
