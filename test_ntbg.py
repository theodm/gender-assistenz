from _spacy import spacify_with_coref
from ntbg import needs_to_be_gendered, RELATIVE_CLAUSE, APPOSITION, KOPULA_SENTENCE, GENITIVE_ATTRIBUTE, \
    EIGENNAME_GEFUNDEN, NOUN_KERNEL_NAME_FOUND, COREF_CHAIN, NO_FEMININE_FORM, BOTH_FORMS, \
    _is_feminine_noun_form_of_extended, _is_feminine_pron_form
import spacy


def _spacy(sentence):
    return spacify_with_coref(sentence)


def test_eigenname_1():
    result = _spacy("Bundeswirtschaftsminister Werner Müller freut sich über solche Aussichten.")

    ntbg, code = needs_to_be_gendered(result, result[0])

    print(code)

    assert not ntbg
    assert code[0][0] == NOUN_KERNEL_NAME_FOUND


def test_eigenname_2():
    result = _spacy("Der Bundeswirtschaftsminister freut sich über solche Aussichten.")

    ntbg, code = needs_to_be_gendered(result, result[1])

    assert ntbg


def test_eigenname_3():
    result = _spacy(
        "Seit dem heutigen Mittwochmorgen kursierten an der Frankfurter Börse Gerüchte, denen zufolge Telekom-Chef Ron Sommer zurücktreten wird.")

    ntbg, code = needs_to_be_gendered(result, result[13])

    print(code)

    assert not ntbg
    assert code[0][0] == NOUN_KERNEL_NAME_FOUND


def test_nomen_not_genderable():
    result = _spacy("Der Käfig ist leer.")

    ntbg, code = needs_to_be_gendered(result, result[1])

    print(code)

    assert not ntbg
    assert code[0][0] == NO_FEMININE_FORM


def test_nomen_with_dash():
    result = _spacy(
        "Die größte Konkurrenz zu den DSL-Anbietern dürfte demnach von den Kabelnetzbetreibern ausgehen , 18 Millionen Breitbandkabelanschlüsse wird es laut Studie geben .")

    ntbg, code = needs_to_be_gendered(result, result[5])

    print(code)

    assert ntbg


def test_compound_noun():
    result = _spacy("Vielsurfer blockieren der Telekom das Telefonnetz.")

    ntbg, code = needs_to_be_gendered(result, result[0])

    print(code)

    assert ntbg


def test_kopula_regular_1():
    result = _spacy("Klesch ist bereits neuer Betreiber in Hessen.")

    ntbg, code = needs_to_be_gendered(result, result[4])

    print(code)

    assert not ntbg
    assert code[0][0] == KOPULA_SENTENCE


def test_kopula_not():
    result = _spacy("Klesch isst Betreiber in Hessen.")

    ntbg, code = needs_to_be_gendered(result, result[2])

    assert ntbg


def test_kopula_regular_2():
    result = _spacy("Klesch wird neuer Betreiber in Hessen.")

    ntbg, code = needs_to_be_gendered(result, result[3])

    print(code)

    assert not ntbg
    assert code[0][0] == KOPULA_SENTENCE


def test_kopula_regular_3():
    result = _spacy("Klesch bleibt neuer Betreiber in Hessen.")

    ntbg, code = needs_to_be_gendered(result, result[3])

    print(code)

    assert not ntbg
    assert code[0][0] == KOPULA_SENTENCE


def test_kopula_regular_plural():
    # ToDo: Was ist mit gemischten Namen hier?
    result = _spacy("Klesch und Kleber bleiben neue Betreiber in Hessen.")

    ntbg, code = needs_to_be_gendered(result, result[5])

    print(code)

    assert not ntbg
    assert code[0][0] == KOPULA_SENTENCE


def test_kopula_plural_not():
    result = _spacy("Die Schüler bleiben neue Betreiber in Hessen.")

    ntbg, code = needs_to_be_gendered(result, result[4], [result[4], result[1]])

    assert ntbg


