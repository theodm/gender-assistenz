from pgender._spacy import spacify
from pgender.pipeline.correction.adj.change_adj_form import get_declination, change_adj_form


def test_get_declination_Kein_Singular():
    # Fall 1 (positiv):

    doc = spacify("Kein fleißiger Schüler sollte das tun.")

    assert get_declination(doc[1]) == "gemischt"

def test_get_declination_Kein_Plural():
    # Fall 6 (positiv)
    # Fall 1 (negativ: Abgrenzungsfall):

    doc = spacify("Keine fleißigen Schüler sollte das tun.")

    assert get_declination(doc[1]) == "schwach"

def test_get_declination_Unbestimmter_Artikel():
    # Fall 2 (positiv):

    doc = spacify("Ein fleißiger Schüler sollte das tun.")

    assert get_declination(doc[1]) == "gemischt"

def test_get_declination_Unbestimmter_Artikel_target_plural():
    # Fall 2 (negativ: Ziel-Numerus ist unterschiedlich):

    doc = spacify("Ein fleißiger Schüler sollte das tun.")

    assert get_declination(doc[1], True) == "stark"

def test_get_declination_possesiv_pronomen():
    # Fall 3 (positiv)

    doc = spacify("Unser fleißiger Schüler sollte das tun.")

    assert get_declination(doc[1]) == "gemischt"

def test_get_declination_irgendein():
    # Fall 4 (positiv)

    doc = spacify("Irgendein fleißiger Schüler sollte das tun.")

    assert get_declination(doc[1]) == "gemischt"

def test_get_declination_bestimmter_artikel():
    # Fall 5 (positiv)

    doc = spacify("Der fleißige Schüler sollte das tun.")

    assert get_declination(doc[1]) == "schwach"


def test_get_declination_derselb():
    # Fall 7 (positiv)

    doc = spacify("Derselbe fleißige Schüler sollte das tun.")

    assert get_declination(doc[1]) == "schwach"


def test_get_declination_alle():
    # Fall 8 (positiv)

    doc = spacify("Alle fleißigen Schüler sollten das tun.")

    assert get_declination(doc[1]) == "schwach"

def test_change_adj():
    doc = spacify("Es würden aber auch Gespräche mit jedem anderen Anbieter geführt, der meine, ein entsprechendes Angebot machen zu können.")

    assert change_adj_form(doc[7], "Fem", "Plur") == "anderen"
