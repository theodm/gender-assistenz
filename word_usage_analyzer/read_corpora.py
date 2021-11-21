import gc

import dataset

from _spacy import spacify_with_coref
from ntbg import NO_FEMININE_FORM
from pipeline.full_pipeline import full_pipeline
from joblib import Memory
from loguru import logger

logger.remove()
memory = Memory("cachedir", verbose=0)

f = open("demofile3.txt", "r", encoding="utf-8")

count = 0

db = dataset.connect('sqlite:///results.db')

marks_table = db['marks']


@memory.cache
def cached_full_pipeline(article):
    return full_pipeline(article)

@memory.cache
def parse_article(article):
    t = article
    ci = 0
    new_article = ""

    result = []

    number_of_ignored_chars = 0

    while ci < len(article):
        if (t[ci] == "!" or t[ci] == "\\") and t[ci + 1] == "-" and t[ci + 2] == "-":
            ntbg = True if t[ci] == "!" else False

            # Zum Anfang des Wortes springen
            ci = ci + 3
            number_of_ignored_chars += 3

            word = ""
            while True:
                if t[ci] == "-" and t[ci + 1] == "-":
                    result.append({
                        "word": word,
                        "word_begin": ci - len(word) - number_of_ignored_chars ,
                        "word_end": ci - number_of_ignored_chars,
                        "ntbg": ntbg
                    })

                    ci = ci + 2
                    number_of_ignored_chars = number_of_ignored_chars + 2

                    break

                word = word + t[ci]
                new_article = new_article + article[ci]
                ci = ci + 1

            continue

        if t[ci] == "-" and t[ci + 1] == "-":
            raise Exception("-- found: " + article[ci-10:ci+20])

        new_article = new_article + article[ci]
        ci = ci + 1

    return new_article, result

articles = 0
sentences = 0
words = 0

total_marks = 0
total_marks_was_correct = 0
total_marks_was_incorrect = 0

total_marks_without_trivial = 0

total_marks_ntbg = 0
total_marks_not_ntbg = 0
total_marks_ntbg_correct = 0
total_marks_ntbg_incorrect = 0
total_marks_not_ntbg_correct = 0
total_marks_not_ntbg_incorrect = 0

total_marks_nouns = 0
total_marks_pronouns = 0
total_marks_ntbg_nouns = 0
total_marks_ntbg_pronouns = 0
total_marks_not_ntbg_nouns = 0
total_marks_not_ntbg_pronouns = 0


total_marks_nouns_ntbg_correct = 0
total_marks_nouns_ntbg_incorrect = 0
total_marks_nouns_not_ntbg_correct = 0
total_marks_nouns_not_ntbg_incorrect = 0

total_marks_pronouns_ntbg_correct = 0
total_marks_pronouns_ntbg_incorrect = 0
total_marks_pronouns_not_ntbg_correct = 0
total_marks_pronouns_not_ntbg_incorrect = 0

total_marks_singular = 0
total_marks_plural = 0
total_marks_number_could_not_be_determined = 0
total_marks_ntbg_singular = 0
total_marks_not_ntbg_singular = 0
total_marks_ntbg_plural = 0
total_marks_not_ntbg_plural = 0

total_marks_singular_ntbg_correct = 0
total_marks_singular_ntbg_incorrect = 0
total_marks_singular_not_ntbg_correct = 0
total_marks_singular_not_ntbg_incorrect = 0

total_marks_plural_ntbg_correct = 0
total_marks_plural_ntbg_incorrect = 0
total_marks_plural_not_ntbg_correct = 0
total_marks_plural_not_ntbg_incorrect = 0

total_was_not_marked_but_found = 0
total_was_not_marked_but_found_ntbg = 0
total_was_not_marked_but_found_not_ntbg = 0

