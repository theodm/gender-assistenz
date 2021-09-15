import sys
import traceback

from conllu import parse_incr
from loguru import logger

from pipeline.full_pipeline import full_pipeline

logger.remove()
logger.add(sys.stderr, level="INFO")

data_file = open("corpora/de_hdt-ud-train.conllu", "r", encoding="utf-8")

i = 0
for tokenlist in parse_incr(data_file):
    sentence = [x["form"] for x in tokenlist]
    sentence = " ".join(sentence)

    res = full_pipeline(sentence)

    for r in res:
        if r["errors"]:
            logger.info(f"{i}: {sentence}")
            logger.info(r["errors"])

    i = i + 1


