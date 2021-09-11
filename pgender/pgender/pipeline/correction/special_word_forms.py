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

#
# Personalpronomen in der ersten und zweiten Person sind niemals zu gendern.
# (ich, meiner, mir, mich)
# (du, deiner, dir, dich)
# (wir, unser, uns, uns)
# (ihr, euer, euch, euch)
#

#
# Personalpronomen in der dritten Person
#
personal_pronomen_dritte_person = [
    "er",  # maskulin, nominativ
    "ihm",  # maskulin, dativ
    "ihn",  # maskulin, akkusativ
    "seiner",  # maskulin, genitiv

    "es",  # neutrum, nominativ
    "ihm",  # neutrum, dativ
    "es",  # neutrum, akkusativ
    "seiner",  # neutrum, genitiv

    "sie",  # feminin, nominativ
    "ihr",  # feminin, dativ
    "sie",  # feminin, akkusativ
    "ihrer",  # feminin, genitiv

    "sie",  # plural, nominativ
    "ihnen",  # plural, dativ
    "sie",  # plural, akkusativ
    "ihrer"  # plural, genitiv

]

#
# Das Reflexivpronomen ist niemals zu gendern.
# (mir, mich)
# (dir, dich)
# (sich)
# (uns)
# (euch)
# (sich)
#

#
# Das Reziprokpronomen "einander" ist niemals zu gendern.
#

#
# Das Possesivpronomen als Artikelwort (attributierendes Possesivpronomen).
#
possesiv_pronomen_ich_artikelwort = [
    "mein",  # maskulin, nominativ
    "meinem",  # maskulin, dativ
    "meinen",  # maskulin, akkusativ
    "meines",  # maskulin, genitiv

    "mein",  # neutrum, nominativ
    "meinem",  # neutrum, dativ
    "mein",  # neutrum, akkusativ
    "meines",  # neutrum, genitiv

    "meine",  # feminin, nominativ
    "meiner",  # feminin, dativ
    "meine",  # feminin, akkusativ
    "meiner",  # feminin, genitiv

    "meine",  # plural, nominativ
    "meinen",  # plural, dativ
    "meine",  # plural, akkusativ
    "meiner"  # plural, genitiv
]

possesiv_pronomen_du_artikelwort = [
    "dein",  # maskulin, nominativ
    "deinem",  # maskulin, dativ
    "deinen",  # maskulin, akkusativ
    "deines",  # maskulin, genitiv

    "dein",  # neutrum, nominativ
    "deinem",  # neutrum, dativ
    "dein",  # neutrum, akkusativ
    "deines",  # neutrum, genitiv

    "deine",  # feminin, nominativ
    "deiner",  # feminin, dativ
    "deine",  # feminin, akkusativ
    "deiner",  # feminin, genitiv

    "deine",  # plural, nominativ
    "deinen",  # plural, dativ
    "deine",  # plural, akkusativ
    "deiner"  # plural, genitiv
]

possesiv_pronomen_er_es_artikelwort = [
    "sein",  # maskulin, nominativ
    "seinem",  # maskulin, dativ
    "seinen",  # maskulin, akkusativ
    "seines",  # maskulin, genitiv

    "sein",  # neutrum, nominativ
    "seinem",  # neutrum, dativ
    "sein",  # neutrum, akkusativ
    "seines",  # neutrum, genitiv

    "seine",  # feminin, nominativ
    "seiner",  # feminin, dativ
    "seine",  # feminin, akkusativ
    "seiner",  # feminin, genitiv

    "seine",  # plural, nominativ
    "seinen",  # plural, dativ
    "seine",  # plural, akkusativ
    "seiner"  # plural, genitiv
]

