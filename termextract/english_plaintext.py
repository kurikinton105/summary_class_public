"""
termextract.english_paintext.py
"""

import re

import termextract.core

IGNORE_WORDS = set(["of", "Of", "OF"])  # of は重要度計算外とする

# ストップワード(小文字)を設定
STOPWORDS_LC = [
    "a", "about", "above", "across", "after",
    "again", "against", "all", "almost", "alone",
    "along", "already", "also", "although", "always",
    "amoung", "an", "and", "another", "any",
    "anybody", "anyone", "anything", "anywhere", "are",
    "area", "areas", "around", "as", "ask",
    "asked", "asking", "asks", "at", "away",
    "b", "back", "backed", "backing", "backs",
    "be", "because", "became", "become", "becomes",
    "been", "before", "began", "behind", "being",
    "begins", "best", "better", "between", "big",
    "both", "but", "by", "c", "came",
    "can", "cannot", "case", "cases", "certain",
    "certainly", "clear", "clearly", "come", "could",
    "d", "did", "differ", "different", "differently",
    "do", "dose", "done", "down", "downed",
    "downing", "downs", "during", "e", "each",
    "early", "either", "end", "ended", "ending",
    "every", "everydody", "everyone", "everything", "everywhere",
    "f", "face", "faces", "fact", "facts",
    "far", "felt", "few", "find", "finds",
    "first", "for", "four", "from", "full",
    "fully", "further", "furthered", "furthering", "furthers",
    "g", "gave", "general", "generally", "get",
    "gets", "give", "given", "gives", "go",
    "going", "good", "goods", "got", "great",
    "greater", "greatest", "group", "grouped", "grouping",
    "groups", "h", "had", "has", "have",
    "having", "he", "her", "herself", "here",
    "high", "higher", "highest", "him", "himself",
    "his", "how", "however", "i", "if",
    "important", "in", "interest", "interested", "interesting",
    "interests", "into", "is", "it", "its",
    "itself", "j", "just", "k", "keep",
    "keeps", "kind", "knew", "know", "known",
    "knows", "l", "large", "largely", "last",
    "lather", "lastest", "least", "less", "let",
    "lets", "like", "likely", "long", "longer",
    "longest", "m", "made", "make", "making",
    "man", "many", "may", "me", "member",
    "members", "mem", "might", "more", "most",
    "mostly", "mr", "mrs", "much", "must",
    "my", "myself", "n", "necessary", "need",
    "needed", "needing", "needs", "never", "new",
    "newer", "newest", "next", "no", "non",
    "not", "nodody", "noone", "nothing", "now",
    "nowther", "number", "numbered", "numbering", "numbers",
    "o", "off", "often", "old",
    "older", "oldest", "on", "once", "one",
    "only", "open", "opened", "opening", "opens",
    "or", "order", "ordered", "ordering", "orders",
    "other", "others", "our", "out", "over",
    "p", "part", "parted", "parting", "parts",
    "per", "perhaps", "place", "places", "point",
    "pointed", "pointing", "points", "possible", "present",
    "presented", "presenting", "presents", "problem", "problems",
    "put", "puts", "q", "quite", "r",
    "rather", "really", "right", "room", "rooms",
    "s", "said", "same", "saw", "say",
    "says", "second", "seconds", "see", "seem",
    "seemed", "seeming", "seems", "sees", "several",
    "shall", "she", "should", "show", "showed",
    "showing", "shows", "side", "sides", "since",
    "small", "smaller", "smallest", "so", "some",
    "somebody", "someone", "something", "somewhere", "state",
    "states", "still", "such", "sure", "t",
    "take", "taken", "than", "that", "the",
    "their", "them", "then", "there", "therefore",
    "these", "they", "thing", "things", "think",
    "thoughts", "three", "those", "through", "thought",
    "today", "together", "too", "took", "toward",
    "turn", "turned", "turning", "turns", "two",
    "u", "under", "untill", "up", "upon",
    "us", "use", "uses", "used", "v",
    "very", "w", "want", "wanted", "wanting",
    "well", "wells", "went", "were", "what",
    "when", "where", "whether", "which", "while",
    "who", "whole", "whose", "why", "will",
    "with", "within", "without", "work", "worked",
    "working", "works", "would", "x", "y",
    "year", "years", "yet", "you", "young",
    "younger", "youngest", "your", "yours", "z",
    "to", "this", "it's", "that's", "what's",
    "who's", "I'm", "am", "was", "largest",
    "we", "can't", "couldn't", "wouldn't", "you're",
    "you'd", "you've", "you'll", "wasn't", "isn't",
    "aren't", "don't", "didn't", "dosen't", "he's",
    "he'll", "she's", "she'll", "we're", "weren't",
    "I'll", "I'd", "we'll", "I've", "it'll",
    "who's", "where's", "haven't", "hasn't", "hadn't",
    "won't", "there's", "whoever", "whichever", "whatever",
    ]

# ストップワードリストをセット化
STOPWORDS_SET = set()
for term in STOPWORDS_LC:
    STOPWORDS_SET.add(term)
    STOPWORDS_SET.add(term.upper())
    if len(term) > 1:
        STOPWORDS_SET.add(term.capitalize())


def cmp_noun_list(data):
    """
    英文テキストを受け取り、複合語（空白区切りの単名詞）のリストを返す
    """
    cmp_nouns = []
    # 行レベルのループ
    for morph in data.split("\n"):
        morph.rstrip()
        if not morph:
            continue
        terms = []
        # 単語レベルのループ
        for word in morph.split():
            # ノイズ削除
            word = re.sub(r"\(", "", word)
            word = re.sub(r"\)", "", word)
            word = re.sub(r"\[", "", word)
            word = re.sub(r"\]", "", word)
            word = re.sub(r"{", "", word)
            word = re.sub(r"}", "", word)
            word = re.sub(r"<", "", word)
            word = re.sub(r">", "", word)
            word = re.sub("\"", "", word)
            if re.match(r"\s*$", word):
                continue
            # 文の末尾を判定
            if (re.search(r"[\.,\?!:;]+$", word) and not
                    re.search(r"^[A-Z].$", word)):
                word = re.sub(r"[\.,\?!:;']+$", "", word)
                if (word not in STOPWORDS_SET and not
                        re.search(r"[\-\=#/\|&\*\+]+", word)):
                    terms.append(word)
                _increase(cmp_nouns, terms)
            elif (word in STOPWORDS_SET or
                  re.search(r"[\-\.=#/\|&\*\+]+", word)):
                _increase(cmp_nouns, terms)
            else:
                terms.append(word)
        # 行の末尾の処理
        _increase(cmp_nouns, terms)
    return cmp_nouns


def _increase(cmp_nouns, terms):
    """
    専門用語リストへ、整形して追加するサブルーチン
    """
    if terms:
        if re.match("of$", terms[0], re.IGNORECASE):
            del terms[0]
    if terms:
        if re.match("of$", terms[-1], re.IGNORECASE):
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
