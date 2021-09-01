import json

import dataset
import os
from sqlalchemy import or_

def find_verb_by_title(title):
    db = dataset.connect('sqlite:///' + os.path.dirname(os.path.realpath(__file__)) + '/words.db')

    words_table = db['verbs']

    result = words_table.find_one(title=title)

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


