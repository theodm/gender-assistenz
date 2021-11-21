from _spacy import spacify_with_coref
from pipeline.correction.correction2 import generate_possible_corrections


def test_simple_singular_with_case_preserve():
    doc = spacify_with_coref("Der Schüler geht ein Eis essen.")

    res, e = generate_possible_corrections([doc[1]])

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
                   {'from': 4, 'to': 11, 'type': 'NOUN', 'replace_with': 'Schüler?Innen'},
                   {'from': 12, 'to': 16, 'type': 'VERB', 'replace_with': 'gehen'},
               ]
           } in res


def test_singular_unbestimmter_artikel():
    doc = spacify_with_coref("Ein Schüler geht ein Eis essen.")

    res, e = generate_possible_corrections([doc[1]])

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
                   {'from': 4, 'to': 11, 'type': 'NOUN', 'replace_with': 'Schüler?Innen'},
                   {'from': 12, 'to': 16, 'type': 'VERB', 'replace_with': 'gehen'},
               ]
           } in res


def test_simple_plural():
    doc = spacify_with_coref("Die Schüler gehen ein Eis essen.")

    res, e = generate_possible_corrections([doc[1]])

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

    res, e = generate_possible_corrections([doc[3]])

    print(res)

    assert {
               "type": "BOTH_FORMS",
               "changes": [
                   {'from': 16, 'replace_with': 'Lehrerinnen und Lehrer', 'to': 22, 'type': 'NOUN'},
                   {'from': 11, 'replace_with': ', ', 'to': 16, 'type': 'CONJ'},
               ]
           } in res


def test_und_form_vor_dem_und_plural():
    doc = spacify_with_coref("Die Schüler und Lehrer gehen ein Eis essen.")

    res, e = generate_possible_corrections([doc[1]])

    print(res)

    assert {
               "type": "BOTH_FORMS",
               "changes": [{'from': 4, 'to': 11, 'type': 'NOUN', 'replace_with': 'Schülerinnen, Schüler'}]
           } in res


def test_oder():
    doc = spacify_with_coref("Die Schüler oder Lehrer gehen ein Eis essen.")

    res, e = generate_possible_corrections([doc[3]])

    print(res)

    assert {
        "type": "BOTH_FORMS",
        "changes": [
                       {'from': 11, 'replace_with': ',', 'to': 17, 'type': 'CONJ'},
                       {'from': 17, 'replace_with': 'Lehrerinnen oder Lehrer', 'to': 23, 'type': 'NOUN'},
                   ] in res
    }


def test_zusammengesetztes_unbekanntes_plural():
    doc = spacify_with_coref("Die Vielsurfer gehen ein Eis essen.")

    res, e = generate_possible_corrections([doc[1]])

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


def test_singular_to_plural_with_adj_positiv_unbestimmt_preserve_case():
    doc = spacify_with_coref("Ein fleißiger Schüler geht ein Eis essen.")

    res, e = generate_possible_corrections([doc[2]])

    print(res)

    assert {
               "type": "PLURAL_*",
               "changes": [
                   {'from': 0, 'to': 4, 'type': 'DET', 'replace_with': ''},
                   {'from': 4, 'to': 13, 'type': 'ADJ', 'replace_with': 'Fleißige'},
                   {'from': 14, 'to': 21, 'type': 'NOUN', 'replace_with': 'Schüler?Innen'},
                   {'from': 22, 'to': 26, 'type': 'VERB', 'replace_with': 'gehen'},
               ]
           } in res


def test_singular_to_plural_with_adj_positiv():
    doc = spacify_with_coref("Der fleißige Schüler geht ein Eis essen.")

    res, e = generate_possible_corrections([doc[2]])

    print(res)

    assert {
               "type": "PLURAL_*",
               "changes": [
                   {'from': 0, 'to': 3, 'type': 'DET', 'replace_with': 'Die'},
                   {'from': 4, 'to': 12, 'type': 'ADJ', 'replace_with': 'fleißigen'},
                   {'from': 13, 'to': 20, 'type': 'NOUN', 'replace_with': 'Schüler?Innen'},
                   {'from': 21, 'to': 25, 'type': 'VERB', 'replace_with': 'gehen'},
               ]
           } in res


