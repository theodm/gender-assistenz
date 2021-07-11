def transform_noun(lex_target_noun, target_case, target_number):
    case_mapping = {
        "Nom": "nominativ_",
        "Gen": "genitiv_",
        "Dat": "dativ_",
        "Acc": "akkusativ_",
    }

    number_mapping = {
        "Sing": "singular",
        "Plur": "plural"
    }

    # Für bestimmte Worte gibt es Plural 1 und Plural 2 Formen
    # statt nur einer Pluralform. Dieser Spezialfall ist zu
    # berücksichtigen.
    if lex_target_noun["nominativ_plural1"] is not None:
        number_mapping["Plur"] = "plural1"

    return lex_target_noun[case_mapping[target_case] + number_mapping[target_number]]
