import json
import re
import dataset
from lxml import etree as ET

from pgender.utils.regex import regex_first_or_none, regex_nth_or_none

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

    result["title"] = verb_title

    if template['template_name'] == "regelmäßig":
        # https://de.wiktionary.org/wiki/Vorlage:Deutsch_Verb_regelm%C3%A4%C3%9Fig

        # Präsens - Aktiv - Indikativ
        result["praes_akt_ind_1_sing"] = f"{t('1')}{t('2')}{t('3')}"
        result["praes_akt_ind_2_sing"] = f"{t('1')}{t('2')}{t('3')}st"
        result["praes_akt_ind_3_sing"] = f"{t('1')}{t('2')}{t('3')}t"
        result["praes_akt_ind_1_plur"] = f"{t('1')}{t('2')}{t('3')}{t('4')}n"
        result["praes_akt_ind_2_plur"] = f"{t('1')}{t('2')}{t('3')}t"
        result["praes_akt_ind_3_plur"] = f"{t('1')}{t('2')}{t('3')}{t('4')}n"

        # Präsens - Aktiv - Konjunktiv I
        result["praes_akt_konj1_1_sing"] = f"{t('1')}{t('2')}{t('3')}{t('4')}"
        result["praes_akt_konj1_2_sing"] = f"{t('1')}{t('2')}{t('3')}{t('4')}est"
        result["praes_akt_konj1_3_sing"] = f"{t('1')}{t('2')}{t('3')}e"
        result["praes_akt_konj1_1_plur"] = f"{t('1')}{t('2')}{t('3')}{t('4')}n"
        result["praes_akt_konj1_2_plur"] = f"{t('1')}{t('2')}{t('3')}et"
        result["praes_akt_konj1_3_plur"] = f"{t('1')}{t('2')}{t('3')}{t('4')}n"

        # Präteritum - Aktiv - Indikativ
        result["praet_akt_ind_1_sing"] = f"{t('1')}{t('2')}{t('3')}te"
        result["praet_akt_ind_2_sing"] = f"{t('1')}{t('2')}{t('3')}test"
        result["praet_akt_ind_3_sing"] = f"{t('1')}{t('2')}{t('3')}te"
        result["praet_akt_ind_1_plur"] = f"{t('1')}{t('2')}{t('3')}ten"
        result["praet_akt_ind_2_plur"] = f"{t('1')}{t('2')}{t('3')}tet"
        result["praet_akt_ind_3_plur"] = f"{t('1')}{t('2')}{t('3')}ten"

        # Präteritum - Aktiv - Konjunktiv II
        result["praet_akt_konj1_1_sing"] = f"{t('1')}{t('2')}{t('3')}te"
        result["praet_akt_konj1_2_sing"] = f"{t('1')}{t('2')}{t('3')}test"
        result["praet_akt_konj1_3_sing"] = f"{t('1')}{t('2')}{t('3')}te"
        result["praet_akt_konj1_1_plur"] = f"{t('1')}{t('2')}{t('3')}ten"
        result["praet_akt_konj1_2_plur"] = f"{t('1')}{t('2')}{t('3')}tet"
        result["praet_akt_konj1_3_plur"] = f"{t('1')}{t('2')}{t('3')}ten"

    if template['template_name'] == "unregelmäßig":
        # https://de.wiktionary.org/wiki/Vorlage:Deutsch_Verb_unregelm%C3%A4%C3%9Fig

        # Präsens - Aktiv - Indikativ
        result["praes_akt_ind_1_sing"] = f"{t('2')}e"
        result["praes_akt_ind_2_sing"] = f"{t('2')}st"
        result["praes_akt_ind_3_sing"] = f"{t('2')}t"
        result["praes_akt_ind_1_plur"] = f"{t('2')}en"
        result["praes_akt_ind_2_plur"] = f"{t('2')}t"
        result["praes_akt_ind_3_plur"] = f"{t('2')}en"

        # Präsens - Aktiv - Konjunktiv I
        result["praes_akt_konj1_1_sing"] = f"{t('2')}e"
        result["praes_akt_konj1_2_sing"] = f"{t('2')}est"
        result["praes_akt_konj1_3_sing"] = f"{t('2')}e"
        result["praes_akt_konj1_1_plur"] = f"{t('2')}en"
        result["praes_akt_konj1_2_plur"] = f"{t('2')}et"
        result["praes_akt_konj1_3_plur"] = f"{t('2')}en"

        # Präteritum - Aktiv - Indikativ
        result["praet_akt_ind_1_sing"] = f"{t('3')}"
        result["praet_akt_ind_2_sing"] = f"{t('3')}st"
        result["praet_akt_ind_3_sing"] = f"{t('3')}"
        result["praet_akt_ind_1_plur"] = f"{t('3')}en"
        result["praet_akt_ind_2_plur"] = f"{t('3')}t"
        result["praet_akt_ind_3_plur"] = f"{t('3')}en"

        # Präteritum - Aktiv - Konjunktiv II
        result["praet_akt_konj2_1_sing"] = f"{t('4')}e"
        result["praet_akt_konj2_2_sing"] = f"{t('4')}est"
        result["praet_akt_konj2_3_sing"] = f"{t('4')}e"
        result["praet_akt_konj2_1_plur"] = f"{t('4')}en"
        result["praet_akt_konj2_2_plur"] = f"{t('4')}et"
        result["praet_akt_konj2_3_plur"] = f"{t('4')}en"

    print(verb_title + " args: " + template["template_name"] + " t: " + str(template) + " result: " + str(result))

    verbs_table.insert(
        result
    )

    page_tag.clear()

db.close()