def test_singular_to_plural_with_adj_komparativ():
    doc = spacify_with_coref("Der fleißigere Schüler geht ein Eis essen.")

    res, e = generate_possible_corrections([doc[2]])

    print(res)

    assert {
               "type": "PLURAL_*",
               "changes": [
                   {'from': 0, 'to': 3, 'type': 'DET', 'replace_with': 'Die'},
                   {'from': 4, 'to': 14, 'type': 'ADJ', 'replace_with': 'fleißigeren'},
                   {'from': 15, 'to': 22, 'type': 'NOUN', 'replace_with': 'Schüler?Innen'},
                   {'from': 23, 'to': 27, 'type': 'VERB', 'replace_with': 'gehen'},
               ]
           } in res

def test_singular_to_plural_with_adj_superlativ():
    doc = spacify_with_coref("Der fleißigste Schüler geht ein Eis essen.")

    res, e = generate_possible_corrections([doc[2]])

    print(res)

    assert {
               "type": "PLURAL_*",
               "changes": [
                   {'from': 0, 'to': 3, 'type': 'DET', 'replace_with': 'Die'},
                   {'from': 4, 'to': 14, 'type': 'ADJ', 'replace_with': 'fleißigsten'},
                   {'from': 15, 'to': 22, 'type': 'NOUN', 'replace_with': 'Schüler?Innen'},
                   {'from': 23, 'to': 27, 'type': 'VERB', 'replace_with': 'gehen'},
               ]
           } in res

def test_singular_aux():
    doc = spacify_with_coref("Der Benutzer soll den PC neu starten.")

    res, e = generate_possible_corrections([doc[1]])

    print(res)

    assert {
               'type': '*',
                'changes': [
                    {'from': 0, 'to': 3, 'type': 'DET', 'replace_with': 'Der?Die'},
                    {'from': 4, 'to': 12, 'type': 'NOUN', 'replace_with': 'Benutzer?In'}
                ]
           } in res

    assert {
               'type': 'PLURAL_*',
               'changes': [
                   {'from': 0, 'to': 3, 'type': 'DET', 'replace_with': 'Die'},
                   {'from': 4, 'to': 12, 'type': 'NOUN', 'replace_with': 'Benutzer?Innen'},
                   {'from': 13, 'to': 17, 'type': 'VERB', 'replace_with': 'sollen'}
               ]
           } in res


def test_pron():
    doc = spacify_with_coref("Der Benutzer, dessen PC abgestürzt ist, soll den PC neu starten.")

    res, e = generate_possible_corrections([doc[1]])

    assert {
        "type": "*",
        "changes": [
            {'from': 0, 'to': 3, 'type': 'DET', 'replace_with': 'Der?Die'},
            {'from': 4, 'to': 12, 'type': 'NOUN', 'replace_with': 'Benutzer?In'},
            {'from': 14, 'to': 20, 'type': 'DET', 'replace_with': 'dessen?deren'}
        ]
    } in res


    assert {
       'type': 'PLURAL_*',
       'changes': [
           {'from': 0, 'to': 3, 'type': 'DET', 'replace_with': 'Die'},
           {'from': 4, 'to': 12, 'type': 'NOUN', 'replace_with': 'Benutzer?Innen'},
           {'from': 14, 'to': 20, 'type': 'DET', 'replace_with': 'deren'},
           {'from': 40, 'to': 44, 'type': 'VERB', 'replace_with': 'sollen'}
       ]
   } in res


