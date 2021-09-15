import json

from pgender.db_extender import find_in_db_and_convert


def test_einfaches_wort():
    result = find_in_db_and_convert("Schriftsteller")

    assert result["title"] == "Schriftsteller"
    assert result["genus"] == "m"

    assert result["nominativ_singular"] == "Schriftsteller"
    assert result["nominativ_plural"] == "Schriftsteller"
    assert result["genitiv_singular"] == "Schriftstellers"
    assert result["genitiv_plural"] == "Schriftsteller"
    assert result["dativ_singular"] == "Schriftsteller"
    assert result["dativ_plural"] == "Schriftstellern"
    assert result["akkusativ_singular"] == "Schriftsteller"
    assert result["akkusativ_plural"] == "Schriftsteller"
    assert result["weibliche_formen"] == ['Schriftstellerin']

def test_andere_form():
    result = find_in_db_and_convert("Schriftstellern")

    assert result["title"] == "Schriftsteller"
    assert result["genus"] == "m"

    assert result["nominativ_singular"] == "Schriftsteller"
    assert result["nominativ_plural"] == "Schriftsteller"
    assert result["genitiv_singular"] == "Schriftstellers"
    assert result["genitiv_plural"] == "Schriftsteller"
    assert result["dativ_singular"] == "Schriftsteller"
    assert result["dativ_plural"] == "Schriftstellern"
    assert result["akkusativ_singular"] == "Schriftsteller"
    assert result["akkusativ_plural"] == "Schriftsteller"
    assert result["weibliche_formen"] == ['Schriftstellerin']

def test_unbekanntes_zusammengesetztes_wort():
    result = find_in_db_and_convert("Vielsurfer")

    assert result["title"] == "Vielsurfer"
    assert result["genus"] == "m"

    assert result["nominativ_singular"] == "Vielsurfer"
    assert result["nominativ_plural"] == "Vielsurfer"
    assert result["genitiv_singular"] == "Vielsurfers"
    assert result["genitiv_plural"] == "Vielsurfer"
    assert result["dativ_singular"] == "Vielsurfer"
    assert result["dativ_plural"] == "Vielsurfern"
    assert result["akkusativ_singular"] == "Vielsurfer"
    assert result["akkusativ_plural"] == "Vielsurfer"
    assert result["weibliche_formen"] == ['Vielsurferin']

def test_feminines_unbekanntes_zusammengesetztes_wort():
    result = find_in_db_and_convert("Vielsurferin")

    assert result["title"] == "Vielsurferin"
    assert result["genus"] == "f"

    assert result["nominativ_singular"] == "Vielsurferin"
    assert result["nominativ_plural"] == "Vielsurferinnen"
    assert result["genitiv_singular"] == "Vielsurferin"
    assert result["genitiv_plural"] == "Vielsurferinnen"
    assert result["dativ_singular"] == "Vielsurferin"
    assert result["dativ_plural"] == "Vielsurferinnen"
    assert result["akkusativ_singular"] == "Vielsurferin"
    assert result["akkusativ_plural"] == "Vielsurferinnen"
    assert result["maennliche_formen"] == ['Vielsurfer']
