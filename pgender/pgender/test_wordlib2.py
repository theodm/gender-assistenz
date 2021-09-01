import pytest
import spacy

from pgender._spacy import spacify
from pgender.wordlib2 import find_det


def test_find_det_simple():
    doc = spacify("Der Rentner geht ein Eis essen.")

    dets = find_det(doc[1])

    assert dets == [doc[0]]


def test_find_det_with_adj():
    doc = spacify("Der fleißige Rentner geht ein Eis essen.")

    dets = find_det(doc[2])

    assert dets == [doc[0]]


def test_find_det_unbestimmt():
    doc = spacify("Ein fleißiger Rentner geht ein Eis essen.")

    dets = find_det(doc[2])

    assert dets == [doc[0]]


