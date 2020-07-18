"""
termextract.nlir.py
"""

import re

import termextract.core

# 重要度計算外とする語
IGNORE_WORDS = set(["和", "与", "的", "之", "等", "型", "式", "性"])


def cmp_noun_list(data):
    """
    nlpirの結果を受け取り、複合語（空白区切りの単名詞）のリストを返す
    """
    cmp_nouns = []
    status = 0
    # status = 1   前が名詞(noun)
    #          2   前が形容詞(adjective)
    #          3   前が助詞(particle), 后接成分(suffix')
    #          4   前が連詞[和、与](c)
    #          5   前が区別詞(distinguishing word)
    rest = 0  # 名詞以外の語が何語連続したかカウント
    seg = []  # 複合語のリスト
    for morph in data:
        term, tag = morph[0:2]
        # 数値や区切り記号の場合
        if re.match(r"[\s\+\-%&$*#^\|\[\]]$", term) or re.match(r"\d+$", term):
            _increase(cmp_nouns, seg, rest)
            seg = []
            continue
        # 名詞の場合
        if tag == "noun":
            status = 1
            seg.append(term)
            rest = 0
        # 形容詞の場合
        elif tag == "adjective":
            # 前の語が"なし","形容詞","助詞＋后接成分","連詞"の場合は連結する
            if status == 0 or status == 2 or status == 3 or status == 4:
                seg.append(term)
                rest += 1
            else:
                _increase(cmp_nouns, seg, rest)
                seg = [term]
                rest += 1
            status = 2
        # 助詞及び後接詞の場合
        elif tag == "particle" or tag == "suffix":
            # 前の語が"名詞","形容詞"の場合は連結する
            if status == 0 or status == 2:
                seg.append(term)
                rest += 1
            else:
                _increase(cmp_nouns, seg, rest)
                seg = []
                rest = 0
            status = 3
        # 連詞（和、与）の場合
        elif tag == "conjunction" and (term == "和" or term == "与"):
            # 前の語が"名詞"の場合は連結する
            if status == 0:
                seg.append(term)
                rest += 1
            else:
                _increase(cmp_nouns, seg, rest)
                seg = []
                rest = 0
            status = 4
        # 区別詞の場合
        elif tag == "distinguishing word":
            # 　前の語が"なし","名詞", "助詞＋后接成分", "連詞"の場合は連結する
            if status == 0 or status == 1 or status == 3 or status == 4:
                seg.append(term)
                rest += 1
            else:
                _increase(cmp_nouns, seg, rest)
                seg = []
                rest = 0
            status = 5
        # 指定した品詞以外の場合は、そこで複合語の区切りとする
        else:
            _increase(cmp_nouns, seg, rest)
            seg = []
            status = 0
    # 改行があった場合はそこで複合語の区切りとする
    _increase(cmp_nouns, seg, rest)
    seg = []
    status = 0
    return cmp_nouns


def _increase(cmp_nouns, seg, rest):
    allwords = ""
    # 複合語の末尾は名詞とし、それ以外は切り捨てる
    pos = len(seg) - rest
    if pos > 0:
        seg = seg[0:pos]
    rest = 0
    if seg:
        for word in seg:
            word = re.sub(r"^\s+", "", word)        # 邪魔なスペースを取り除く
            word = re.sub(r"\s+$", "", word)
            if allwords == "":
                allwords = word
            else:
                allwords += ' ' + word
        # ' で区切られた語は接続する
        allwords.replace(" ' ", "'")
        # 末尾の . と , は削除する
        allwords = re.sub(",$", "", allwords)
        allwords = re.sub(r"\.$", "", allwords)
        cmp_nouns.append(allwords)


def cmp_noun_dict(data):
    """
    複合語（単名詞の空白区切り）をキーに、その出現回数を値にしたディクショナリを返す
    """
    cmp_noun = cmp_noun_list(data)
    return termextract.core.list2dict(cmp_noun)
