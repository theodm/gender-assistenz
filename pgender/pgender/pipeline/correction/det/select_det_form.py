from pgender.pipeline.correction.special_word_forms import unbestimmte_artikel, bestimmte_artikel, special_word_form


def select_det_form(det, target_case, target_gender, target_number):
    lower_det = det.text.lower()

    unbestimmter_det = lower_det in unbestimmte_artikel
    bestimmter_det = lower_det in bestimmte_artikel

    assert unbestimmter_det | bestimmter_det

    if unbestimmter_det:
        return special_word_form(unbestimmte_artikel, target_case, target_gender, target_number)
    else:
        return special_word_form(bestimmte_artikel, target_case, target_gender, target_number)