import sys
import traceback

from conllu import parse_incr
from loguru import logger

from pipeline.full_pipeline import full_pipeline

logger.remove()
logger.add(sys.stderr, level="INFO")

data_file = open("corpora/tiger_release_aug07.corrected.16012013.conll09", "r", encoding="utf-8")

f = open("demofile2.txt", "a")

i = 0
for tokenlist in parse_incr(data_file):
    sentence = [x["form"] for x in tokenlist]
    sentence = " ".join(sentence)

    sentence = sentence.replace(" ,", ",").replace(" ;", ";").replace(" .", ".").replace(" :", ":").replace(" ?", "?").repalce(" .", ".").replace(" !", "!")

    f.write(sentence)




