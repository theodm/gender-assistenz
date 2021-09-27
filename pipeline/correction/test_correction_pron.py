from _spacy import spacify_with_coref
from pipeline.correction.correction_pron import generate_possible_corrections_for_pron


def test_singular_pron():
    doc = spacify_with_coref("Er, dessen Bein gebrochen war, geht ein Eis essen.")

    res = generate_possible_corrections_for_pron(doc[0])

    print(res)

    assert {
               'type': '*',
               'changes': [
                   {'text': 'Er', 'from': 0, 'to': 2, 'type': 'NOUN', 'replace_with': 'Er?Sie'},
                   {'text': 'dessen', 'from': 4, 'to': 10, 'type': 'DET', 'replace_with': 'dessen?deren'}
               ]
           } in res[0]

    assert {
               'type': 'PLURAL_*',
               'changes': [
                   {'text': 'Er', 'from': 0, 'to': 2, 'type': 'NOUN', 'replace_with': 'Sie'},
                   {'text': 'dessen', 'from': 4, 'to': 10, 'type': 'DET', 'replace_with': 'deren'},
                   {'text': 'geht', 'from': 31, 'to': 35, 'type': 'VERB', 'replace_with': 'gehen'}
               ]
           } in res[0]


def test_jedermann():
    doc = spacify_with_coref(
        "Das Recht, zur Wahrung und Förderung der Arbeits- und Wirtschaftsbedingungen Vereinigungen zu bilden, ist für jedermann und für alle Berufe.")

    res = generate_possible_corrections_for_pron(doc[17])

    print(res)

    assert {
               'type': '*',
               'changes': [
                   {'text': 'jedermann', 'from': 110, 'to': 119, 'type': 'NOUN', 'replace_with': 'jedermann?jede'}
               ]
           } in res[0]

    assert {
               'type': 'PLURAL_*',
               'changes': [
                   {'text': 'jedermann', 'from': 110, 'to': 119, 'type': 'NOUN', 'replace_with': 'alle'}
               ]
           } in res[0]
