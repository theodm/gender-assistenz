import json

import dataset
import os
from sqlalchemy import or_

def find_verb_by_title(word):
    db = dataset.connect('sqlite:///' + os.path.dirname(os.path.realpath(__file__)) + '/words.db')

    verbs_table = db['verbs']

    praes_akt_ind_1_sing = verbs_table.table.columns.praes_akt_ind_1_sing
    praes_akt_ind_2_sing = verbs_table.table.columns.praes_akt_ind_2_sing
    praes_akt_ind_3_sing = verbs_table.table.columns.praes_akt_ind_3_sing
    praes_akt_ind_1_plur = verbs_table.table.columns.praes_akt_ind_1_plur
    praes_akt_ind_2_plur = verbs_table.table.columns.praes_akt_ind_2_plur
    praes_akt_ind_3_plur = verbs_table.table.columns.praes_akt_ind_3_plur
    praes_akt_konj1_1_sing = verbs_table.table.columns.praes_akt_konj1_1_sing
    praes_akt_konj1_2_sing = verbs_table.table.columns.praes_akt_konj1_2_sing
    praes_akt_konj1_3_sing = verbs_table.table.columns.praes_akt_konj1_3_sing
    praes_akt_konj1_1_plur = verbs_table.table.columns.praes_akt_konj1_1_plur
    praes_akt_konj1_2_plur = verbs_table.table.columns.praes_akt_konj1_2_plur
    praes_akt_konj1_3_plur = verbs_table.table.columns.praes_akt_konj1_3_plur
    praet_akt_ind_1_sing = verbs_table.table.columns.praet_akt_ind_1_sing
    praet_akt_ind_2_sing = verbs_table.table.columns.praet_akt_ind_2_sing
    praet_akt_ind_3_sing = verbs_table.table.columns.praet_akt_ind_3_sing
    praet_akt_ind_1_plur = verbs_table.table.columns.praet_akt_ind_1_plur
    praet_akt_ind_2_plur = verbs_table.table.columns.praet_akt_ind_2_plur
    praet_akt_ind_3_plur = verbs_table.table.columns.praet_akt_ind_3_plur
    praet_akt_konj1_1_sing = verbs_table.table.columns.praet_akt_konj1_1_sing
    praet_akt_konj1_2_sing = verbs_table.table.columns.praet_akt_konj1_2_sing
    praet_akt_konj1_3_sing = verbs_table.table.columns.praet_akt_konj1_3_sing
    praet_akt_konj1_1_plur = verbs_table.table.columns.praet_akt_konj1_1_plur
    praet_akt_konj1_2_plur = verbs_table.table.columns.praet_akt_konj1_2_plur
    praet_akt_konj1_3_plur = verbs_table.table.columns.praet_akt_konj1_3_plur
    praet_akt_konj2_1_sing = verbs_table.table.columns.praet_akt_konj2_1_sing
    praet_akt_konj2_2_sing = verbs_table.table.columns.praet_akt_konj2_2_sing
    praet_akt_konj2_3_sing = verbs_table.table.columns.praet_akt_konj2_3_sing
    praet_akt_konj2_1_plur = verbs_table.table.columns.praet_akt_konj2_1_plur
    praet_akt_konj2_2_plur = verbs_table.table.columns.praet_akt_konj2_2_plur
    praet_akt_konj2_3_plur = verbs_table.table.columns.praet_akt_konj2_3_plur

    clause = or_(
        praes_akt_ind_1_sing == word,
        praes_akt_ind_2_sing == word,
        praes_akt_ind_3_sing == word,
        praes_akt_ind_1_plur == word,
        praes_akt_ind_2_plur == word,
        praes_akt_ind_3_plur == word,
        praes_akt_konj1_1_sing == word,
        praes_akt_konj1_2_sing == word,
        praes_akt_konj1_3_sing == word,
        praes_akt_konj1_1_plur == word,
        praes_akt_konj1_2_plur == word,
        praes_akt_konj1_3_plur == word,
        praet_akt_ind_1_sing == word,
        praet_akt_ind_2_sing == word,
        praet_akt_ind_3_sing == word,
        praet_akt_ind_1_plur == word,
        praet_akt_ind_2_plur == word,
        praet_akt_ind_3_plur == word,
        praet_akt_konj1_1_sing == word,
        praet_akt_konj1_2_sing == word,
        praet_akt_konj1_3_sing == word,
        praet_akt_konj1_1_plur == word,
        praet_akt_konj1_2_plur == word,
        praet_akt_konj1_3_plur == word,
        praet_akt_konj2_1_sing == word,
        praet_akt_konj2_2_sing == word,
        praet_akt_konj2_3_sing == word,
        praet_akt_konj2_1_plur == word,
        praet_akt_konj2_2_plur == word,
        praet_akt_konj2_3_plur == word,
    )

    result = verbs_table.find_one(clause)

    db.close()

    return result

def find_verb_by_any_form(title):
    db = dataset.connect('sqlite:///' + os.path.dirname(os.path.realpath(__file__)) + '/words.db')

    verbs_table = db['verbs']

    result = verbs_table.find_one(title=title)

    db.close()

    return result


def find_by_title(title):
    db = dataset.connect('sqlite:///' + os.path.dirname(os.path.realpath(__file__)) + '/words.db')

    words_table = db['words']

    result = words_table.find_one(title=title)

    if result:
        result["maennliche_formen"] = json.loads(result["maennliche_formen"]) if result["maennliche_formen"] else []
        result["weibliche_formen"] = json.loads(result["weibliche_formen"]) if result["weibliche_formen"] else []

    db.close()

    return result

def find_by_any_form(word):
    db = dataset.connect('sqlite:///' + os.path.dirname(os.path.realpath(__file__)) + '/words.db')

    words_table = db['words']

    nominativ_singular = words_table.table.columns.nominativ_singular
    genitiv_singular = words_table.table.columns.genitiv_singular
    dativ_singular = words_table.table.columns.dativ_singular
    akkusativ_singular = words_table.table.columns.akkusativ_singular

    nominativ_plural = words_table.table.columns.nominativ_plural
    genitiv_plural = words_table.table.columns.genitiv_plural
    dativ_plural = words_table.table.columns.dativ_plural
    akkusativ_plural = words_table.table.columns.akkusativ_plural

    clause = or_(
        nominativ_singular == word,
        genitiv_singular == word,
        dativ_singular == word,
        akkusativ_singular == word,
        nominativ_plural == word,
        genitiv_plural == word,
        dativ_plural == word,
        akkusativ_plural == word
    )

    result = words_table.find_one(clause)

    if result:
        result["maennliche_formen"] = json.loads(result["maennliche_formen"]) if result["maennliche_formen"] else []
        result["weibliche_formen"] = json.loads(result["weibliche_formen"]) if result["weibliche_formen"] else []

    return result


