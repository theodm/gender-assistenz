import json
import re
import dataset
from lxml import etree as ET

from pgender.utils.regex import regex_first_or_none, regex_nth_or_none

db = dataset.connect('sqlite:///words.db')

words_table = db['words']


# def read_file(path):
#     file = open(path, mode='r', encoding="utf-8")
#     contents = file.read()
#     file.close()
#
#     return contents

continue_print = False

def print_cnt(str):
    if continue_print:
        print(str)

result = []

# Namespace der Tags innerhalb des Wiktionary-Exports
ns = "{http://www.mediawiki.org/xml/export-0.10/}"

for event, page_tag in ET.iterparse("dewiktionary-20210601-pages-articles.xml", events=("end",), tag=f"{ns}page"):
    title = page_tag.find(f"{ns}title")

    revision_tag = page_tag.find(f"{ns}revision")

    # is None, statt not, da ein Tag bei lxml eine Liste ist und eine leere Liste als falsy ausgewertet wird.
    if revision_tag is None:
        print_cnt("no revision tag for page, skipping...")
        continue

    text_tag = revision_tag.find(f"{ns}text")

    if text_tag is None:
        print_cnt("no text tag in revision tag for page, skipping...")
        continue

    text = text_tag.text

    if not text or "Deutsch Substantiv" not in text:
        print_cnt(f"{title.text} ist kein Substantiv")
        continue

    multiple_meaning_texts = text.split("\n=== {{Wortart|Substantiv|Deutsch}}")[1:]

    for text in multiple_meaning_texts:
        if len(multiple_meaning_texts) > 2:
            print(f"{title.text} has multiple meanings: {len(multiple_meaning_texts) - 1}")

        # Genus auslesen
        genus = regex_first_or_none('\\|Genus=([a-z])', text)
        if not genus:
            print_cnt(f"{title.text} enthält keine Genus-Informationen")
            continue

        formen = [
            "Nominativ Singular",
            "Nominativ Plural",
            "Genitiv Singular",
            "Genitiv Plural",
            "Dativ Singular",
            "Dativ Plural",
            "Akkusativ Singular",
            "Akkusativ Plural",

            "Nominativ Plural 1",
            "Genitiv Plural 1",
            "Dativ Plural 1",
            "Akkusativ Plural 1",

            "Nominativ Plural 2",
            "Genitiv Plural 2",
            "Dativ Plural 2",
            "Akkusativ Plural 2",
        ]

        formen_result = []
        for form in formen:
            form_result = regex_first_or_none(f"\\|{form}=(.*)\n", text)

            formen_result.append(form_result.strip() if form_result is not None else None)

        #print(formen_result)

        # Bsp.: [[Portierfrau]], [[Portierin]], [[Portiersfrau]]
        weibliche_formen_raw = regex_nth_or_none("Weibliche Wortformen}}\\n:\\[(.*)?\\] (.*)", text, 1)
        weibliche_formen_matches = None
        if weibliche_formen_raw:
            weibliche_formen_matches = re.findall("\\[\\[(.*)?\\]\\]", weibliche_formen_raw)

        maennliche_formen_raw = regex_nth_or_none("Männliche Wortformen}}\\n:\\[(.*)?\\] (.*)", text, 1)
        maennliche_formen_matches = None
        if maennliche_formen_raw:
            maennliche_formen_matches = re.findall("\\[\\[(.*)?\\]\\]", maennliche_formen_raw)

        if not maennliche_formen_matches and not weibliche_formen_matches:
            print_cnt(f"{title.text} enthält weder männliche noch weibliche Formen.")
            continue

        print(title.text + f" [{genus}]")
        result += title.text + f" [{genus}]"

        words_table.insert(
            dict(
                title=title.text,
                genus=genus,

                nominativ_singular=formen_result[0],
                nominativ_plural=formen_result[1],
                genitiv_singular=formen_result[2],
                genitiv_plural=formen_result[3],
                dativ_singular=formen_result[4],
                dativ_plural=formen_result[5],
                akkusativ_singular=formen_result[6],
                akkusativ_plural=formen_result[7],

                nominativ_plural1=formen_result[8],
                genitiv_plural1=formen_result[9],
                dativ_plural1=formen_result[10],
                akkusativ_plural1=formen_result[11],
                nominativ_plural2=formen_result[12],
                genitiv_plural2=formen_result[13],
                dativ_plural2=formen_result[14],
                akkusativ_plural2=formen_result[15],

                maennliche_formen=None if not maennliche_formen_matches else json.dumps(maennliche_formen_matches),
                weibliche_formen=None if not weibliche_formen_matches else json.dumps(weibliche_formen_matches)
            )
        )

    page_tag.clear()

print(len(result))

db.close()