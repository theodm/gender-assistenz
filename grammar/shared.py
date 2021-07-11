# https://de.serlo.org/deutsch-als-fremdsprache/31129/unbestimmter-artikel
unbestimmte_artikel = [
    "ein",  # maskulin, nominativ
    "einem",  # maskulin, dativ
    "einen",  # maskulin, akkusativ
    "eines",  # maskulin, genitiv

    "ein",  # neutrum, nominativ
    "einem",  # neutrum, dativ
    "ein",  # neutrum, akkusativ
    "eines",  # neutrum, genitiv

    "eine",  # feminin, nominativ
    "einer",  # feminin, dativ
    "eine",  # feminin, akkusativ
    "einer",  # feminin, genitiv

    "", # plural, nominativ
    "", # plural, dativ
    "", # plural, akkusativ
    "" # plural, genitiv
]

# https://de.serlo.org/deutsch-als-fremdsprache/31114/bestimmter-artikel
bestimmte_artikel = [
    "der",  # maskulin, nominativ
    "dem",  # maskulin, dativ
    "den",  # maskulin, akkusativ
    "des",  # maskulin, genitiv

    "das",  # neutrum, nominativ
    "dem",  # neutrum, dativ
    "das",  # neutrum, akkusativ
    "des",  # neutrum, genitiv

    "die",  # feminin, nominativ
    "der",  # feminin, dativ
    "die",  # feminin, akkusativ
    "der",  # feminin, genitiv

    "die",  # plural, nominativ
    "den",  # plural, dativ
    "die",  # plural, akkusativ
    "der"  # plural, genitiv
]

def for_target(_list, target_case, target_gender, target_number):
    gender_as_index = {
        "Masc": 0,
        "Neut": 1,
        "Fem": 2
    }

    case_as_index = {
        "Nom": 0,
        "Dat": 1,
        "Acc": 2,
        "Gen": 3
    }

    if target_number == "Plur":
        return _list[3 * 4 + case_as_index[target_case]]
    else:
        return _list[gender_as_index[target_gender] * 4 + case_as_index[target_case]]
