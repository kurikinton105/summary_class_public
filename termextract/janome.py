"""
termextract.janome.py
"""

import termextract.mecab
import termextract.core

IGNORE_WORDS = termextract.mecab.IGNORE_WORDS
SETSUBI = termextract.mecab.SETSUBI


def cmp_noun_list(data):
    """
    janomeの形態素解析結果を受け取り、複合語（空白区切りの単名詞）のリストを返す
    """
    tagged_text = _janome2macab_style(data)
    return termextract.mecab.cmp_noun_list(tagged_text)


def cmp_noun_dict(data):
    """
    複合語（単名詞の空白区切り）をキーに、その出現回数を値にしたディクショナリを返す
    """
    cmp_noun = cmp_noun_list(data)
    return termextract.core.list2dict(cmp_noun)


def _janome2macab_style(tokenize_text):
    tagged_text = ""
    for token in tokenize_text:
        surface = token.surface.replace("\t", " ")
        tagged_text += surface
        tagged_text += "\t"
        tagged_text += token.part_of_speech
        tagged_text += "\n"
    return tagged_text
