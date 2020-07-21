debug = False #デバッグ時はTrue
from MCE.bag_of_words import make_summary
from MCE.CreateAdditionalExplanation import CreateAdditionalExplanation
import time

#テキストからMakeClassEasy化したテキスト及び処理時間のタプルを返します
#引数:text = 入力テキスト,compression = 要約時圧縮率,number_of_sentence=要約時分数,c = 重要単語抽出個数
def MakeClassEasy(text,compression,number_of_sentence,c=-1):
    start = time.time()
    summary = make_summary(text,compression,number_of_sentence)#入力テキストの要約
    explain = CreateAdditionalExplanation(summary,c)#要約から重要語の抽出,重要語から補足説明の生成
    if(debug): print(summary)
    output = summary + "\n\n以下重要語補足説明(自動生成)\n"
    for e in explain:
        try:
            e[1] = make_summary(e[1],50,50)#重要語に対応する補足説明の要約
        except:
            e[1] = "補足説明を生成できませんでした."
        output = output + e[0] + "\n" + e[1] + "\n\n"#つなげる
    if(debug):print(explain)
    return (summary,explain,time.time()-start)