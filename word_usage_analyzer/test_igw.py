from word_usage_analyzer.igw import is_gendered_word, gendered_form_to_feminine_form


def test_forms():
    assert is_gendered_word("SchülerIn") == True
    assert is_gendered_word("Schülerin") == False
    assert is_gendered_word("SchülerInnen") == True
    assert is_gendered_word("Schülerinnen") == False
    assert is_gendered_word("Innenausbauexpertin") == False
    assert is_gendered_word("InnenausbauexpertInnen") == True
    assert is_gendered_word("Elektronik-Installateur") == False
    assert is_gendered_word("Elektronik-InstallateurInnen") == True

    assert is_gendered_word("Schüler(innen)") == True
    assert is_gendered_word("Schüler*innen") == True
    assert is_gendered_word("Schüler_innen") == True
    assert is_gendered_word("Schüler:innen") == True


def test_convert():
    assert gendered_form_to_feminine_form("SchülerIn") == "Schülerin"
    assert gendered_form_to_feminine_form("SchülerInnen") == "Schülerinnen"
    assert gendered_form_to_feminine_form("InnenausbauexpertInnen") == "Innenausbauexpertinnen"
    assert gendered_form_to_feminine_form("Elektronik-InstallateurInnen") == "Elektronik-Installateurinnen"

    assert gendered_form_to_feminine_form("Schüler(innen)") == "Schülerinnen"
    assert gendered_form_to_feminine_form("Schüler*innen") == "Schülerinnen"
    assert gendered_form_to_feminine_form("Schüler_innen") == "Schülerinnen"
    assert gendered_form_to_feminine_form("Schüler:innen") == "Schülerinnen"

