import json
import re
import dataset
import requests
from lxml import etree as ET
from bs4 import BeautifulSoup

from pgender.utils.regex import regex_first_or_none, regex_nth_or_none, regex_m_first_or_none
from pgender.wiktionary.api import find_verb_by_title, find_verb_by_any_form

db = dataset.connect('sqlite:///words.db')

verbs_table = db['verbs']

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

    if not text:
        continue

    verb_title = regex_first_or_none('== (.*) \(Konjugation\)', text)

    if not verb_title:
        continue

    verb_title = verb_title.replace("[", "").replace("]", "").replace(", untrennbar", "").replace("{{Anker|untrennbar}}", "").replace("{{Anker|trennbar}}", "").replace("{{Anker|sein}}", "")

    if verb_title == "erpacken":
        continue

    template = regex_first_or_none('{{Deutsch Verb (.*)}}', text)

    if not template:
        continue

    #
    # Hiermit wird ein Wiktionary-Template in ein internes Format,
    # zur besseren Bearbeitung umgewandelt.
    #
    # Bsp.: {{Deutsch Verb unregelmäßig|1=|2=|3=|4=|5=|6=|7=|8=|9=|10=|Hilfsverb=|vp=|zp=|gerund=|Partizip+=|reflexiv=|zr=}}
    #       {{Deutsch Verb unregelmäßig|1|2|3|4|5|6|7|8|9|10|Hilfsverb=|vp=|zp=|gerund=|Partizip+=|reflexiv=|zr=}}
    #
    #       {{Deutsch Verb unregelmäßig|2=beiß|3=biss|4=biss|5=gebissen|7=-s|vp=ja|zp=ja|gerund=ja}}
    #
    def parse_wiki_template(template):
        obj = {}

        args = template.split("|")

        obj["template_name"] = args[0]

        for arg in args:
            kv_pair = arg.split("=")

            if len(kv_pair) > 1:
                obj[kv_pair[0]] = kv_pair[1]

        index_param_index = 1
        for arg in args:
            if "=" not in arg and arg != args[0]:
                obj[f"{index_param_index}"] = arg
                index_param_index = index_param_index + 1

        return obj

    template = parse_wiki_template(template)

    result = {}
    
    def t(x):
        return template.get(x, "")

    def tn(x):
        return template.get(x, None)

    result["title"] = verb_title

    print(verb_title)
    if find_verb_by_title(verb_title):
        continue

    r = requests.get("https://de.wiktionary.org/wiki/Flexion:" + verb_title)

    r_text = r.text\
        .replace("Sg. 1. Pers.", "1. Person Singular")\
        .replace("Sg. 2. Pers.", "2. Person Singular")\
        .replace("Sg. 3. Pers.", "3. Person Singular")\
        .replace("Pl. 1. Pers.", "1. Person Plural")\
        .replace("Pl. 2. Pers.", "2. Person Plural")\
        .replace("Pl. 3. Pers.", "3. Person Plural")

    soup = BeautifulSoup(r_text, 'html.parser')


    table_heading = soup.find(id="Indikativ_und_Konjunktiv")
    if not table_heading:
        print("SKIPPED: " + verb_title)
        continue

    praesens_table = table_heading.parent.findNext('table')


    def parent_until_td(obj):
        if obj.parent.name == "td":
            return obj.parent

        return parent_until_td(obj.parent)


    praesens_1_sing = parent_until_td(praesens_table.findAll(text=re.compile("1. Person Singular"))[0])

    result["praes_akt_ind_1_sing"] = regex_first_or_none("ich ([a-zA-Zäöüß]+)", praesens_1_sing.findNext('td').text)
    result["praes_akt_konj1_1_sing"] = regex_first_or_none("ich ([a-zA-Zäöüß]+)", praesens_1_sing.findNext('td').findNext('td').text)

    praesens_2_sing = parent_until_td(praesens_table.findAll(text=re.compile("2. Person Singular"))[0])

    result["praes_akt_ind_2_sing"] = regex_first_or_none("du ([a-zA-Zäöüß]+)", praesens_2_sing.findNext('td').text)
    result["praes_akt_konj1_2_sing"] = regex_first_or_none("du ([a-zA-Zäöüß]+)", praesens_2_sing.findNext('td').findNext('td').text)

    praesens_3_sing = parent_until_td(praesens_table.findAll(text=re.compile("3. Person Singular"))[0])

    result["praes_akt_ind_3_sing"] = regex_first_or_none("er/sie/es ([a-zA-Zäöüß]+)", praesens_3_sing.findNext('td').text)
    result["praes_akt_konj1_3_sing"] = regex_first_or_none("er/sie/es ([a-zA-Zäöüß]+)", praesens_3_sing.findNext('td').findNext('td').text)

    praesens_1_plur = parent_until_td(praesens_table.findAll(text=re.compile("1. Person Plural"))[0])

    result["praes_akt_ind_1_plur"] = regex_first_or_none("wir ([a-zA-Zäöüß]+)", praesens_1_plur.findNext('td').text)
    result["praes_akt_konj1_1_plur"] = regex_first_or_none("wir ([a-zA-Zäöüß]+)", praesens_1_plur.findNext('td').findNext('td').text)

    praesens_2_plur = parent_until_td(praesens_table.findAll(text=re.compile("2. Person Plural"))[0])

    result["praes_akt_ind_2_plur"] = regex_first_or_none("ihr ([a-zA-Zäöüß]+)", praesens_2_plur.findNext('td').text)
    result["praes_akt_konj1_2_plur"] = regex_first_or_none("ihr ([a-zA-Zäöüß]+)", praesens_2_plur.findNext('td').findNext('td').text)

    praesens_3_plur = parent_until_td(praesens_table.findAll(text=re.compile("3. Person Plural"))[0])

    result["praes_akt_ind_3_plur"] = regex_first_or_none("sie ([a-zA-Zäöüß]+)", praesens_3_plur.findNext('td').text)
    result["praes_akt_konj1_3_plur"] = regex_first_or_none("sie ([a-zA-Zäöüß]+)", praesens_3_plur.findNext('td').findNext('td').text)

    praet_table = table_heading.parent.findNext('table')

    praet_1_sing = parent_until_td(praet_table.findAll(text=re.compile("1. Person Singular"))[1])

    result["praet_akt_ind_1_sing"] = regex_first_or_none("ich ([a-zA-Zäöüß]+)", praet_1_sing.findNext('td').text)
    result["praet_akt_konj1_1_sing"] = regex_first_or_none("ich ([a-zA-Zäöüß]+)", praet_1_sing.findNext('td').findNext('td').text)

    praet_2_sing = parent_until_td(praet_table.findAll(text=re.compile("2. Person Singular"))[1])

    result["praet_akt_ind_2_sing"] = regex_first_or_none("du ([a-zA-Zäöüß]+)", praet_2_sing.findNext('td').text)
    result["praet_akt_konj1_2_sing"] = regex_first_or_none("du ([a-zA-Zäöüß]+)", praet_2_sing.findNext('td').findNext('td').text)

    praet_3_sing = parent_until_td(praesens_table.findAll(text=re.compile("3. Person Singular"))[1])

    result["praet_akt_ind_3_sing"] = regex_first_or_none("er/sie/es ([a-zA-Zäöüß]+)", praet_3_sing.findNext('td').text)
    result["praet_akt_konj1_3_sing"] = regex_first_or_none("er/sie/es ([a-zA-Zäöüß]+)", praet_3_sing.findNext('td').findNext('td').text)

    praet_1_plur = parent_until_td(praet_table.findAll(text=re.compile("1. Person Plural"))[1])

    result["praet_akt_ind_1_plur"] = regex_first_or_none("wir ([a-zA-Zäöüß]+)", praet_1_plur.findNext('td').text)
    result["praet_akt_konj1_1_plur"] = regex_first_or_none("wir ([a-zA-Zäöüß]+)", praet_1_plur.findNext('td').findNext('td').text)

    praet_2_plur = parent_until_td(praesens_table.findAll(text=re.compile("2. Person Plural"))[1])

    result["praet_akt_ind_2_plur"] = regex_first_or_none("ihr ([a-zA-Zäöüß]+)", praet_2_plur.findNext('td').text)
    result["praet_akt_konj1_2_plur"] = regex_first_or_none("ihr ([a-zA-Zäöüß]+)", praet_2_plur.findNext('td').findNext('td').text)

    praet_3_plur = parent_until_td(praesens_table.findAll(text=re.compile("3. Person Plural"))[1])

    result["praet_akt_ind_3_plur"] = regex_first_or_none("sie ([a-zA-Zäöüß]+)", praet_3_plur.findNext('td').text)
    result["praet_akt_konj1_3_plur"] = regex_first_or_none("sie ([a-zA-Zäöüß]+)", praet_3_plur.findNext('td').findNext('td').text)

    # if template['template_name'] == "regelmäßig":
    #     # https://de.wiktionary.org/wiki/Vorlage:Deutsch_Verb_regelm%C3%A4%C3%9Fig
    #
    #     # Präsens - Aktiv - Indikativ
    #     result["praes_akt_ind_1_sing"] = f"{t('1')}{t('2')}{t('3')}"
    #     result["praes_akt_ind_2_sing"] = f"{t('1')}{t('2')}{t('3')}st"
    #     result["praes_akt_ind_3_sing"] = f"{t('1')}{t('2')}{t('3')}t"
    #     result["praes_akt_ind_1_plur"] = f"{t('1')}{t('2')}{t('3')}{t('4')}n"
    #     result["praes_akt_ind_2_plur"] = f"{t('1')}{t('2')}{t('3')}t"
    #     result["praes_akt_ind_3_plur"] = f"{t('1')}{t('2')}{t('3')}{t('4')}n"
    #
    #     # Präsens - Aktiv - Konjunktiv I
    #     result["praes_akt_konj1_1_sing"] = f"{t('1')}{t('2')}{t('3')}{t('4')}"
    #     result["praes_akt_konj1_2_sing"] = f"{t('1')}{t('2')}{t('3')}{t('4')}est"
    #     result["praes_akt_konj1_3_sing"] = f"{t('1')}{t('2')}{t('3')}e"
    #     result["praes_akt_konj1_1_plur"] = f"{t('1')}{t('2')}{t('3')}{t('4')}n"
    #     result["praes_akt_konj1_2_plur"] = f"{t('1')}{t('2')}{t('3')}et"
    #     result["praes_akt_konj1_3_plur"] = f"{t('1')}{t('2')}{t('3')}{t('4')}n"
    #
    #     # Präteritum - Aktiv - Indikativ
    #     result["praet_akt_ind_1_sing"] = f"{t('1')}{t('2')}{t('3')}te"
    #     result["praet_akt_ind_2_sing"] = f"{t('1')}{t('2')}{t('3')}test"
    #     result["praet_akt_ind_3_sing"] = f"{t('1')}{t('2')}{t('3')}te"
    #     result["praet_akt_ind_1_plur"] = f"{t('1')}{t('2')}{t('3')}ten"
    #     result["praet_akt_ind_2_plur"] = f"{t('1')}{t('2')}{t('3')}tet"
    #     result["praet_akt_ind_3_plur"] = f"{t('1')}{t('2')}{t('3')}ten"
    #
    #     # Präteritum - Aktiv - Konjunktiv II
    #     result["praet_akt_konj2_1_sing"] = f"{t('1')}{t('2')}{t('3')}te"
    #     result["praet_akt_konj2_2_sing"] = f"{t('1')}{t('2')}{t('3')}test"
    #     result["praet_akt_konj2_3_sing"] = f"{t('1')}{t('2')}{t('3')}te"
    #     result["praet_akt_konj2_1_plur"] = f"{t('1')}{t('2')}{t('3')}ten"
    #     result["praet_akt_konj2_2_plur"] = f"{t('1')}{t('2')}{t('3')}tet"
    #     result["praet_akt_konj2_3_plur"] = f"{t('1')}{t('2')}{t('3')}ten"
    #
    # if template['template_name'] == "unregelmäßig":
    #     # https://de.wiktionary.org/wiki/Vorlage:Deutsch_Verb_unregelm%C3%A4%C3%9Fig
    #
    #     def unregelmaessig_praes_akt_ind_1_sing():
    #         if t('Indikativ Präsens (ich)'):
    #             return t('Indikativ Präsens (ich)')
    #
    #         if len(t('10')) > 0:
    #             if t('10') in ["dürfen", "können", "mögen", "müssen", "sollen", "wissen", "wollen"]:
    #                 if len(t('6')) > 0:
    #                     return t('6')
    #                 else:
    #                     return t('2')
    #             else:
    #                 if len(t('6')) > 0:
    #                     return t('6')
    #                 else:
    #                     return t('2') + "e"
    #
    #         return t('2') + "e"
    #
    #     # Präsens - Aktiv - Indikativ
    #     result["praes_akt_ind_1_sing"] = unregelmaessig_praes_akt_ind_1_sing()
    #     result["praes_akt_ind_2_sing"] = f"{t('2')}st"
    #     result["praes_akt_ind_3_sing"] = f"{t('2')}t"
    #     result["praes_akt_ind_1_plur"] = f"{t('2')}en"
    #     result["praes_akt_ind_2_plur"] = f"{t('2')}t"
    #     result["praes_akt_ind_3_plur"] = f"{t('2')}en"
    #
    #     # Präsens - Aktiv - Konjunktiv I
    #     result["praes_akt_konj1_1_sing"] = f"{t('2')}e"
    #     result["praes_akt_konj1_2_sing"] = f"{t('2')}est"
    #     result["praes_akt_konj1_3_sing"] = f"{t('2')}e"
    #     result["praes_akt_konj1_1_plur"] = f"{t('2')}en"
    #     result["praes_akt_konj1_2_plur"] = f"{t('2')}et"
    #     result["praes_akt_konj1_3_plur"] = f"{t('2')}en"
    #
    #     # Präteritum - Aktiv - Indikativ
    #     result["praet_akt_ind_1_sing"] = f"{t('3')}"
    #     result["praet_akt_ind_2_sing"] = f"{t('3')}st"
    #     result["praet_akt_ind_3_sing"] = f"{t('3')}"
    #     result["praet_akt_ind_1_plur"] = f"{t('3')}en"
    #     result["praet_akt_ind_2_plur"] = f"{t('3')}t"
    #     result["praet_akt_ind_3_plur"] = f"{t('3')}en"
    #
    #     # Präteritum - Aktiv - Konjunktiv II
    #     result["praet_akt_konj2_1_sing"] = f"{t('4')}e"
    #     result["praet_akt_konj2_2_sing"] = f"{t('4')}est"
    #     result["praet_akt_konj2_3_sing"] = f"{t('4')}e"
    #     result["praet_akt_konj2_1_plur"] = f"{t('4')}en"
    #     result["praet_akt_konj2_2_plur"] = f"{t('4')}et"
    #     result["praet_akt_konj2_3_plur"] = f"{t('4')}en"

    print(verb_title + " args: " + template["template_name"] + " t: " + str(template) + " result: " + str(result))

    verbs_table.insert(
        result
    )

    page_tag.clear()

db.close()