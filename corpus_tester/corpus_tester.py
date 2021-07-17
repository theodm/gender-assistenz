import stanza
from conllu import parse_incr
import click

from stanza_test import make_tree

nlp = stanza.Pipeline(lang='de', processors='tokenize,mwt,pos,lemma,depparse')

data_file = open("de_hdt-ud-train.conllu", "r", encoding="utf-8")

i = 0
for tokenlist in parse_incr(data_file):
    sentence = [x["form"] for x in tokenlist]
    sentence = " ".join(sentence)

    print(f"{i}: " + sentence)
    i = i + 1

    if i < 1224:
        continue

    doc = nlp(sentence)

    tree = make_tree(doc.sentences[0])

    inorder = tree.in_order_list()
    for n in inorder:
        if n.word.xpos in ["NN", "NNP"]:
            if not n.weibliche_formen():
                continue

            needs_to_be_gendered = n.needs_to_be_gendered()

            print("")
            print("FOUND: " + n.word.text + f" (Guess: {needs_to_be_gendered})")

            current_word_index = n.word.id - 1

            while current_word_index >= len(tokenlist) or tokenlist[current_word_index]["xpos"] != "NN":
                current_word_index = current_word_index - 1

            if click.confirm('Do you want to continue?', default=True):
                tokenlist[current_word_index]["feats"]["SBG"] = "yes"
            else:
                tokenlist[current_word_index]["feats"]["SBG"] = "no"

    with open("modified.conllu", "a", encoding="utf-8") as output_file:
        output_file.write(tokenlist.serialize())