while True:
    count = count + 1

    print(count)

    print("----")


    article = ""
    while True:
        line = f.readline()

        if "---" in line:
            break

        if "!\"§$%" in line or not line:
            break

        article += line

    new_article, marked_words = parse_article(article)

    fpr = cached_full_pipeline(new_article)

    # print(new_article)
    # print(r)
    # print(fpr)


    def find_in_r(_from, _to):
        for w in marked_words:
            if w["word_begin"] == _from and w["word_end"] == _to:
                return w

        return None


    def find_in_pipeline_result(_from, _to):
        for w in fpr:
            if w["from"] == _from and w["to"] == _to:
                return w

        return None

    spacify = spacify_with_coref(new_article)
    
    print(new_article)
    
    # Wir gehen alle markierten Worte durch.
    for found_word in marked_words:
        # Wir überprüfen, ob das Wort auch durch das System erkannt wird.
        marked_word = find_in_pipeline_result(found_word["word_begin"], found_word["word_end"])
        
        # Ist die Markierung grunsätzlich zu korrigieren?
        if found_word["ntbg"]:
            ntbg = True
        else:
            ntbg = False

        begin_ = [x for x in spacify if x.idx == found_word["word_begin"]]
        if not begin_:
            print(f"could not find: {found_word}")
            continue

        _word = begin_[0]

        # Überprüfung: Ist das Vorkommen singular oder plural?
        number = "<undefined>"
        is_singular = "?"
        if _word.morph.get("Number") and _word.morph.get("Number")[0]:
            number = _word.morph.get("Number")[0]
            is_singular = "y" if number == "Sing" else "n"

        # Überprüfung: Ist das Vorkommen ein Nomen oder ein Pronomen?
        pos = _word.pos_
        is_noun = (pos == "NOUN")

        tag = _word.tag_

        if not marked_word: 
            was_found = False
            is_trivial = False

            # Wenn das Vorkommen durch die Pipeline nicht gefunden wurde, ist es
            # nur korrekt, wenn es nicht gegendert werden muss. Dann wurde es zwar vom
            # ersten Schritt nicht gefunden; das Ergebnis stimmt aber trotzdem.
            was_correct = not ntbg
        else:
            pipeline_ntbg = marked_word["shouldBeGendered"]
            was_correct = (pipeline_ntbg == ntbg)
            is_trivial = False
            if was_correct:
                if marked_word["reasonNotGendered"] and marked_word["reasonNotGendered"][0] and marked_word["reasonNotGendered"][0][0]:
                    is_trivial = marked_word["reasonNotGendered"][0][0] == NO_FEMININE_FORM

        total_marks = total_marks + 1
        if was_correct:
            total_marks_was_correct = total_marks_was_correct + 1
        
        if not was_correct:
            total_marks_was_incorrect = total_marks_was_incorrect + 1

        if not total_marks_without_trivial:
            total_marks_without_trivial = 0

        if ntbg: 
            total_marks_ntbg = total_marks_ntbg + 1

        if not ntbg: 
            total_marks_not_ntbg = total_marks_not_ntbg + 1

        if ntbg and was_correct:
            total_marks_ntbg_correct = total_marks_ntbg_correct + 1
        if ntbg and not was_correct:
            total_marks_ntbg_incorrect = total_marks_ntbg_incorrect + 1

        if not ntbg and was_correct:
            total_marks_not_ntbg_correct = total_marks_not_ntbg_correct + 1
        if not ntbg and not was_correct:
            total_marks_not_ntbg_incorrect = total_marks_not_ntbg_incorrect + 1

        if is_noun:
            total_marks_nouns = total_marks_nouns + 1
        if not is_noun:
            total_marks_pronouns = total_marks_pronouns + 1

        if ntbg and is_noun:
            total_marks_ntbg_nouns = total_marks_ntbg_nouns + 1
        if ntbg and not is_noun:
            total_marks_ntbg_pronouns = total_marks_ntbg_pronouns + 1
        if not ntbg and is_noun:
            total_marks_not_ntbg_nouns = total_marks_not_ntbg_nouns + 1
        if not ntbg and not is_noun:
            total_marks_not_ntbg_pronouns = total_marks_not_ntbg_pronouns + 1
        
        if is_noun:
            if ntbg and was_correct:
                total_marks_nouns_ntbg_correct = total_marks_nouns_ntbg_correct + 1
            if ntbg and not was_correct:
                total_marks_nouns_ntbg_incorrect = total_marks_nouns_ntbg_incorrect + 1
            if not ntbg and was_correct:
                total_marks_nouns_not_ntbg_correct = total_marks_nouns_not_ntbg_correct + 1
            if not ntbg and not was_correct:
                total_marks_nouns_not_ntbg_incorrect = total_marks_nouns_not_ntbg_incorrect + 1

        if not is_noun:
            if ntbg and was_correct:
                total_marks_pronouns_ntbg_correct = total_marks_pronouns_ntbg_correct + 1
            if ntbg and not was_correct:
                total_marks_pronouns_ntbg_incorrect = total_marks_pronouns_ntbg_incorrect + 1
            if not ntbg and was_correct:
                total_marks_pronouns_not_ntbg_correct = total_marks_pronouns_not_ntbg_correct + 1
            if not ntbg and not was_correct:
                total_marks_pronouns_not_ntbg_incorrect = total_marks_pronouns_not_ntbg_incorrect + 1

        if not is_singular or is_singular == "?":
            total_marks_nubmer_could_not_be_determined = total_marks_number_could_not_be_determined + 1

        if is_singular == "y":
            total_marks_singular = total_marks_singular + 1

        if is_singular == "n":
            total_marks_plural = total_marks_plural + 1

        if ntbg and is_singular == "y":
            total_marks_ntbg_singular = total_marks_ntbg_singular + 1
        if ntbg and is_singular == "n":
            total_marks_not_ntbg_singular = total_marks_not_ntbg_singular + 1
        if not ntbg and is_singular == "y":
            total_marks_ntbg_plural = total_marks_ntbg_plural + 1
        if not ntbg and is_singular == "n":
            total_marks_not_ntbg_plural = total_marks_not_ntbg_plural + 1
                    
        if is_singular == "y":
            if ntbg and was_correct:
                total_marks_singular_ntbg_correct = total_marks_singular_ntbg_correct + 1
            if ntbg and not was_correct:
                total_marks_singular_ntbg_incorrect = total_marks_singular_ntbg_incorrect + 1
            if not ntbg and was_correct:
                total_marks_singular_not_ntbg_correct = total_marks_singular_not_ntbg_correct + 1
            if not ntbg and not was_correct:
                total_marks_singular_not_ntbg_incorrect = total_marks_singular_not_ntbg_incorrect + 1

        if is_singular == "n":
            if ntbg and was_correct:
                total_marks_plural_ntbg_correct = total_marks_plural_ntbg_correct + 1
            if ntbg and not was_correct:
                total_marks_plural_ntbg_incorrect = total_marks_plural_ntbg_incorrect + 1
            if not ntbg and was_correct:
                total_marks_plural_not_ntbg_correct = total_marks_plural_not_ntbg_correct + 1
            if not ntbg and not was_correct:
                total_marks_plural_not_ntbg_incorrect = total_marks_plural_not_ntbg_incorrect + 1