possesiv_pronomen_sie_artikelwort = [
    "ihr",  # maskulin, nominativ
    "ihrem",  # maskulin, dativ
    "ihren",  # maskulin, akkusativ
    "ihres",  # maskulin, genitiv

    "ihr",  # neutrum, nominativ
    "ihrem",  # neutrum, dativ
    "ihr",  # neutrum, akkusativ
    "ihres",  # neutrum, genitiv

    "ihre",  # feminin, nominativ
    "ihrer",  # feminin, dativ
    "ihre",  # feminin, akkusativ
    "ihrer",  # feminin, genitiv

    "ihre",  # plural, nominativ
    "ihren",  # plural, dativ
    "ihre",  # plural, akkusativ
    "ihrer"  # plural, genitiv
]

possesiv_pronomen_wir_artikelwort = [
    "unser",  # maskulin, nominativ
    "unserem",  # maskulin, dativ
    "unseren",  # maskulin, akkusativ
    "unseres",  # maskulin, genitiv

    "unser",  # neutrum, nominativ
    "unserem",  # neutrum, dativ
    "unser",  # neutrum, akkusativ
    "unseres",  # neutrum, genitiv

    "unsere",  # feminin, nominativ
    "unserer",  # feminin, dativ
    "unsere",  # feminin, akkusativ
    "unserer",  # feminin, genitiv

    "unsere",  # plural, nominativ
    "unseren",  # plural, dativ
    "unsere",  # plural, akkusativ
    "unserer"  # plural, genitiv
]

possesiv_pronomen_ihr_artikelwort = [
    "eur",  # maskulin, nominativ
    "eurem",  # maskulin, dativ
    "euren",  # maskulin, akkusativ
    "eures",  # maskulin, genitiv

    "eure",  # neutrum, nominativ
    "eurem",  # neutrum, dativ
    "euer",  # neutrum, akkusativ
    "eures",  # neutrum, genitiv

    "eure",  # feminin, nominativ
    "eurer",  # feminin, dativ
    "eure",  # feminin, akkusativ
    "eurer",  # feminin, genitiv

    "eure",  # plural, nominativ
    "euren",  # plural, dativ
    "eure",  # plural, akkusativ
    "eurer"  # plural, genitiv
]

possesiv_pronomen_sie_plural_artikelwort = [
    "ihr",  # maskulin, nominativ
    "ihrem",  # maskulin, dativ
    "ihren",  # maskulin, akkusativ
    "ihres",  # maskulin, genitiv

    "ihr",  # neutrum, nominativ
    "ihrem",  # neutrum, dativ
    "ihr",  # neutrum, akkusativ
    "ihres",  # neutrum, genitiv

    "ihre",  # feminin, nominativ
    "ihrer",  # feminin, dativ
    "ihre",  # feminin, akkusativ
    "ihrer",  # feminin, genitiv

    "ihre",  # plural, nominativ
    "ihren",  # plural, dativ
    "ihre",  # plural, akkusativ
    "ihrer"  # plural, genitiv
]

#
# Das Possesivpronomen stellvertretend für ein Nomen (substituirendes Possesivpronomen).
#
possesiv_pronomen_ich_attributierend = [
    "meiner",  # maskulin, nominativ
    "meinem",  # maskulin, dativ
    "meinen",  # maskulin, akkusativ
    "meines",  # maskulin, genitiv

    "meines",  # neutrum, nominativ
    "meinem",  # neutrum, dativ
    "meines",  # neutrum, akkusativ
    "meines",  # neutrum, genitiv

    "meine",  # feminin, nominativ
    "meiner",  # feminin, dativ
    "meine",  # feminin, akkusativ
    "meiner",  # feminin, genitiv

    "meine",  # plural, nominativ
    "meinen",  # plural, dativ
    "meine",  # plural, akkusativ
    "meiner"  # plural, genitiv
]

possesiv_pronomen_du_attributierend = [
    "deiner",  # maskulin, nominativ
    "deinem",  # maskulin, dativ
    "deinen",  # maskulin, akkusativ
    "deines",  # maskulin, genitiv

    "deines",  # neutrum, nominativ
    "deinem",  # neutrum, dativ
    "deines",  # neutrum, akkusativ
    "deines",  # neutrum, genitiv

    "deine",  # feminin, nominativ
    "deiner",  # feminin, dativ
    "deine",  # feminin, akkusativ
    "deiner",  # feminin, genitiv

    "deine",  # plural, nominativ
    "deinen",  # plural, dativ
    "deine",  # plural, akkusativ
    "deiner"  # plural, genitiv
]


