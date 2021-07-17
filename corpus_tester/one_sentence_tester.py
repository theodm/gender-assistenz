import stanza

from stanza_test import make_tree

nlp = stanza.Pipeline(lang='de', processors='tokenize,mwt,pos,lemma,depparse')

sentence = "Ziel ist es , dass sich T-DSL-Kunden auf dem Wege von Netz-Zusammenschaltungen einen Internet-Provider frei aussuchen dürfen ."

with open('test.txt', 'r', encoding="utf-8") as file:
    sentence = file.read()

doc = nlp(sentence)

print(*[
    f'id:{word.id}\tword: {word.text}\tdeprel: {word.deprel}\thead: {word.head}\t lemma: {word.lemma}\t upos: {word.upos}\txpos: {word.xpos}\tfeats: {word.feats if word.feats else "_"}\t'
    for sent in doc.sentences for word in sent.words], sep='\n')

for sent in doc.sentences:
    tree = make_tree(sent)

    print(" ".join([x.text for x in sent.words]))

    inorder = tree.in_order_list()
    for n in inorder:
        if n.word.xpos in ["NN", "NNP"]:
            if not n.weibliche_formen():
                continue

            needs_to_be_gendered = n.needs_to_be_gendered()

            print("")
            print("FOUND: " + n.word.text + f" (Guess: {needs_to_be_gendered})")