#        print(f"ntbg: {ntbg} was_correct: {was_correct} is_noun: {is_noun} is_singular: {is_singular} _pos: {pos} Number: {number} " + str(marked_word) + " " + str(found_word))

        marks_table.upsert({
            "uniqid": str(count) + "_" + str(found_word["word_begin"]),
            "ntbg": ntbg,
            "was_correct": was_correct,
            "article": article,
            "new_article": new_article,
            "is_trivial": is_trivial,
            "is_noun": is_noun,
            "is_singular": is_singular,
            "_pos": pos,
            "_tag": tag,
            "Number": number,
            "marked_word": str(marked_word),
            "found_word": str(found_word)
        }, ["uniqid"])

    # Wir suchen alle, die als ntbg markiert wurden vom Skript, die aber tatsächlich nicht
    # gegendert werden muss (fälschlicherweise korrigiert)
    for found_word in fpr:
        marked_word = find_in_r(found_word["from"], found_word["to"])
        
        if not marked_word:
            total_was_not_marked_but_found = total_was_not_marked_but_found + 1

            if found_word["shouldBeGendered"]:
                total_was_not_marked_but_found_ntbg = total_was_not_marked_but_found_ntbg + 1
                print(f"incorrect2: {found_word}")
            else:
                total_was_not_marked_but_found_not_ntbg = total_was_not_marked_but_found_not_ntbg + 1
                print(f"incorrect__2: {found_word}")



    articles = articles + 1

    sentences = sentences + len([x for x in spacify.sents])
    words = words + len(spacify)

    # print(article)
    # print("===")

    if "!\"§$%" in line or not line:
        break

