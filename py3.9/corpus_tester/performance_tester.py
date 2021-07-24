import stanza
from conllu import parse_incr
import click

from stanza_test import make_tree

nlp = stanza.Pipeline(lang='de', processors='tokenize,mwt,pos,lemma,depparse')

data_file = open("modified.conllu", "r", encoding="utf-8")

i = 0
for tokenlist in parse_incr(data_file):
    sentence = [x["form"] for x in tokenlist]
    sentence = " ".join(sentence)

    i = i + 1

    doc = nlp(sentence)

    tree = make_tree(doc.sentences[0])

    inorder = tree.in_order_list()
    for n in inorder:
        if n.word.xpos in ["NN", "NNP"]:
            if not n.weibliche_formen():
                continue
p
            needs_to_be_gendered = n.needs_to_be_gendered()

            # print("")
            # print("FOUND: " + n.word.text + f" (Guess: {needs_to_be_gendered})")

            current_word_index = n.word.id - 1

            while current_word_index >= len(tokenlist) or tokenlist[current_word_index]["xpos"] != "NN":
                current_word_index = current_word_index - 1

            print(f"{i}: " + sentence)

            if tokenlist[current_word_index]["feats"]["SBG"] == "yes" and needs_to_be_gendered:
                print(f"CORRECT: {n.word.text} " + tokenlist[current_word_index]["feats"]["SBG"])
            elif tokenlist[current_word_index]["feats"]["SBG"] == "no" and not needs_to_be_gendered:
                print(f"CORRECT: {n.word.text} " + tokenlist[current_word_index]["feats"]["SBG"])
            else:
                print(f"INCORRECT: {n.word.text} " + tokenlist[current_word_index]["feats"]["SBG"] + " but " + str(needs_to_be_gendered))
