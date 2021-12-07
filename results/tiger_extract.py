import json
import re
import dataset
from lxml import etree as ET

#
# Der TIGER-Korpus liegt in einem eigenen XML-Format vor (vgl.: https://www.ims.uni-stuttgart.de/forschung/ressourcen/korpora/tiger/). Dieses Skript
# konvertiert dieses Format in ein einfaches Text-Format. Dabei wird jedes maskuline Pronomen im Singular oder Nomen im Singular oder Plural
# bereits markiert. Diese Markierung muss von einem*einer Benutzer*in ergänzt werden um die Angabe, ob das Vorkommen gegendert werden muss, oder nicht.
#
# Auf diesem markierten Text wird die Evaluation ausgeführt.
#
# Folgende Anpassungen müssen gemacht werden:
# 1. Einzelne Zeitungsartikel müssen mit "---" getrennt werden.
# 2. Wörter mit -- müssen um das Zeichen \ oder ! ergänzt werden. (\ = nicht korrekturbedürftig, ! = korrekturbedürftig)
# 3. Das Ende muss mit !"§$% gekennzeichnet werden.
#
# Dann kann der Text mittels des Skripts read_corpora.py ausgewertet werden.
#
# TIGER-Korpus muss unter corpora/tiger_release_aug07.corrected.16012013.xml liegen.
#
continue_print = False

def print_cnt(str):
    if continue_print:
        print(str)

all_sentences = []

f = open("output.txt", "a", encoding="utf-8")

for event, s_tag in ET.iterparse("corpora/tiger_release_aug07.corrected.16012013.xml", events=("end",), tag=f"s"):
    graph_tag = s_tag.find(f"graph")
    terminals_tag = graph_tag.find(f"terminals")
    t_tags = terminals_tag.findall(f"t")

    sentence = []
    for t_tag in t_tags:
        word = {}

        word["word"] = t_tag.attrib["word"]
        word["pos"] = t_tag.attrib["pos"]
        word["number"] = t_tag.attrib["number"]
        word["gender"] = t_tag.attrib["gender"]
        word["case"] = t_tag.attrib["case"]

        if (word["gender"] in ["Masc", "*"] or (word["gender"] in ["Neut"] and word["number"] == "Plur")) and word["pos"] in ["PDS", "PIS", "PPER", "PPOSS", "PRELS", "PWS", "NN"]:
            word["word"] = "--" + word["word"] + "--"

        sentence.append(word)

    f.write(" ".join(x["word"] for x in sentence).replace(" ,", ",").replace(" ;", ";").replace(" .", ".").replace(" :", ":").replace(" ?", "?").replace(" .", ".").replace(" !", "!").replace("`` ", "\"").replace(" `` ", "\"").replace(" ``", "\"").replace("'' ", "\"").replace(" '' ", "\"").replace(" ''", "\"").replace("( ", "(").replace(" )", ")") + "\n")