def test_pron_kein():
    doc = spacify_with_coref("In einem Bereich gab es in diesem Jahr keinen Sieger.")

    res, e = generate_possible_corrections([doc[9]])

    assert {
               'type': 'PLURAL_*',
               'changes': [
                   {'from': 39, 'to': 45, 'type': 'DET', 'replace_with': 'keine'},
                   {'from': 46, 'to': 52, 'type': 'NOUN', 'replace_with': 'Sieger?Innen'}
               ]
           } in res


    assert {
               'type': '*',
               'changes': [
                   {'from': 39, 'to': 45, 'type': 'DET', 'replace_with': 'keinen?keine'},
                   {'from': 46, 'to': 52, 'type': 'NOUN', 'replace_with': 'Sieger?In'}
               ]
           } in res

def test_pron_dies():
    doc = spacify_with_coref("Wie angekündigt trennte die Telekom auch diesen Anbieter vom Netz.")

    res, e = generate_possible_corrections([doc[7]])

    print(res)

    assert {
        'type': '*',
        'changes': [
            {'from': 41, 'to': 47, 'type': 'DET', 'replace_with': 'diesen?diese'},
            {'from': 48, 'to': 56, 'type': 'NOUN', 'replace_with': 'Anbieter?In'}
        ]
    } in res

    assert {
        'type': 'PLURAL_*',
        'changes': [
            {'from': 41, 'to': 47, 'type': 'DET', 'replace_with': 'diese'},
            {'from': 48, 'to': 56, 'type': 'NOUN', 'replace_with': 'Anbieter?Innen'}
        ]
    } in res

def test_pron_jen():
    doc = spacify_with_coref("Wie angekündigt trennte die Telekom auch jenen Anbieter vom Netz.")

    res, e = generate_possible_corrections([doc[7]])

    print(res)

    assert {
        'type': '*',
        'changes': [
            {'from': 41, 'to': 46, 'type': 'DET', 'replace_with': 'jenen?jene'},
            {'from': 47, 'to': 55, 'type': 'NOUN', 'replace_with': 'Anbieter?In'}
        ]
    } in res

    assert {
        'type': 'PLURAL_*',
        'changes': [
            {'from': 41, 'to': 46, 'type': 'DET', 'replace_with': 'jene'},
            {'from': 47, 'to': 55, 'type': 'NOUN', 'replace_with': 'Anbieter?Innen'}
        ]
    } in res

def test_pron_jed():
    doc = spacify_with_coref("Es würden aber auch Gespräche mit jedem anderen Anbieter geführt, der meine, ein entsprechendes Angebot machen zu können.")

    res, e = generate_possible_corrections([doc[8]])

    print(res)

    assert {
        'type': '*',
        'changes': [
            {'from': 34, 'to': 39, 'type': 'DET', 'replace_with': 'jedem?jeder'},
            {'from': 48, 'to': 56, 'type': 'NOUN', 'replace_with': 'Anbieter?In'},
            {'from': 66, 'to': 69, 'type': 'DET', 'replace_with': 'der?die'}
        ]
    } in res

    assert {
        'type': 'PLURAL_*',
        'changes': [
            {'from': 34, 'to': 39, 'type': 'DET', 'replace_with': 'allen'},
            {'from': 40, 'to': 47, 'type': 'ADJ', 'replace_with': 'anderen'},
            {'from': 48, 'to': 56, 'type': 'NOUN', 'replace_with': 'Anbieter?Innen'},
            {'from': 66, 'to': 69, 'type': 'DET', 'replace_with': 'die'},
            {'from': 70, 'to': 75, 'type': 'VERB', 'replace_with': 'meinen'}
        ]
    } in res
def test_pron_er():
    doc = spacify_with_coref("Der Benutzer sagte, er sei vorsichtig vorgegangen.")

    res, e = generate_possible_corrections([doc[1]])

    print(res)


def test_pron_sein():
    doc = spacify_with_coref("Nach seiner Aussage würde zwar sein Buchhalter daran glauben , aber nicht seine Kinder - und die wüssten viel mehr vom Internet als er .")

    res, e = generate_possible_corrections([doc[6]])

    print(res)