print("articles : " + str(articles))
print("sentences : " + str(sentences))
print("words : " + str(words))

print("total_marks : " + str(total_marks))
print("total_marks_was_correct : " + str(total_marks_was_correct))
print("total_marks_was_incorrect : " + str(total_marks_was_incorrect))

print("total_marks_ntbg : " + str(total_marks_ntbg))
print("total_marks_not_ntbg : " + str(total_marks_not_ntbg))
print("total_marks_ntbg_correct : " + str(total_marks_ntbg_correct))
print("total_marks_ntbg_incorrect : " + str(total_marks_ntbg_incorrect))
print("total_marks_not_ntbg_correct : " + str(total_marks_not_ntbg_correct))
print("total_marks_not_ntbg_incorrect : " + str(total_marks_not_ntbg_incorrect))

print("total_marks_nouns : " + str(total_marks_nouns))
print("total_marks_pronouns : " + str(total_marks_pronouns))
print("total_marks_ntbg_nouns : " + str(total_marks_ntbg_nouns))
print("total_marks_ntbg_pronouns : " + str(total_marks_ntbg_pronouns))
print("total_marks_not_ntbg_nouns : " + str(total_marks_not_ntbg_nouns))
print("total_marks_not_ntbg_pronouns : " + str(total_marks_not_ntbg_pronouns))


print("total_marks_nouns_ntbg_correct : " + str(total_marks_nouns_ntbg_correct))
print("total_marks_nouns_ntbg_incorrect : " + str(total_marks_nouns_ntbg_incorrect))
print("total_marks_nouns_not_ntbg_correct : " + str(total_marks_nouns_not_ntbg_correct))
print("total_marks_nouns_not_ntbg_incorrect : " + str(total_marks_nouns_not_ntbg_incorrect))

print("total_marks_pronouns_ntbg_correct : " + str(total_marks_pronouns_ntbg_correct))
print("total_marks_pronouns_ntbg_incorrect : " + str(total_marks_pronouns_ntbg_incorrect))
print("total_marks_pronouns_not_ntbg_correct : " + str(total_marks_pronouns_not_ntbg_correct))
print("total_marks_pronouns_not_ntbg_incorrect : " + str(total_marks_pronouns_not_ntbg_incorrect))

print("total_marks_singular : " + str(total_marks_singular))
print("total_marks_plural : " + str(total_marks_plural))
print("total_marks_number_could_not_be_determined : " + str(total_marks_number_could_not_be_determined))
print("total_marks_ntbg_singular : " + str(total_marks_ntbg_singular))
print("total_marks_not_ntbg_singular : " + str(total_marks_not_ntbg_singular))
print("total_marks_ntbg_plural : " + str(total_marks_ntbg_plural))
print("total_marks_not_ntbg_plural : " + str(total_marks_not_ntbg_plural))

print("total_marks_singular_ntbg_correct : " + str(total_marks_singular_ntbg_correct))
print("total_marks_singular_ntbg_incorrect : " + str(total_marks_singular_ntbg_incorrect))
print("total_marks_singular_not_ntbg_correct : " + str(total_marks_singular_not_ntbg_correct))
print("total_marks_singular_not_ntbg_incorrect : " + str(total_marks_singular_not_ntbg_incorrect))

print("total_marks_plural_ntbg_correct : " + str(total_marks_plural_ntbg_correct))
print("total_marks_plural_ntbg_incorrect : " + str(total_marks_plural_ntbg_incorrect))
print("total_marks_plural_not_ntbg_correct : " + str(total_marks_plural_not_ntbg_correct))
print("total_marks_plural_not_ntbg_incorrect : " + str(total_marks_plural_not_ntbg_incorrect))

print("total_was_not_marked_but_found : " + str(total_was_not_marked_but_found))
print("total_was_not_marked_but_found_ntbg : " + str(total_was_not_marked_but_found_ntbg))
print("total_was_not_marked_but_found_not_ntbg : " + str(total_was_not_marked_but_found_not_ntbg))

f.close()
