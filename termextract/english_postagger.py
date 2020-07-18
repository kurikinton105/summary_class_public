"""
termextract.engish_postagger.py
"""

import re

import termextract.core

IGNORE_WORDS = set(["of", "Of", "OF"])  # of は重要度計算外とする


def cmp_noun_list(data):
    """
    nltkのpos_tagの結果を受け取り、複合語（空白区切りの単名詞）のリストを返す
    """
    cmp_nouns = []
    status = 0
    # status = 1   前が名詞(NN, NNS, NNP)
    #          2   前が形容詞(JJ)
    #          3   前が所有格語尾(POS)
    #          4   前がof
    #          5   前が基数(CD)
    #          6   前が過去分詞の動詞(VBN)
    #          7   前が外来語(FW)
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
        if re.search("NN[PS]?$", tag) or tag == "NNPS":
            # 複数形を単数形に置き換える。
            if tag == "NNS":
                term = stemming(term)
            # 固有名詞以外は先頭の大文字を小文字に。
            if re.search("NNS?$", tag) and re.match("[A-Z][a-z]", term):
                term = term.title()
            status = 1
            seg.append(term)
            rest = 0
        # 形容詞(JJ)の場合
        elif tag == "JJ":
            # 前の語が"なし","形容詞","所有格語尾","基数"の場合は連結する
            if status == 0 or status == 2 or status == 3 or status == 5:
                seg.append(term)
                rest += 1
            else:
                _increase(cmp_nouns, seg, rest)
                seg = [term]
                rest += 1
            status = 2
        # 所有格語尾(POS)の場合
        elif tag == "POS":
            # 前の語が名詞の場合は連結する
            if status == 1:
                status = 3
                seg.append(term)
                rest += 1
            else:
                _increase(cmp_nouns, seg, rest)
                seg = []
        # of の場合
        elif term == "of" and tag == "IN":
            # 前の語が名詞の場合は連結する
            if status == 1:
                status = 4
                seg.append(term)
                rest += 1
            else:
                _increase(cmp_nouns, seg, rest)
                seg = []
                status = 0
        # 基数(CD)の場合は、語の先頭のみ許可
        elif tag == "CD":
            _increase(cmp_nouns, seg, rest)
            seg = [term]
            status = 5
        # 過去分詞の動詞は語の先頭のみ許可
        elif tag == "VBN":
            _increase(cmp_nouns, seg, rest)
            seg = [term]
            status = 6
            rest += 1
        # 外来語(FW)の場合は単語として処理
        elif tag == "FW":
            _increase(cmp_nouns, seg, rest)
            status = 7
            seg = [term]
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


def stemming(noun):
    """"
    複数形を単数形に変えるだけのstemmer
    """
    if noun.endswith("ies") and not re.search("[ae]ies$", noun):
        noun = re.sub("ies$", "y", noun)
    elif noun.endswith("es") and not re.search("[aeo]es$", noun):
        noun = re.sub("es$", "e", noun)
    elif noun.endswith("s") and not re.search("[us]s", noun):
        noun = re.sub("s$", "", noun)
    return noun


def _increase(cmp_nouns, seg, rest):
    allwords = ""
    # 複合語の末尾は名詞とし、それ以外は切り捨てる
    pos = len(seg) - rest
    if pos > 0:
        seg = seg[0:pos]
    rest = 0
    if seg:
        for word in seg:
            word = re.sub(r"^\s+", "", word)
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
