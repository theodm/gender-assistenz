import nltk
from HanTa import HanoverTagger as ht

tagger = ht.HanoverTagger('morphmodel_ger.pgz')

# Probleme: Mehrere Bedeutungen von Wörtern Bauer (Bäuerin) Bauer (Bauerin) Bauer (Familienname) von Bauende

sentence = 'Die Studenten sind in der Bibliothek.'
sentence2 = "Der Student ist in der Bibliothek."

sentence = 'Die Bibliothekare gehen ein Eis essen'
sentence = 'Die gefürchteten Bibliothekare gehen ein Eis essen'
sentence = "Gefürchtete Bibliothekare, die gehen ein Eis essen."
#sentence = "Gefürchtete Bibliothekare, deren Geldbörse geklaut wurde, die gehen ein Eis essen."
#sentence = "Eine Gruppe von gefürchteten eingeschlossenen Bibliothekaren, deren Geldbörse geklaut wurde, die gehen Eis essen."

sentence = 'Der Bibliothekar geht ein Eis essen'
sentence = 'Der gefürchtete Bibliothekar geht ein Eis essen'
sentence4 = 'Ein gefürchteter Bibliothekar, der geht ein Eis essen'
sentence4 = 'Ein gefürchteter Bibliothekar, dessen Geldbörse geklaut wurde, der geht ein Eis essen.'

sentence = "Der gute und anständige Bibliothekar geht ein Eis essen."


# Nominativ Plural
sentence = "Der Studenten wegen geht es ins Bett. Die Bürger sind empört. Die Kapitäne sind empört. Dies ist ein Zeitungsartikel und hier könnte Ihre Werbung stehen! Friseure, hier ein Test!"

# Kapitän: -e Kapitäne KapitänInnen -innen (1)
# Arzt: -e (mit Umlaut) Ärzte ÄrztInnen -innen (2)
# Student: -en Studenten  StudentInnen -innen (3a)
# Bauer: -n Bauern  BauerInnen -innen (3b)
# fraglich: Kind: -er Kinder kein weiblich (4)
# Schwager: -er (mit Umlaut) Schwäger SchwägerInnen (5) (aber Gott/Göttin)
# Täter: Null Täter TäterInnen (6)
# ??: Null (mit Umlaut) (bsp: Apfel/Äpfel) (7)
# Privatier: -s Privatier Privatiere (8)


# Mafioso Mafiosa

# Räuber
# Bürger -?? Bürgerinnen -innen Problem: Wie kann ich Plural Nominativ von Singular Nominativ unterscheiden
# Kapitäne -e Kapitäninnen -innen:
# Friseure -e



#-arm, -bold, -chen, -de, -e, -(er/ el)ei, -el, -er, -haft, -heit/ -keit/ -icht, -ian/ jan, -i, -in, -ismus, -leer, -lein, -ler, -ling, -los, -ner, -nis, -reich, -rich, -s, -sal, -schaft, -sel, -t, -tel, -tum, -ung, -voll

# "Arbeiter"
# "Friseure"

words = nltk.word_tokenize(sentence)


words_to_gender = [
    {
        "lemma": "student",

        "singular": "student",
        "gendered_singular": "student*In",

        "plural": "studenten",
        "gendered_plural": "student*Innen"
    },
    {
        "lemma": "bibliothekar",

        "singular": "bibliothekar",
        "gendered_singular": "Bibliothekar*In",

        "plural": "bibliothekare",
        "gendered_plural": "Bibliothekar*Innen"
    },

]

words_to_gender_only_lemma = list(map(lambda x: x["lemma"], words_to_gender))

print(f"words_to_gender_only_lemma: {words_to_gender_only_lemma}")

print(words)

tags = tagger.tag_sent(words, taglevel=7)
print(tags)

changes = []


def nn_get_suffix(tag):
    tag_parts = tag[2]

    for tp in tag_parts:
        if tp[1] == 'SUF_NN':
            return tp[0]

    return None

def tag_get_type(tag):
    return tag[3]


def tag_is_plural(tag):
    suffix = nn_get_suffix(tag)

    if suffix == "en":
        return True



    return False


for i, tag in enumerate(tags):
    print(f"Analyze word: {tag} ({tag[3]})")

    if tag_get_type(tag) == "NN":
        nn_suffix = nn_get_suffix(tag)
        has_plural_suffix = nn_suffix == "en" or nn_suffix == "e" or nn_suffix == "er"

        print(f" > Suffix: {nn_suffix}")

        if not tag[1] in words_to_gender_only_lemma:
            continue

        index_in_words = words_to_gender_only_lemma.index(tag[1])

        if has_plural_suffix:
            changes += ('REPLACE', i, words_to_gender[index_in_words]["gendered_plural"])
            continue

        def find_article_before():
            si = i

            while True:
                si = si - 1

                if si < 0:
                    return None

                tag_at_si = tags[si]

                if tag_get_type(tag_at_si) == "ADJA":
                    continue

                if tag_get_type(tag_at_si) == "ART":
                    return si

                return None

        article_before = find_article_before()

        if article_before:
            print(f" > article before: {tags[article_before]}")

        # Suche nach einem Artikel vor dem Nomen










print(changes)





# ART -> bestimmter ODER unbestimmter Artikel
# NN -> normales Nomen
# VAFIN -> finites Voll- oder Kopulaverb
# APPR -> Präposition; Zirkumposition links
# PRELAT -> attribuierendes Relativpronomen
# ADJ -> Adjektiv
# ADJA -> attributives Adjektiv
# ADJD -> adverbiales ODER prädikatives Adjektiv
# PRELS -> substituierendes Relativpronomen
# PDS -> substituierendes Demonstrativpronomen
# KON -> nebenordnende Konjunktion und, oder, aber
# volle Liste: https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&ved=2ahUKEwi0stuz1Y_xAhVBVhoKHXZ1BQ8QFjAAegQIBRAD&url=https%3A%2F%2Fwww.linguistik.hu-berlin.de%2Fde%2Finstitut%2Fprofessuren%2Fkorpuslinguistik%2Fmitarbeiter-innen%2Fhagen%2FSTTS_Tagset_Tiger&usg=AOvVaw3e83_0ql0irf_aGMl1NzXE

