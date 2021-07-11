from conllu import parse_incr

data_file = open("de_hdt-ud-train.conllu", "r", encoding="utf-8")

for tokenlist in parse_incr(data_file):

    print(tokenlist)