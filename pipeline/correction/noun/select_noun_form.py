
# Für einen Lexikoneintrag wählt diese Methode in Abhängigkeit
# des übergebenen Kasus und des Numerus die entsprechende Wortform
# aus dem Lexikoneintrag zurück.
#
# Bsp.:
# Für das Nomen Spieler gibt es die folgenden Formen:
#
# 	            Singular 	    Plural
#   Nominativ 	der Spieler 	die Spieler
#   Genitiv 	des Spielers 	der Spieler
#   Dativ 	    dem Spieler 	den Spielern
#   Akkusativ 	den Spieler 	die Spieler
#
# In einigen Fällen gibt es für ein Nomen eine Pluralform 1 und
# eine Pluralform 2. TODO
def select_noun_form(lex_target_noun, target_case, target_number):
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
    # statt nur einer Pluralform. TODO
    if "nominativ_plural1" in lex_target_noun and lex_target_noun["nominativ_plural1"] is not None:
        number_mapping["Plur"] = "plural1"

    return lex_target_noun[case_mapping[target_case] + number_mapping[target_number]]