possesiv_pronomen_er_es_attributierend = [
    "seiner",  # maskulin, nominativ
    "seinem",  # maskulin, dativ
    "seinen",  # maskulin, akkusativ
    "seines",  # maskulin, genitiv

    "seines",  # neutrum, nominativ
    "seinem",  # neutrum, dativ
    "seines",  # neutrum, akkusativ
    "seines",  # neutrum, genitiv

    "seine",  # feminin, nominativ
    "seiner",  # feminin, dativ
    "seine",  # feminin, akkusativ
    "seiner",  # feminin, genitiv

    "seine",  # plural, nominativ
    "seinen",  # plural, dativ
    "seine",  # plural, akkusativ
    "seiner"  # plural, genitiv
]


posssesiv_pronomen_sie_attributierend = [
    "ihrer",  # maskulin, nominativ
    "ihrem",  # maskulin, dativ
    "ihren",  # maskulin, akkusativ
    "ihres",  # maskulin, genitiv

    "ihres",  # neutrum, nominativ
    "ihrem",  # neutrum, dativ
    "ihres",  # neutrum, akkusativ
    "ihres",  # neutrum, genitiv

    "ihre",  # feminin, nominativ
    "ihrer",  # feminin, dativ
    "ihre",  # feminin, akkusativ
    "ihrer",  # feminin, genitiv

    "ihre",  # plural, nominativ
    "ihren",  # plural, dativ
    "ihre",  # plural, akkusativ
    "ihrer"  # plural, genitiv
]


posssesiv_pronomen_wir_attributierend = [
    "unserer",  # maskulin, nominativ
    "unserem",  # maskulin, dativ
    "unseren",  # maskulin, akkusativ
    "unseres",  # maskulin, genitiv

    "unseres",  # neutrum, nominativ
    "unserem",  # neutrum, dativ
    "unseres",  # neutrum, akkusativ
    "unseres",  # neutrum, genitiv

    "unsere",  # feminin, nominativ
    "unserer",  # feminin, dativ
    "unsere",  # feminin, akkusativ
    "unserer",  # feminin, genitiv

    "unsere",  # plural, nominativ
    "unseren",  # plural, dativ
    "unsere",  # plural, akkusativ
    "unserer"  # plural, genitiv
]


posssesiv_pronomen_ihr_attributierend = [
    "eurer",  # maskulin, nominativ
    "eurem",  # maskulin, dativ
    "euren",  # maskulin, akkusativ
    "eures",  # maskulin, genitiv

    "eures",  # neutrum, nominativ
    "eurem",  # neutrum, dativ
    "eures",  # neutrum, akkusativ
    "eures",  # neutrum, genitiv

    "eure",  # feminin, nominativ
    "eurer",  # feminin, dativ
    "eure",  # feminin, akkusativ
    "eurer",  # feminin, genitiv

    "eure",  # plural, nominativ
    "euren",  # plural, dativ
    "eure",  # plural, akkusativ
    "eurer"  # plural, genitiv
]


posssesiv_pronomen_sie_plural_attributierend = [
    "ihrer",  # maskulin, nominativ
    "ihrem",  # maskulin, dativ
    "ihren",  # maskulin, akkusativ
    "ihres",  # maskulin, genitiv

    "ihres",  # neutrum, nominativ
    "ihrem",  # neutrum, dativ
    "ihres",  # neutrum, akkusativ
    "ihres",  # neutrum, genitiv

    "ihre",  # feminin, nominativ
    "ihrer",  # feminin, dativ
    "ihre",  # feminin, akkusativ
    "ihrer",  # feminin, genitiv

    "ihre",  # plural, nominativ
    "ihren",  # plural, dativ
    "ihre",  # plural, akkusativ
    "ihrer"  # plural, genitiv
]

