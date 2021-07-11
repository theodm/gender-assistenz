

from stanza_test import do_correct

# Tests für Adjektive
def test_adj():
    # Keine Deklination erforderlich, wenn die Adjektive mit einem Verb stehen.
    # Beispiel: Der Schüler ist eifrig.
    #           Die Schülerin ist eifrig.
    #           Die Schüler sind eifrig.
    do_correct("Der Schüler ist eifrig")

def test_adj2():
    # Deklination erforderlich, wenn sie vor einem Substantiv stehen.
    # Beispiel: Der eifrige Schüler geht schlafen.
    #           Die eifrige Schülerin geht schlafen.
    #           Die eifrigen Schüler gehen schlafen.
    do_correct("Der eifrige Schüler geht schlafen.")

def test_adj3():
    # Starke Deklination, wenn dem Adjektiv kein Artikel vorausgeht.
    # Beispiel: Eifriger Schüler geht schlafen.
    #           Eifrige Schülerin geht schlafen.
    #           Eifrige Schüler gehen schlafen.
    do_correct("Eifriger Schüler geht schlafen.")

def test_adj4():
    # Schwache Deklination, wenn dem Adjektiv ein bestimmter Artikel oder ein anderes Artikelwort mit Endung vorausgeht.
    # Beispiel: Der eifrige Schüler geht schlafen.
    #           Die eifrige Schülerin geht schlafen.
    #           Die eifrigen Schüler gehen schlafen.
    do_correct("Der eifrige Schüler geht schlafen.")

def test_adj5():
    # Gemischte Deklination, wenn dem Adjektiv ein unbestimmter Artikel, ein Possesivpronomen oder "kein" vorausgeht.
    # Beispiel: Ein eifriger Schüler geht schlafen.
    #           Eine eifrige Schülerin geht schlafen
    #           Eifrige Schüler gehen schlafen.
    do_correct("Ein eifriger Schüler geht schlafen.")




def test_sehr_einfacher_satz():
    # Singular
    do_correct("Der eifrige Schüler geht ein Eis essen.")

def test_sehr_einfacher_satz2():
    # Singular
    do_correct("Die eifrigeren Schüler gehen ein Eis essen.")


