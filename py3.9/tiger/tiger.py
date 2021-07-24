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

for event, s_tag in ET.iterparse("tiger_release_aug07.corrected.16012013.xml", events=("end",), tag=f"s"):
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

        sentence.append(word)

    all_sentences.append(sentence)

    f.write(" ".join(x["word"] for x in sentence) + "\n")

    #print([x["word"] for x in sentence])



#
# for sentence in all_sentences:
#     for i, w in enumerate(sentence):
#         indexOfLast = i - 1
#
#         if indexOfLast < 0:
#             continue
#
#
#
#         if w["pos"] == "NN" and w["case"] == "Nom" and w["number"] == "Pl":
#             print([x["word"] for x in sentence])

