"""
termextract.mecab.py
"""

import re

import termextract.core

IGNORE_WORDS = set(["的"])  # 重要度計算外とする語
SETSUBI = set(["など", "ら", "上", "内", "型", "間", "中", "毎"])


def cmp_noun_list(data):
    """
    和布蕪の形態素解析結果を受け取り、複合語（空白区切りの単名詞）のリストを返す
    """
    cmp_nouns = []
    must = 0  # 次の語が名詞でなければならない場合は真
    terms = []  # 複合語リスト作成用の作業用配列
    # 単名詞の連結処理
    for morph in data.split("\n"):
        morph.rstrip()
        if morph == "EOS" or morph == "":
            if not must:
                _increase(cmp_nouns, terms)
            must = 0
            continue
        noun_value = morph.split("\t")
        if len(noun_value) < 2:
            continue
        noun, values = noun_value[0:2]
        value = values.split(",")
        part_of_speach, cl_1, cl_2 = value[0:3]
        if (part_of_speach == "名詞" and cl_1 == "一般" or
                part_of_speach == "名詞" and cl_1 == "接尾" and cl_2 == "一般" or
                part_of_speach == "名詞" and cl_1 == "接尾" and cl_2 == "サ変接続" or
                part_of_speach == "名詞" and cl_1 == "固有名詞" or
                part_of_speach == "記号" and cl_1 == "アルファベット" or
                part_of_speach == "名詞" and cl_1 == "サ変接続" and not
                re.match(r"[!\"#$%&'\(\)*+,-./{\|}:;<>\[\]\?!]$", noun)):
            terms.append(noun)
            must = 0
        elif (part_of_speach == "名詞" and cl_1 == "形容動詞語幹" or
              part_of_speach == "名詞" and cl_1 == "ナイ形容詞語幹"):
            terms.append(noun)
            must = 1
        elif part_of_speach == "名詞" and cl_1 == "接尾" and cl_2 == "形容動詞語幹":
            terms.append(noun)
            must = 1
        elif part_of_speach == "動詞":
            del terms[:]
        else:
            if not must:
                _increase(cmp_nouns, terms)
            must = 0
            del terms[:]
    if not must:
        _increase(cmp_nouns, terms)
    return cmp_nouns


def _increase(cmp_nouns, terms):
    """
    専門用語リストへ、整形して追加するサブルーチン
    """
    # 語頭の不要な語の削除
    if len(terms) > 1:
        if terms[0] == "本":
            del terms[0]
    if terms:
        # 語尾の余分な語の削除
        end = terms[-1]
        if end in SETSUBI or re.match(r"\s+$", end):
            del terms[-1]
    if terms:
        cmp_noun = ' '.join(terms)
        cmp_nouns.append(cmp_noun)
    del terms[:]


def cmp_noun_dict(data):
    """
    複合語（単名詞の空白区切り）をキーに、その出現回数を値にしたディクショナリを返す
    """
    cmp_noun = cmp_noun_list(data)
    return termextract.core.list2dict(cmp_noun)
