from pipeline.correction.special_word_forms import possesiv_pronomen_er_es_artikelwort, \
    possesiv_pronomen_sie_artikelwort, possesiv_pronomen_sie_plural_artikelwort, special_word_form


def select_pposs_form(pron, target_gender, target_number):
    lower_pron = pron.text.lower()

    convert_map = {
        "Masc_Sing": possesiv_pronomen_er_es_artikelwort,
        "Fem_Sing": possesiv_pronomen_sie_artikelwort,
        "Masc_Plur": possesiv_pronomen_sie_plural_artikelwort,
        "Fem_Plur": possesiv_pronomen_sie_plural_artikelwort
    }

    pronomen_list = convert_map[target_gender + "_" + target_number]

    # Hier wird das ganze Wort ausgetauscht, ansonsten muss die
    # Wortform gleichbleiben, da sich die Morphologie auf ein anderes Wort
    # bezieht.
    #
    # Bsp.: Der Schüler geht seine Tante besuchen.
    #
    # Die Morphologie bezieht sich auf Tante nicht auf Schüler, vom Schüler hängt stattdessen
    # ab, ob seine oder "ihre" verwendet wird.
    #
    target_case = pron.morph.get("Case")[0]
    _target_gender = pron.morph.get("Gender")[0]
    _target_number = pron.morph.get("Number")[0]

    return special_word_form(pronomen_list, target_case, _target_gender, _target_number)

