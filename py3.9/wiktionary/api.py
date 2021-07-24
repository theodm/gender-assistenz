import dataset
import os

def find_by_lemma(lemma):
    db = dataset.connect('sqlite:///' + os.path.dirname(os.path.realpath(__file__)) + '/words.db')

    words_table = db['words']

    result = words_table.find_one(title=lemma)

    db.close()

    return result
