from pipeline.full_pipeline import full_pipeline
from joblib import Memory
from loguru import logger

logger.remove()
memory = Memory("cachedir")

f = open("demofile3.txt", "r", encoding="utf-8")

count = 0

@memory.cache
def cached_full_pipeline(article):
    return full_pipeline(article)

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

total_correct = 0
total_incorrect = 0
total_incorrect2 = 0

while True:
    count += 1

    article = ""
    while True:
        line = f.readline()

        if "---" in line:
            break

        if "!\"§$%" in line or not line:
            break

        article += line

    new_article, r = parse_article(article)


    fpr = cached_full_pipeline(new_article)

    # print(new_article)
    # print(r)
    # print(fpr)

    def find_in_r(_from, _to):
        for w in r:
            if w["word_begin"] == _from and w["word_end"] == _to:
                return w

        return None


    def find_in_fpr(_from, _to):
        for w in fpr:
            if w["from"] == _from and w["to"] == _to:
                return w

        return None

    correct = 0
    incorrect = 0
    incorrect2 = 0
    # Wir suchen alle, die als ntbg markiert wurden und überprüfen, ob diese auch von
    # uns erkannt werden.
    for w in r:
        found = find_in_fpr(w["word_begin"], w["word_end"])

        if w["ntbg"] and (found and found["shouldBeGendered"]):
            print("correct: " + str(found))
            correct = correct + 1
        elif w["ntbg"]:
            print("incorrect: " + str(w) + " " + str(found))
            incorrect = incorrect + 1


    # Wir suchen alle, die als ntbg markiert wurden vom Skript, die aber tatsächlich nicht
    # gegendert werden muss (fälschlicherweise korrigiert)
    for w in fpr:
        found = find_in_r(w["from"], w["to"])

        if w["shouldBeGendered"] and not found:
            print("not found: " + str(w))
            incorrect2 = incorrect2 + 1

    print(correct)
    print(incorrect)
    print(incorrect2)

    total_correct = total_correct + correct
    total_incorrect = total_incorrect + incorrect
    total_incorrect2 = total_incorrect2 + incorrect2

    # print(article)
    # print("===")

    if "!\"§$%" in line or not line:
        break

print("total correct" + str(total_correct))
print("total incorrect" + str(total_incorrect))
print("total incorrect2" + str(total_incorrect2))

f.close()
