

# https://www.deutschplus.net/pages/Relativpronomen_der_die_das
from grammar import shared

relativ_pronomen_derdiedas = [
    "der",  # maskulin, nominativ
    "dem",  # maskulin, dativ
    "den",  # maskulin, akkusativ
    "dessen",  # maskulin, genitiv

    "das",  # neutrum, nominativ
    "dem",  # neutrum, dativ
    "das",  # neutrum, akkusativ
    "dessen",  # neutrum, genitiv

    "die",  # feminin, nominativ
    "der",  # feminin, dativ
    "die",  # feminin, akkusativ
    "deren",  # feminin, genitiv

    "die",  # plural, nominativ
    "denen",  # plural, dativ
    "die",  # plural, akkusativ
    "deren"  # plural, genitiv
]

relativ_pronomen_welche = [
    "welcher",  # maskulin, nominativ
    "welchem",  # maskulin, dativ
    "welchen",  # maskulin, akkusativ
    "-",  # maskulin, genitiv

    "welches",  # neutrum, nominativ
    "welchem",  # neutrum, dativ
    "welches",  # neutrum, akkusativ
    "-",  # neutrum, genitiv

    "welche",  # feminin, nominativ
    "welcher",  # feminin, dativ
    "welches",  # feminin, akkusativ
    "-",  # feminin, genitiv

    "welche",  # plural, nominativ
    "welchen",  # plural, dativ
    "welche",  # plural, akkusativ
    "-"  # plural, genitiv
]


def transform_determiner(det, target_case, target_gender, target_number):
    if det.word.xpos == "ART":
        return modify_art(det, target_case, target_gender, target_number)
    elif det.word.xpos in ["PRELAT", "PRELS"]:
        return modify_prelat(det, target_case, target_gender, target_number)
    else:
        assert det.word.xpos in ["ART", "PRELAT", "PRELS"]

    return


def modify_prelat(det, target_case, target_gender, target_number):
    assert det.word.xpos == "PRELAT" or det.word.xpos == "PRELS"

    lower_det = det.word.text.lower()

    derdiedas_det = lower_det in relativ_pronomen_derdiedas
    welche_det = lower_det in relativ_pronomen_welche

    # Kasus soll gleich bleiben
    target_case = det.Case

    assert derdiedas_det | welche_det

    if derdiedas_det:
        return shared.for_target(relativ_pronomen_derdiedas, target_case, target_gender, target_number)
    else:
        return shared.for_target(relativ_pronomen_welche, target_case, target_gender, target_number)


def modify_art(det, target_case, target_gender, target_number):
    assert det.word.xpos == "ART"

    lower_det = det.word.text.lower()

    unbestimmter_det = lower_det in shared.unbestimmte_artikel
    bestimmter_det = lower_det in shared.bestimmte_artikel

    assert unbestimmter_det | bestimmter_det

    if unbestimmter_det:
        return shared.for_target(shared.unbestimmte_artikel, target_case, target_gender, target_number)
    else:
        return shared.for_target(shared.bestimmte_artikel, target_case, target_gender, target_number)
