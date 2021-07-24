from ntbg import needs_to_be_gendered, EIGENNAME_GEFUNDEN, EIGENNAME_KOPULA_SATZ_GEFUNDEN
import spacy

def _spacy(sentence):
    return spacy.load("de_dep_news_trf")(sentence)


def test_eigenname_1():
    result = _spacy("Bundeswirtschaftsminister Werner Müller freut sich über solche Aussichten.")

    ntbg, code, message = needs_to_be_gendered(result[0])

    assert not ntbg
    assert code == EIGENNAME_GEFUNDEN


def test_eigenname_2():
    result = _spacy("Der Bundeswirtschaftsminister freut sich über solche Aussichten.")

    ntbg, code, message = needs_to_be_gendered(result[1])

    assert ntbg

def test_eigenname_3():
    result = _spacy("Seit dem heutigen Mittwochmorgen kursierten an der Frankfurter Börse Gerüchte, denen zufolge Telekom-Chef Ron Sommer zurücktreten wird.")

    ntbg, code, message = needs_to_be_gendered(result[13])

    assert not ntbg
    assert code == EIGENNAME_GEFUNDEN


def test_kopula_regular_1():
    result = _spacy("Klesch ist bereits neuer Betreiber in Hessen.")

    ntbg, code, message = needs_to_be_gendered(result[4])

    assert not ntbg
    assert code == EIGENNAME_KOPULA_SATZ_GEFUNDEN

def test_kopula_not():
    result = _spacy("Klesch isst Betreiber in Hessen.")

    ntbg, code, message = needs_to_be_gendered(result[2])

    assert ntbg

def test_kopula_regular_2():
    result = _spacy("Klesch wird neuer Betreiber in Hessen.")

    ntbg, code, message = needs_to_be_gendered(result[3])

    assert not ntbg
    assert code == EIGENNAME_KOPULA_SATZ_GEFUNDEN

def test_kopula_regular_3():
    result = _spacy("Klesch bleibt neuer Betreiber in Hessen.")

    ntbg, code, message = needs_to_be_gendered(result[3])

    assert not ntbg
    assert code == EIGENNAME_KOPULA_SATZ_GEFUNDEN

def test_kopula_regular_plural():
    # ToDo: Was ist mit gemischten Namen hier?
    result = _spacy("Klesch und Kleber bleiben neue Betreiber in Hessen.")

    ntbg, code, message = needs_to_be_gendered(result[5])

    assert not ntbg
    assert code == EIGENNAME_KOPULA_SATZ_GEFUNDEN

def test_kopula_plural_not():
    result = _spacy("Die Schüler bleiben neue Betreiber in Hessen.")

    ntbg, code, message = needs_to_be_gendered(result[4])

    assert ntbg