#
# Demonstrativpronomen können sowohl als Artikelwörter als auch als Stellvertreter eines Nomens vorkommen.
#
demonstrativ_pronomen_derdiedas = [
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


demonstrativ_pronomen_solch = [
    "solcher",  # maskulin, nominativ
    "solchem",  # maskulin, dativ
    "solchen",  # maskulin, akkusativ
    "solchen",  # maskulin, genitiv

    "solches",  # neutrum, nominativ
    "solchem",  # neutrum, dativ
    "solches",  # neutrum, akkusativ
    "solchen",  # neutrum, genitiv

    "solche",  # feminin, nominativ
    "solcher",  # feminin, dativ
    "solche",  # feminin, akkusativ
    "solcher",  # feminin, genitiv

    "solche",  # plural, nominativ
    "solchen",  # plural, dativ
    "solche",  # plural, akkusativ
    "solcher"  # plural, genitiv
]

#
# Das Demonstrativpronomen selbst / selber wird nicht dekliniert.
#

#
# Das Demonstrativpronomen derlei / dergleichen wird nicht dekliniert.
#

demonstrativ_pronomen_derselb = [
    "derselbe",  # maskulin, nominativ
    "demselben",  # maskulin, dativ
    "denselben",  # maskulin, akkusativ
    "desselben",  # maskulin, genitiv

    "dasselbe",  # neutrum, nominativ
    "demselben",  # neutrum, dativ
    "dasselbe",  # neutrum, akkusativ
    "desselben",  # neutrum, genitiv

    "dieselbe",  # feminin, nominativ
    "derselben",  # feminin, dativ
    "dieselbe",  # feminin, akkusativ
    "derselben",  # feminin, genitiv

    "dieselben",  # plural, nominativ
    "denselben",  # plural, dativ
    "dieselben",  # plural, akkusativ
    "derselben"  # plural, genitiv
]


demonstrativ_pronomen_derjenige = [
    "derjenige",  # maskulin, nominativ
    "demjenigen",  # maskulin, dativ
    "denjenigen",  # maskulin, akkusativ
    "desjenigen",  # maskulin, genitiv

    "dasjenige",  # neutrum, nominativ
    "demjenigen",  # neutrum, dativ
    "dasjenige",  # neutrum, akkusativ
    "desjenigen",  # neutrum, genitiv

    "diejenige",  # feminin, nominativ
    "derjenigen",  # feminin, dativ
    "diejenige",  # feminin, akkusativ
    "derjenigen",  # feminin, genitiv

    "diejenigen",  # plural, nominativ
    "denjenigen",  # plural, dativ
    "diejenigen",  # plural, akkusativ
    "derjenigen"  # plural, genitiv
]

demonstrativ_pronomen_dies = [
    "dieser",  # maskulin, nominativ
    "diesem",  # maskulin, dativ
    "diesen",  # maskulin, akkusativ
    "dieses",  # maskulin, genitiv

    "dieses",  # neutrum, nominativ
    "diesem",  # neutrum, dativ
    "dieses",  # neutrum, akkusativ
    "dieses",  # neutrum, genitiv

    "diese",  # feminin, nominativ
    "dieser",  # feminin, dativ
    "diese",  # feminin, akkusativ
    "dieser",  # feminin, genitiv

    "diese",  # plural, nominativ
    "diesen",  # plural, dativ
    "diese",  # plural, akkusativ
    "dieser"  # plural, genitiv
]

demonstrativ_pronomen_jen = [
    "jener",  # maskulin, nominativ
    "jenem",  # maskulin, dativ
    "jenen",  # maskulin, akkusativ
    "jenes",  # maskulin, genitiv

    "jenes",  # neutrum, nominativ
    "jenem",  # neutrum, dativ
    "jenes",  # neutrum, akkusativ
    "jenes",  # neutrum, genitiv

    "jene",  # feminin, nominativ
    "jener",  # feminin, dativ
    "jene",  # feminin, akkusativ
    "jener",  # feminin, genitiv

    "jene",  # plural, nominativ
    "jenen",  # plural, dativ
    "jene",  # plural, akkusativ
    "jener"  # plural, genitiv
]

#
# Fragepronomen
#

#
# Das Fragepronomen wer / was muss nicht gegendert werden.
#

frage_pronomen_welche = [
    "welcher",  # maskulin, nominativ
    "welchem",  # maskulin, dativ
    "welchen",  # maskulin, akkusativ
    "welches",  # maskulin, genitiv

    "welches",  # neutrum, nominativ
    "welchem",  # neutrum, dativ
    "welches",  # neutrum, akkusativ
    "welches",  # neutrum, genitiv

    "welche",  # feminin, nominativ
    "welcher",  # feminin, dativ
    "welche",  # feminin, akkusativ
    "welcher",  # feminin, genitiv

    "welche",  # plural, nominativ
    "welchen",  # plural, dativ
    "welche",  # plural, akkusativ
    "welcher"  # plural, genitiv
]

#
# Das Fragepronomen "was für ein" wird von SpacY nicht gefunden, da es aus mehreren Wörtern besteht.
#

#
# Relativpronomen leiten Relativsätze ein.
#
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

#
# Die Relativpronomen wer/was wird nicht gegendert.
#

#
# Indefinitpronomen können sowohl als Artikelwörter als auch als Stellvertreter eines Nomens vorkommen.
#

#
# "Ein" wird nur als substituirendes Pronomen verwendet.
#
indefinit_pronomen_ein = [
    "einer",  # maskulin, nominativ
    "einem",  # maskulin, dativ
    "einen",  # maskulin, akkusativ
    "eines",  # maskulin, genitiv

    "eines",  # neutrum, nominativ
    "einem",  # neutrum, dativ
    "eines",  # neutrum, akkusativ
    "eines",  # neutrum, genitiv

    "eine",  # feminin, nominativ
    "einer",  # feminin, dativ
    "eine",  # feminin, akkusativ
    "einer",  # feminin, genitiv

    "",  # plural, nominativ
    "",  # plural, dativ
    "",  # plural, akkusativ
    ""  # plural, genitiv
]

indefinit_pronomen_kein_artikelwort = [
    "kein",  # maskulin, nominativ
    "keinem",  # maskulin, dativ
    "keinen",  # maskulin, akkusativ
    "keines",  # maskulin, genitiv

    "kein",  # neutrum, nominativ
    "keinem",  # neutrum, dativ
    "kein",  # neutrum, akkusativ
    "keines",  # neutrum, genitiv

    "keine",  # feminin, nominativ
    "keiner",  # feminin, dativ
    "keine",  # feminin, akkusativ
    "keiner",  # feminin, genitiv

    "keine",  # plural, nominativ
    "keinen",  # plural, dativ
    "keine",  # plural, akkusativ
    "keiner"  # plural, genitiv
]

indefinit_pronomen_kein_substituirend = [
    "keiner",  # maskulin, nominativ
    "keinem",  # maskulin, dativ
    "keinen",  # maskulin, akkusativ
    "keines",  # maskulin, genitiv

    "keins",  # neutrum, nominativ
    "keinem",  # neutrum, dativ
    "keins",  # neutrum, akkusativ
    "keines",  # neutrum, genitiv

    "keine",  # feminin, nominativ
    "keiner",  # feminin, dativ
    "keine",  # feminin, akkusativ
    "keiner",  # feminin, genitiv

    "keine",  # plural, nominativ
    "keinen",  # plural, dativ
    "keine",  # plural, akkusativ
    "keiner"  # plural, genitiv
]

indefinit_pronomen_welche = [
    "welcher",  # maskulin, nominativ
    "welchem",  # maskulin, dativ
    "welchen",  # maskulin, akkusativ
    "",  # maskulin, genitiv

    "welches",  # neutrum, nominativ
    "welchem",  # neutrum, dativ
    "welches",  # neutrum, akkusativ
    "",  # neutrum, genitiv

    "welche",  # feminin, nominativ
    "welcher",  # feminin, dativ
    "welche",  # feminin, akkusativ
    "",  # feminin, genitiv

    "welche",  # plural, nominativ
    "welchen",  # plural, dativ
    "welche",  # plural, akkusativ
    ""  # plural, genitiv
]

#
# Indefinitpronomen "man" wird nicht gegendert.
#

#
# Indefinitpronomen "jemand" / "niemand" wird nicht gegendert.
#

#
# Indefinitpronomen "etwas" / "nichts" wird nicht gegendert.
#


indefinit_pronomen_all = [
    "aller",  # maskulin, nominativ
    "allem",  # maskulin, dativ
    "allen",  # maskulin, akkusativ
    "alles",  # maskulin, genitiv

    "alles",  # neutrum, nominativ
    "allem",  # neutrum, dativ
    "alles",  # neutrum, akkusativ
    "alles",  # neutrum, genitiv

    "alle",  # feminin, nominativ
    "aller",  # feminin, dativ
    "allem",  # feminin, akkusativ
    "aller",  # feminin, genitiv

    "alle",  # plural, nominativ
    "allen",  # plural, dativ
    "alle",  # plural, akkusativ
    "aller"  # plural, genitiv
]


indefinit_pronomen_einige = [
    "einiger",  # maskulin, nominativ
    "einigem",  # maskulin, dativ
    "einigen",  # maskulin, akkusativ
    "einigen",  # maskulin, genitiv

    "einiges",  # neutrum, nominativ
    "einigem",  # neutrum, dativ
    "einiges",  # neutrum, akkusativ
    "einigen",  # neutrum, genitiv

    "einige",  # feminin, nominativ
    "einiger",  # feminin, dativ
    "einige",  # feminin, akkusativ
    "einiger",  # feminin, genitiv

    "einige",  # plural, nominativ
    "einigen",  # plural, dativ
    "einige",  # plural, akkusativ
    "einiger"  # plural, genitiv
]


indefinit_pronomen_manch = [
    "mancher",  # maskulin, nominativ
    "manchem",  # maskulin, dativ
    "manchem",  # maskulin, akkusativ
    "manches",  # maskulin, genitiv

    "manches",  # neutrum, nominativ
    "manchem",  # neutrum, dativ
    "manches",  # neutrum, akkusativ
    "manches",  # neutrum, genitiv

    "manche",  # feminin, nominativ
    "mancher",  # feminin, dativ
    "manche",  # feminin, akkusativ
    "mancher",  # feminin, genitiv

    "manche",  # plural, nominativ
    "manchen",  # plural, dativ
    "manche",  # plural, akkusativ
    "mancher"  # plural, genitiv
]

#
# Indefinitpronomen "beide" wird nicht gegendert.
#


indefinit_pronomen_irgendein_artikelwort = [
    "irgendein",  # maskulin, nominativ
    "irgendeinem",  # maskulin, dativ
    "irgendeinen",  # maskulin, akkusativ
    "irgendeines",  # maskulin, genitiv

    "irgendein",  # neutrum, nominativ
    "irgendeinem",  # neutrum, dativ
    "irgendein",  # neutrum, akkusativ
    "irgendeines",  # neutrum, genitiv

    "irgendeine",  # feminin, nominativ
    "irgendeiner",  # feminin, dativ
    "irgendeine",  # feminin, akkusativ
    "irgendeiner",  # feminin, genitiv

    "", # plural, nominativ
    "", # plural, dativ
    "", # plural, akkusativ
    "" # plural, genitiv
]


indefinit_pronomen_irgendein_substituirt = [
    "irgendeiner",  # maskulin, nominativ
    "irgendeinem",  # maskulin, dativ
    "irgendeinen",  # maskulin, akkusativ
    "irgendeines",  # maskulin, genitiv

    "irgendeines",  # neutrum, nominativ
    "irgendeinem",  # neutrum, dativ
    "irgendeines",  # neutrum, akkusativ
    "irgendeines",  # neutrum, genitiv

    "irgendeine",  # feminin, nominativ
    "irgendeiner",  # feminin, dativ
    "irgendeine",  # feminin, akkusativ
    "irgendeiner",  # feminin, genitiv

    "", # plural, nominativ
    "", # plural, dativ
    "", # plural, akkusativ
    "" # plural, genitiv
]


indefinit_pronomen_irgenwelch = [
    "irgendwelcher",  # maskulin, nominativ
    "irgendwelchem",  # maskulin, dativ
    "irgendwelchen",  # maskulin, akkusativ
    "irgendwelches",  # maskulin, genitiv

    "irgendwelches",  # neutrum, nominativ
    "irgendwelchem",  # neutrum, dativ
    "irgendwelches",  # neutrum, akkusativ
    "irgendwelches",  # neutrum, genitiv

    "irgendwelche",  # feminin, nominativ
    "irgendwelcher",  # feminin, dativ
    "irgendwelche",  # feminin, akkusativ
    "irgendwelcher",  # feminin, genitiv

    "irgendwelche",  # plural, nominativ
    "irgendwelchen",  # plural, dativ
    "irgendwelche",  # plural, akkusativ
    "irgendwelcher"  # plural, genitiv
]


indefinit_pronomen_jed = [
    "jeder",  # maskulin, nominativ
    "jedem",  # maskulin, dativ
    "jeden",  # maskulin, akkusativ
    "jedes",  # maskulin, genitiv

    "jedes",  # neutrum, nominativ
    "jedem",  # neutrum, dativ
    "jedes",  # neutrum, akkusativ
    "jedes",  # neutrum, genitiv

    "jede",  # feminin, nominativ
    "jeder",  # feminin, dativ
    "jede",  # feminin, akkusativ
    "jeder",  # feminin, genitiv

    "",  # plural, nominativ
    "",  # plural, dativ
    "",  # plural, akkusativ
    ""  # plural, genitiv
]

#
# Das Infinitpronomen jedermann wird nicht gegendert.
#


#
# Deklinationen der Adjektive
#
starke_deklination = [
    "er",  # maskulin, nominativ
    "em",  # maskulin, dativ
    "en",  # maskulin, akkusativ
    "en",  # maskulin, genitiv

    "es",  # neutrum, nominativ
    "em",  # neutrum, dativ
    "es",  # neutrum, akkusativ
    "en",  # neutrum, genitiv

    "e",  # feminin, nominativ
    "er",  # feminin, dativ
    "e",  # feminin, akkusativ
    "er",  # feminin, genitiv

    "e",  # plural, nominativ
    "en",  # plural, dativ
    "e",  # plural, akkusativ
    "er"  # plural, genitiv
]

gemischte_deklination = [
    "er",  # maskulin, nominativ
    "en",  # maskulin, dativ
    "en",  # maskulin, akkusativ
    "en",  # maskulin, genitiv

    "es",  # neutrum, nominativ
    "en",  # neutrum, dativ
    "es",  # neutrum, akkusativ
    "en",  # neutrum, genitiv

    "e",  # feminin, nominativ
    "en",  # feminin, dativ
    "e",  # feminin, akkusativ
    "en",  # feminin, genitiv

    "en",  # plural, nominativ
    "en",  # plural, dativ
    "en",  # plural, akkusativ
    "er"  # plural, genitiv
]

schwache_deklination = [
    "e",  # maskulin, nominativ
    "en",  # maskulin, dativ
    "en",  # maskulin, akkusativ
    "en",  # maskulin, genitiv

    "e",  # neutrum, nominativ
    "en",  # neutrum, dativ
    "e",  # neutrum, akkusativ
    "en",  # neutrum, genitiv

    "e",  # feminin, nominativ
    "en",  # feminin, dativ
    "e",  # feminin, akkusativ
    "en",  # feminin, genitiv

    "en",  # plural, nominativ
    "en",  # plural, dativ
    "en",  # plural, akkusativ
    "er"  # plural, genitiv
]

def special_word_form(_list, target_case, target_gender, target_number):
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
