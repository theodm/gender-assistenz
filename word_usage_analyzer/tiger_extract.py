import json
import re
import dataset
from lxml import etree as ET

f = open("test.txt","w+", encoding="utf-8")

continue_print = False

def print_cnt(str):
    if continue_print:
        print(str)

all_sentences = []

f = open("demofile2.txt", "a", encoding="utf-8")

# \ = wird nicht korrigiert
# ! = wird korrigiert

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

