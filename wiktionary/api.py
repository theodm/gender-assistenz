import dataset


def find_by_lemma(lemma):
    db = dataset.connect('sqlite:///./wiktionary/words.db')

    words_table = db['words']

    result = words_table.find_one(title=lemma)

    db.close()

    return result
