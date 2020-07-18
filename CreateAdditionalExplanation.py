debug = False
import termextract.janome
import termextract.core
import collections
import requests
from bs4 import BeautifulSoup
from janome.tokenizer import Tokenizer

#上位c個の重要複合語のリストを返します.c=-1(デフォルト)ですべての複合語を返します.
def Extract_ImportantWords(text,c=-1):

    if(debug):print(text)
    
    t = Tokenizer()
    tokenize_text = t.tokenize(text)
    #頻度ベクトル生成
    frequency = termextract.janome.cmp_noun_dict(tokenize_text) #複合語抽出
    #LR(ボトムアップ構文解析)のスコアの生成
    lr = termextract.core.score_lr(
        frequency,
        ignore_words=termextract.mecab.IGNORE_WORDS,
        lr_mode=1, average_rate=1)
    #頻度lRスコアの生成(すなわち重要度)
    term_imp = termextract.core.term_importance(frequency, lr)
    #降順に表示
    imp_words = []
    data_collection = collections.Counter(term_imp)
    if(c == -1):#全表示
        for cmp_noun, value in data_collection.most_common() :
            imp_words.append(termextract.core.modify_agglutinative_lang(cmp_noun))
    else:#c個表示
        tmp = 1
        for cmp_noun, value in data_collection.most_common():
            if(tmp > c): break
            imp_words.append(termextract.core.modify_agglutinative_lang(cmp_noun))
            tmp += 1
    if(debug):print(imp_words)
    return imp_words


# User-Agent

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
            AppleWebKit/537.36 (KHTML, like Gecko) \
            Chrome/83.0.4103.116 Safari/537.36 Edg/83.0.478.64"

def get_html(url, params=None, headers=None):
    """ get_html
    url: データを取得するサイトのURL
    [params]: 検索サイトのパラメーター {x: param}
    [headers]: カスタムヘッダー情報
    """
    try:
        # データ取得
        resp = requests.get(url, params=params, headers=headers)
        resp.encoding = 'utf-8'
        # 要素の抽出
        soup = BeautifulSoup(resp.text, "html.parser")
        return soup
    except Exception as e:
        return None

def get_search_url(word):
    """ get_search_url
    word: 検索するワード
    """
    try:
        # google 検索
        search_url = "https://www.google.co.jp/search"
        search_params = {"q": word}
        search_headers = {"User-Agent": user_agent}
        # データ取得
        soup = get_html(search_url, search_params, search_headers)
        if soup != None:
            #class = r <a href>
            tags = soup.select(".r > a")
            urls = [tag.get("href") for tag in tags]
            return urls
        else:
            return None
    except Exception as e:
        return None

#soupからテキストの抽出
def extract_textFhtml(soup):
    for script in soup(["script", "style"]):#いらないタグの削除
        script.decompose()
    text=soup.get_text()#テキスト取得
    lines=[]
    for line in text.splitlines():#リスト化
        lines.append(line.strip())
    text="".join(line for line in lines if line)#空白を除去して１つにまとめる
    return text

#渡されたテキストから重要語を求め,各重要語を説明するサイトの本文を返します.
#戻り値[word,text]のリスト word:重要語,text:重要語に対応する説明サイトの本文
def CreateAdditionalExplanation(text,c=-1):
    additionals = []

    importances = Extract_ImportantWords(text,c)
    for word in importances:
        try:
            urls = get_search_url(word)
            if(urls[0] != None):
                soup = get_html(urls[0])
                text = extract_textFhtml(soup)
                additionals.append([word,text])
        except Exception as e:
            if(debug):print("エラー")
    return additionals
