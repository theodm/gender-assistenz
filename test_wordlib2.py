import pytest
import spacy

from _spacy import spacify
from wordlib2 import find_adj, find_verb, find_art_and_pron


def test_find_det_simple():
    doc = spacify("Der Rentner geht ein Eis essen.")

    dets = find_art_and_pron(doc[1])

    assert dets == [doc[0]]


def test_find_det_with_adj():
    doc = spacify("Der fleißige Rentner geht ein Eis essen.")

    dets = find_art_and_pron(doc[2])

    assert dets == [doc[0]]


def test_find_adj():
    doc = spacify("Der fleißige Rentner geht ein Eis essen.")

    dets = find_adj(doc[2])

    assert dets == [doc[1]]


def test_find_det_unbestimmt():
    doc = spacify("Ein fleißiger Rentner geht ein Eis essen.")

    dets = find_art_and_pron(doc[2])

    assert dets == [doc[0]]


def test_find_verb():
    doc = spacify("Ein fleißiger Rentner geht ein Eis essen.")

    verb = find_verb(doc[2])

    assert verb == [doc[3]]


def test_find_verb_aux():
    doc = spacify("Ein fleißiger Rentner soll ein Eis essen gehen.")

    verb = find_verb(doc[2])

    assert verb == [doc[3]]

def test_find_verb_oc():
    doc = spacify("Der Benutzer sagte, er sei vorsichtig vorgegangen.")

    pron = find_verb(doc[1])

    assert pron == [doc[2], doc[5]]


def test_find_prelat_art():
    doc = spacify("Der Benutzer, dessen Account gestohlen wurde, soll den PC neu starten.")

    pron = find_art_and_pron(doc[1])

    assert pron == [doc[0], doc[3]]

def test_find_art2():
    doc = spacify("Der Benutzer, dessen PC abgestürzt ist, soll den PC neu starten.")

    pron = find_art_and_pron(doc[1])

    assert pron == [doc[0], doc[3]]

def test_find_art3():
    doc = spacify("In einem Bereich gab es in diesem Jahr keinen Sieger.")

    pron = find_art_and_pron(doc[9])

    assert pron == [doc[8]]

def test_find_pron_er():
    doc = spacify("Der Benutzer sagte, er sei vorsichtig vorgegangen.")

    pron = find_art_and_pron(doc[1])

    assert pron == [doc[0], doc[4]]






