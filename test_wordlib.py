import pytest
import spacy

from wordlib import follow_child_dep, follow_child_dep_single_or_none, follow_parent_dep


@pytest.fixture
def doc():
    return spacy.load("de_dep_news_trf")("Die kleine Jennifer, deren Vater Elektriker ist, schaut die Sendung mit der Maus.")


def test_follow_child_dep(doc):
    result = follow_child_dep(doc[2], ["nk", "rc"])

    # ["Die", "kleine", "ist"]
    assert result == [doc[0], doc[1], doc[7]]


def test_follow_child_dep_single_dep(doc):
    result = follow_child_dep(doc[2], "nk")

    # ["Die", "kleine"]
    assert result == [doc[0], doc[1]]

def test_follow_child_dep_single_or_none_multiple_results(doc):
    # Hier gibt es zwei Ergebnisse, daher eine Exception
    with pytest.raises(Exception):
        follow_child_dep_single_or_none(doc[2], "nk")


def test_follow_child_dep_single_or_none_single_result(doc):
    result = follow_child_dep_single_or_none(doc[2], "rc")

    assert result == doc[7]

def test_follow_child_dep_single_or_none_none_result(doc):
    result = follow_child_dep_single_or_none(doc[2], "pc")

    assert result is None

def test_follow_parent_or_multiple(doc):
    result = follow_parent_dep(doc[0], ["nk", "sb"])

    assert result == doc[2]

def test_follow_parent(doc):
    result = follow_parent_dep(doc[0], "nk")

    assert result == doc[2]


def test_follow_parent_none_result(doc):
    result = follow_parent_dep(doc[0], "sb")

    assert result is None
