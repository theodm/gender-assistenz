import nltk
import matplotlib
from nltk.corpus import udhr

languages = ['Chickasaw', 'English', 'German_Deutsch',
    'Greenlandic_Inuktikut', 'Hungarian_Magyar', 'Ibibio_Efik']


def read_tiger_corpus(valid_cols_n=15, col_words=1):
    result = []

    with open("tiger_release_aug07.corrected.16012013.conll09", encoding="UTF-8") as f:
        for line in f:
            parts = line.split()
            if len(parts) == valid_cols_n:
                result.append(parts[col_words])

    return result

print(read_tiger_corpus())

#
#
# word = udhr.words("German_Deutsch" + '-Latin1')
#
# print(len(word))
#
# cfd = nltk.ConditionalFreqDist(
#           (lang, len(word))
#           for lang in languages
#           for word in udhr.words(lang + '-Latin1'))
#
# cfd.plot(cumulative=True)