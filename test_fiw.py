from _spacy import spacify
from fiw import find_initial_words

def test_nomen():
    doc = spacify("Bundeswirtschaftsminister Werner Müller freut sich über solche Aussichten.")

    result = find_initial_words(doc)

    assert result == [(doc[0], 0)]


def test_nomen():
    doc = spacify("Der Käfig ist leer.")

    result = find_initial_words(doc)

    assert result == [(doc[1], 1)]

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

    assert result == [(doc[0], 0), (doc[2], 2), (doc[8], 8), (doc[11], 11)]

def test_derjenige2():
    doc = spacify("Derjenige, der sich impfen lassen will, sollte einen Krankheitstag wegen Impfnebenwirkungen einplanen.")

    result = find_initial_words(doc)

    assert result == [(doc[0], 0), (doc[2], 2), (doc[10], 10)]


def test_persPron1Person():
    doc = spacify("Verschärft stellen sich die Probleme für Frauen dar, die oft freiwillig in Nachtschicht gehen, \"weil das familiär für mich ideal ist\".")

    result = find_initial_words(doc)

    assert result == []

def test_persPron3():
    doc = spacify("Er sollte sich überlegen ob das sinnvoll ist.")

    result = find_initial_words(doc)

    assert result == [(doc[0], 0)]