def test_adj_without_morph():
    doc = spacify_with_coref("""Nach Angaben der Freiburger " Aktionärsgemeinschaft Metabox " soll ein Berliner Immobilienunternehmer Kopf der Investorengruppe sein .""")

    res, e = generate_possible_corrections([doc[11]])

    assert res, e == [
        {
            'type': '*',
            'changes': [
                {'from': 67, 'to': 70, 'type': 'DET', 'replace_with': 'ein?eine'},
                {'from': 80, 'to': 101, 'type': 'NOUN', 'replace_with': 'Immobilienunternehmer?In'}
            ]
        },
        {
            'type': 'PLURAL_*',
            'changes': [
                {'from': 62, 'to': 66, 'type': 'VERB', 'replace_with': 'sollen'},
                {'from': 67, 'to': 71, 'type': 'DET', 'replace_with': ''},
                # ToDo: Das macht eigentlich keinen Sinn
                {'from': 71, 'to': 79, 'type': 'ADJ', 'replace_with': 'Berline'},
                {'from': 80, 'to': 101, 'type': 'NOUN', 'replace_with': 'Immobilienunternehmer?Innen'}
            ]
        }
    ]

def test_adj_coref_1():
    doc = spacify_with_coref("""Der Schüler geht sein Geld zählen.""")

    res, e = generate_possible_corrections([doc[1], doc[3]])

    assert res, e == [
        {
            'type': '*',
            'changes': [
                {
                    'from': 0,
                    'to': 3,
                    'type': 'DET',
                    'replace_with': 'Der?Die'
                },
                {
                    'from': 4,
                    'to': 11,
                    'type': 'NOUN',
                    'replace_with': 'Schüler?In'
                },
                {
                    'from': 17,
                    'to': 21,
                    'type': 'DET',
                    'replace_with': 'sein?ihr'
                }
            ]
        },
        {
            'type': 'PLURAL_*',
            'changes': [
                {
                    'from': 0,
                    'to': 3,
                    'type':'DET',
                    'replace_with': 'Die'
                },
                {
                    'from': 4,
                    'to': 11,
                    'type': 'NOUN',
                    'replace_with': 'Schüler?Innen'
                },
                {
                    'from': 12,
                    'to': 16,
                    'type': 'VERB',
                    'replace_with': 'gehen'
                },
                {
                    'from': 17,
                    'to': 21,
                    'type': 'DET',
                    'replace_with': 'ihr'
                }
            ]
        }
    ]


def test_singular_pron():
    doc = spacify_with_coref("Er, dessen Bein gebrochen war, geht ein Eis essen.")

    res, e = generate_possible_corrections([doc[0]])

    print(res)

    assert {
               'type': '*',
               'changes': [
                   {'from': 0, 'to': 2, 'type': 'DET', 'replace_with': 'Er?Sie'},
                   {'from': 4, 'to': 10, 'type': 'DET', 'replace_with': 'dessen?deren'}
               ]
           } in res

    assert {
               'type': 'PLURAL_*',
               'changes': [
                   {'from': 0, 'to': 2, 'type': 'DET', 'replace_with': 'Sie'},
                   {'from': 4, 'to': 10, 'type': 'DET', 'replace_with': 'deren'},
                   {'from': 31, 'to': 35, 'type': 'VERB', 'replace_with': 'gehen'}
               ]
           } in res


def test_jedermann():
    doc = spacify_with_coref(
        "Das Recht, zur Wahrung und Förderung der Arbeits- und Wirtschaftsbedingungen Vereinigungen zu bilden, ist für jedermann und für alle Berufe.")

    res, e = generate_possible_corrections([doc[17]])

    print(res)

    assert {
               'type': '*',
               'changes': [
                   {'from': 110, 'to': 119, 'type': 'DET', 'replace_with': 'jedermann?jede'}
               ]
           } in res

    assert {
               'type': 'PLURAL_*',
               'changes': [
                   {'from': 110, 'to': 119, 'type': 'DET', 'replace_with': 'alle'}
               ]
           } in res


def test_Kritiker():
    doc = spacify_with_coref(
        "Daß Perot ein Unternehmen erfolgreich leiten kann, davon sind selbst seine Kritiker überzeugt.")

    res, e = generate_possible_corrections([doc[12]])

    print(res)
    print(e)


