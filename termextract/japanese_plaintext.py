"""
termextract.japanese_paintext.py
"""

import re

import termextract.core

IGNORE_WORDS = set([])  # 重要度計算外とする語

# ひらがな
JP_HIRA = set([chr(i) for i in range(12353, 12436)])
# カタカナ
JP_KATA = set([chr(i) for i in range(12449, 12532+1)])
JP_KATA.add("ー")
MULTIBYTE_MARK = set([
    "", "、", "。", "”", "“", "，", "《", "》", "：", "（", "）", "；",
    "〈", "〉", "「", "」", "『", "』", "【", "】", "〔", "〕", "？", "！",
    "-", "…", "‘", "’", "／",
    "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "０", "１", "２", "３",
    "４", "５", "６", "７", "８", "９",
    " ",
    ])


def cmp_noun_list(data):
    """
    和文テキストを受け取り、複合語（空白区切りの単名詞）のリストを返す
    """
    cmp_nouns = []
    terms = []
    # 行レベルのループ
    for morph in data.split("\n"):
        morph.rstrip()
        if not morph:
            continue
        morph = morph.replace(",", " ")
        morph = morph.replace(".", " ")
        morph = morph.replace("(", " ")
        morph = morph.replace(")", " ")
        morph = morph.replace(";", " ")
        morph = morph.replace("!", " ")
        morph = morph.replace("[", " ")
        morph = morph.replace("]", " ")
        morph = morph.replace("?", " ")
        morph = morph.replace("/", " ")
        is_stopword = 0
        is_kata = 0
        kata = ""
        # 文字レベルのループ
        while morph:
            is_stopword = 0
            # 英語
            eng_word = re.match(r"[a-zA-Z0-9_]+", morph)
            if eng_word is not None:
                if is_kata:
                    if len(kata) > 1:
                        terms.append(kata)
                    kata = ""
                    is_kata = 0
                morph = morph[len(eng_word.group(0)):]
                terms.append(eng_word.group(0))
            if not morph:
                continue
            # マルチバイト記号
            if morph[0] in MULTIBYTE_MARK:
                if is_kata:
                    if len(kata) > 1:
                        terms.append(kata)
                    kata = ""
                    is_kata = 0
                _increase(cmp_nouns, terms)
                is_stopword = 1
            # ひらがな
            if morph[0] in JP_HIRA:
                if is_kata:
                    if len(kata) > 1:
                        terms.append(kata)
                    kata = ""
                    is_kata = 0
                _increase(cmp_nouns, terms)
                is_stopword = 1
            # カタカナ
            if morph[0] in JP_KATA:
                kata += morph[0]
                is_kata = 1
            if not is_stopword:
                if not is_kata:
                    terms.append(morph[0])
            morph = morph[1:]
        if not is_stopword:
            terms.append(kata)
            _increase(cmp_nouns, terms)
    # 行の末尾の処理
    _increase(cmp_nouns, terms)
    cmp_nouns_cut_uni = [x for x in cmp_nouns if len(x) > 1]
    return cmp_nouns_cut_uni


def _increase(cmp_nouns, terms):
    """
    専門用語リストへ、整形して追加するサブルーチン
    """
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
