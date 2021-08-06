from pgender._spacy import spacify
from pgender.fiw import find_initial_words

def test_nomen():
    doc = spacify("Bundeswirtschaftsminister Werner Müller freut sich über solche Aussichten.")

    result = find_initial_words(doc)

    assert result == [(doc[0], 0)]
#
# def test_nomen_not_pron():
#     doc = spacify("Bundeswirtschaftsminister Werner Müller, derjenige, der davon profitiert, freut sich über solche Aussichten.")
#
#     result = find_initial_words(doc)
#
#     assert result == [(doc[0], 0)]

def test_nomen_not_genderable():
    doc = spacify("Der Käfig ist leer.")

    result = find_initial_words(doc)

    assert result == []

def test_nomen_with_dash():
    doc = spacify("Die größte Konkurrenz zu den DSL-Anbietern dürfte demnach von den Kabelnetzbetreibern ausgehen , 18 Millionen Breitbandkabelanschlüsse wird es laut Studie geben .")

    result = find_initial_words(doc)

    assert result == [(doc[5], 5)]

def test_compound_noun():
    doc = spacify("Vielsurfer blockieren der Telekom das Telefonnetz.")

    result = find_initial_words(doc)

    assert result == [(doc[0], 0)]

#
# def test_nomen_should_not_mark_pronoun():
#     doc = spacify("Hinter der neuen Firma steht unter anderem Lucent Technologies, einer der größten Anbieter von Equipment für Netzwerke und Telekommunikation .")
#
#     result = find_initial_words(doc)
#
#     assert result == [(doc[13], 13)]

def test_jeder():
    doc = spacify("Jeder sollte sich überlegen, ob sein eigenes Verhalten in Ordnung ist.")

    result = find_initial_words(doc)

    assert result == [(doc[0], 0)]

def test_jeder2():
    doc = spacify("Jeder, der deshalb auf die Straße geht, sollte sich überlegen, ob sein eigenes Verhalten in Ordnung ist.")

    result = find_initial_words(doc)

    assert result == [(doc[0], 0), (doc[2], 2)]

def test_mancher():
    doc = spacify("Mancher sollte sich überlegen, ob sein eigenes Verhalten in Ordnung ist.")

    result = find_initial_words(doc)

    assert result == [(doc[0], 0)]

def test_einer():
    doc = spacify("Einer sollte sich überlegen, ob sein eigenes Verhalten in Ordnung ist.")

    result = find_initial_words(doc)

    assert result == [(doc[0], 0)]

def test_keiner():
    doc = spacify("Keiner sollte sich überlegen, ob sein eigenes Verhalten in Ordnung ist.")

    result = find_initial_words(doc)

    assert result == [(doc[0], 0)]

def test_irgendein():
    doc = spacify("Irgendeiner sollte sich überlegen, ob sein eigenes Verhalten in Ordnung ist.")

    result = find_initial_words(doc)

    assert result == [(doc[0], 0)]


def test_derjenige():
    doc = spacify("Derjenige, der sich impfen lassen will, der sollte einen Krankheitstag wegen Impfnebenwirkungen einplanen.")

    result = find_initial_words(doc)

    assert result == [(doc[0], 0), (doc[2], 2), (doc[8], 8)]

def test_derjenige2():
    doc = spacify("Derjenige, der sich impfen lassen will, sollte einen Krankheitstag wegen Impfnebenwirkungen einplanen.")

    result = find_initial_words(doc)

    assert result == [(doc[0], 0), (doc[2], 2)]