def test_app_pron():
    result = _spacy(
        "Hinter der neuen Firma steht unter anderem Lucent Technologies , einer der größten Anbieter von Equipment für Netzwerke und Telekommunikation .")

    ntbg, code = needs_to_be_gendered(result, result[10])

    print(code)

    assert not ntbg
    assert code[0][0] == APPOSITION


def test_app_pron_rec():
    result = _spacy(
        "Hinter der neuen Firma steht unter anderem die Firma Lucent Technologies , einer der größten Anbieter von Equipment für Netzwerke und Telekommunikation .")

    ntbg, code = needs_to_be_gendered(result, result[12])

    print(code)

    assert not ntbg
    assert code[0][0] == APPOSITION


def test_gen_attribute_rec():
    result = _spacy(
        "Hinter der neuen Firma steht unter anderem Lucent Technologies , einer der größten Anbieter von Equipment für Netzwerke und Telekommunikation .")

    ntbg, code = needs_to_be_gendered(result, result[13])

    print(code)

    assert not ntbg
    assert code[0][0] == GENITIVE_ATTRIBUTE
    assert code[1][0] == APPOSITION


def test_gen_attribute_pos():
    result = _spacy(
        "Das am heutigen Donnerstag von der Telekom vorgelegte Angebot zur Großhandelsflatrate stößt beim Verband der Anbieter von Telekommunikations- und Mehrwertdiensten ( VATM ) auf Kritik .")

    ntbg, code = needs_to_be_gendered(result, result[15], [result[15]])

    print(code)

    assert ntbg


def test_gen_attribute_pos2():
    result = _spacy(
        "Die Mitnahme der Handy-Nummer bei einem Wechsel des Mobilfunkanbieters wird nun erst ab dem November nächsten Jahres möglich sein .")

    ntbg, code = needs_to_be_gendered(result, result[8], [result[8]])

    print(code)

    assert ntbg


#
# def test_TODOOD():
#     result = _spacy("""Das zwischen den beiden Unternehmen vereinbarte Entgelt soll " deutlich " unter dem derzeitigen regulierten Preis liegen , den Telekommunikationsunternehmen für die gleiche Leistung an die Deutsche Telekom zahlen müssen .""")
#
#     ntbg, code = needs_to_be_gendered(result, result[18], [result[18]])
#
#     print(code)
#
#     assert not ntbg

# In dem zweiten Vergütungsbericht der Bundesregierung an den Bundestag , der vom Kabinett verabschiedet wurde , wird gefordert , dass digitale Speichermedien zukünftig der Vergütungspflicht unterliegen sollen . <-- Cooles Beispiel
def test_relative_clause_subject():
    result = _spacy(
        "Der Duden für Szenesprachen , der bereits seit dem Frühjahr im Handel ist , wird nun online fortgeschrieben .")

    ntbg, code = needs_to_be_gendered(result, result[5], [])

    print(code)

    assert not ntbg
    assert code[0][0] == RELATIVE_CLAUSE


def test_coref_single_sentence():
    result = _spacy(
        "Während der Test ursprünglich am 31.12.2000 abgeschlossen sein sollte , geht er nun bis Ende April des nächsten Jahres weiter . ")

    print(result[11])
    ntbg, code = needs_to_be_gendered(result, result[11])

    print(code)

    assert not ntbg
    assert code[0][0] == COREF_CHAIN


def test_coref_multiple_sentence():
    result = _spacy(
        "Von Angela Merkel sind kaum Nassbilder bekannt; wo Merkel ist, ist notfalls auch immer ein Regenschirm. Sie würde sich auch nicht öffentlich in Situationen bringen, in denen man US-Präsidenten oder britische Premierminister immer wieder sieht: Sie kämpfen mit ihrem Schirm, weil der durch den Wind umgestülpt wird. ")

    print(result[19])
    ntbg, code = needs_to_be_gendered(result, result[19])

    print(code)

    assert not ntbg
    assert code[0][0] == COREF_CHAIN


