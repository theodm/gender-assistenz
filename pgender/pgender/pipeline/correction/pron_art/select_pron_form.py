from pgender.pipeline.correction.special_word_forms import relativ_pronomen_derdiedas, relativ_pronomen_welche, \
    special_word_form, indefinit_pronomen_kein, demonstrativ_pronomen_dies, demonstrativ_pronomen_jen, \
    indefinit_pronomen_jed, possesiv_pronomen_sein_substituirend


def select_pron_form(pron, target_gender, target_number):
    lower_pron = pron.text.lower()

    derdiedas_det = lower_pron in relativ_pronomen_derdiedas
    kein_det = lower_pron in indefinit_pronomen_kein
    dies_det = lower_pron in demonstrativ_pronomen_dies
    jen_det = lower_pron in demonstrativ_pronomen_jen
    welche_det = lower_pron in relativ_pronomen_welche
    jed_det = lower_pron in indefinit_pronomen_jed
    sein_det = lower_pron in possesiv_pronomen_sein_substituirend

    # Kasus soll gleich bleiben
    target_case = pron.morph.get("Case")[0]

    assert derdiedas_det | welche_det | kein_det | dies_det | jen_det | jed_det | sein_det

    if derdiedas_det:
        return special_word_form(relativ_pronomen_derdiedas, target_case, target_gender, target_number)
    elif kein_det:
        return special_word_form(indefinit_pronomen_kein, target_case, target_gender, target_number)
    elif dies_det:
        return special_word_form(demonstrativ_pronomen_dies, target_case, target_gender, target_number)
    elif jen_det:
        return special_word_form(demonstrativ_pronomen_jen, target_case, target_gender, target_number)
    elif jed_det:
        return special_word_form(indefinit_pronomen_jed, target_case, target_gender, target_number)
    elif sein_det:
        return special_word_form(possesiv_pronomen_sein_substituirend, target_case, target_gender, target_number)
    else:
        return special_word_form(relativ_pronomen_welche, target_case, target_gender, target_number)