def test_both_forms_1():
    result = _spacy("Wissenschaftler und Wissenschaftlerinnen gehen ein Eis essen.")

    ntbg, code = needs_to_be_gendered(result, result[0])

    print(code)

    assert not ntbg
    assert code[0][0] == BOTH_FORMS


def test_both_forms_2():
    result = _spacy("Telekom-Kunden und Telekom-Kundinnen gehen ein Eis essen.")

    ntbg, code = needs_to_be_gendered(result, result[0])

    print(code)

    assert not ntbg
    assert code[0][0] == BOTH_FORMS


def test_both_forms_3():
    result = _spacy("Telekom-Kunden und Kundinnen gehen ein Eis essen.")

    ntbg, code = needs_to_be_gendered(result, result[0])

    print(code)

    assert not ntbg
    assert code[0][0] == BOTH_FORMS


def test_both_forms_4():
    result = _spacy("Wissenschaftlerinnen und Wissenschaftler gehen ein Eis essen.")

    ntbg, code = needs_to_be_gendered(result, result[2])

    print(code)

    assert not ntbg
    assert code[0][0] == BOTH_FORMS


def test_both_forms_5():
    result = _spacy("Wissenschaftlerinnen, Vertreter, Vertreterinnen und Wissenschaftler gehen ein Eis essen.")

    ntbg, code = needs_to_be_gendered(result, result[6])

    print(code)

    assert not ntbg
    assert code[0][0] == BOTH_FORMS


def test_both_forms_6():
    result = _spacy("Telekom-Kunden, Wissenschaftler, Wissenschaftlerinnen, und Telekom-Kundinnen gehen ein Eis essen.")

    ntbg, code = needs_to_be_gendered(result, result[0])

    print(code)

    assert not ntbg
    assert code[0][0] == BOTH_FORMS


def test_temp():
    result = _spacy("Markus, der neue Betreiber, ging pleite.")

    ntbg, code = needs_to_be_gendered(result, result[4])

    print(code)

    assert not ntbg


def test_both_forms_7():
    result = _spacy(
        "Unter den Spitzenkandidatinnen und -Kandidaten zur Bundestagswahl wird Annalena Baerbock mit Abstand am häufigsten Opfer von Desinformationskampagnen und Fake News.")

    ntbg, code = needs_to_be_gendered(result, result[4])

    print(code)

    assert not ntbg
    assert code[0][0] == BOTH_FORMS


def test_both_forms_pron_1():
    result = _spacy("Er und sie stehen vor seinem Haus")

    ntbg, code = needs_to_be_gendered(result, result[0])

    print(code)

    assert not ntbg
    assert code[0][0] == BOTH_FORMS

def test_both_forms_pron_2():
    result = _spacy("Sie und er stehen vor seinem Haus")

    ntbg, code = needs_to_be_gendered(result, result[2])

    print(code)

    assert not ntbg
    assert code[0][0] == BOTH_FORMS

def test_both_forms_pron_3():
    result = _spacy("Eine oder einer stehen vor deinem Haus.")

    ntbg, code = needs_to_be_gendered(result, result[2])

    print(code)

    assert not ntbg
    assert code[0][0] == BOTH_FORMS
#
# def test_subset_of_noun():
#     result = _spacy("Fortschritt wird erreicht, wenn jeder volljährige Bürger, der eine Meinung hat, wählen geht.")
#
#     ntbg, code = needs_to_be_gendered(result, result[9])
#
#     print(code)
#
#     assert not ntbg
#     assert code[0][0] == BOTH_FORMS



def test__is_feminine_noun_form_of_extended():
    assert _is_feminine_noun_form_of_extended("Wissenschaftlerin", "Wissenschaftler")

def test__is_feminine_noun_form_of_extended_2():
    assert _is_feminine_noun_form_of_extended("Raketenwissenschaftlerin", "Wissenschaftler")

def test__is_feminine_noun_form_of_extended_3():
    assert _is_feminine_noun_form_of_extended("Raketenwissenschaftlerin", "-Wissenschaftler")


