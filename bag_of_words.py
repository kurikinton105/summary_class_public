from janome.tokenizer import Tokenizer
import numpy as np

def power_method(cosine_matrix, n, e):#PageRankを行う
    transposed_matrix = cosine_matrix.T
    sentences_count = n

    p_vector = np.array([1.0 / sentences_count] * sentences_count)

    lambda_val = 1.0

    while lambda_val > e:
        next_p = np.dot(transposed_matrix, p_vector)
        lambda_val = np.linalg.norm(np.subtract(next_p, p_vector))
        p_vector = next_p

    return p_vector

#Cos類似度を求めてあげる！！
def cosinSimilarity(vec0,vec1):
    Dot = np.dot(vec0,vec1)#内積
    Sum = np.sqrt(np.sum(vec0)) * np.sqrt(np.sum(vec1))
    vec_cos = Dot/Sum
    ##print(vec_cos)
    return vec_cos

def bag_of_words_sum(input_text,compression,number_of_sentence): #input_text：入力テキスト,compression：圧縮率,number_of_sentence：文字数制限
    #一番初めに専門用語の配列を作成
    wordlist = []
    path = "dataset.txt"
    with open(path) as f:
        for s_line in f:
            #print(s_line)
            s_line = s_line.strip("\n")
            wordlist.append(s_line)
    #input_text=("経路制御技術（ルーティング）とは、ネットワーク層が行う処理で目的のパケットの宛先のIPアドレスまでどのようにIPを経由して送られるかについて制御を行う技術である。\nインターネットにおける経路制御技術は、直接転送と間接転送がある。直接転送では、同一のネットワーク上のホストに転送を行い、ルータを経由する必要がない。一方間接転送は、異なるネットワーク上のホストへの転送を行う。\n経路選択には、事前に経路を決定する静的経路制御とルータ間でルーティングプロトコルを使用し、経路表を作成する動的経路制御の２種類がある。静的経路制御では、経路表が事前に作られているため、経路が安定する。しかし経路数が多くなった場合は設定が複雑になることやルータの障害の際に再設定が必要である。一方、動的経路制御はルータが経路を計算するため、経路計算の負荷や冗長性のある経路選択が行われるなどのデメリットがあるが、経路表を自動で作るため、障害迂回の際の経路変更が自動で行われるなどのメリットがある。今回の課題では、動的経路制御の一種であるOSPFのプロトコルについて調査を行う。\n")

    input_text=input_text.strip("\n")
    input_text=input_text.split('。')
    #print(input_text)
    input_text_copy = input_text
    #形態素分析（pip3 install janomeが必要）

    tokenslist=[]
    tokenslist_dic=[]
    #print(tokenslist)
    for i in range(len(input_text)-1):
        tokenslist1=[]
        t = Tokenizer() # 字句解析器の作成
        tokens = t.tokenize(input_text[i]) # 形態素解析tokens[]のなかに一つづつ含まれる。
        for token in tokens:
            #print(token) # 結果の表示
            tokenslist1.append(token.surface)
            tokenslist_dic.append(token.surface)
        tokenslist.append(tokenslist1)

    #print(tokens[0].surface) # 結果の表示(.surfaceを使うと文字の表示ができる)
    #print(tokenslist)

    #辞書を作る
    #print(tokenslist_dic)
    tokenslist_dic=list(set(tokenslist_dic)) #重複を消してあげる。
    #print(tokenslist_dic)
    #print(len(tokenslist_dic))
    vec = np.zeros((len(tokenslist),len(tokenslist_dic))) #配列の用意
    #print(vec.shape)

    #bags of words を作る！！
    for i in range(len(tokenslist)):
        for j in range(len(tokenslist_dic)):
            #print(tokenslist[i].count(tokenslist_dic[j]))
            vec[i][j] = tokenslist[i].count(tokenslist_dic[j])

    #print(vec)

    #print(cosinSimilarity(vec[0],vec[0]))

    graph = np.zeros((len(tokenslist),len(tokenslist)),dtype="float32")

    for i in range(len(tokenslist)):
        for j in range(len(tokenslist)):
            graph[i][j] = cosinSimilarity(vec[i],vec[j])

    #print(graph) #cos類似度の対応関係の配列ができる！！

    #隣接行列を作ってあげる
    para =0.3 #比較のパラメータ
    compare = np.full_like(graph, para) #比較用配列

    adjacency = graph >compare
    #print(adjacency)

    #確率行列を作る
    rundom_graph = np.zeros_like(graph)

    for i in range(len(tokenslist)):
        sum_one = np.sum(adjacency[i])
        for j in range(len(tokenslist)):
            rundom_graph[i][j] = adjacency[i][j]/sum_one

    #print(rundom_graph)

    ratings = power_method(rundom_graph, len(tokenslist),0.01)

    #print((ratings)) #どの文が重要かを示してくれてる！

    #文字列の出力

    compression = compression/100 #圧縮率（%)
    #number_of_sentence = len(tokenslist) # 文字数

    sort_index = np.argsort(ratings) #大きい順にソートした時のインデックス
    #print(sort_index)
    output=[]
    output_index = []
    for i in range(int(len(tokenslist)/2)):
        output_index.append(sort_index[i])

    output_index.sort
    output_index = np.array(output_index)
    output_index = np.sort(output_index)
    #print(output_index)


    for i in range(len(output_index)):
        #print(input_text_copy[output_index[i]])
        output.append(input_text_copy[output_index[i]])

    #専門用語があったら入れ替える
    output_kyaku = output

    for i in range(len(wordlist)):
      for j in range(len(output_kyaku)):
        if wordlist[i] in output_kyaku[j]:
          if wordlist[i] !="":
            output_kyaku[j] = output_kyaku[j].replace(str(wordlist[i]),"$"+str(wordlist[i])+"$")

    return output
#input_text_word=("経路制御技術（ルーティング）とは、ネットワーク層が行う処理で目的のパケットの宛先のIPアドレスまでどのようにIPを経由して送られるかについて制御を行う技術である。値インターネットにおける経路制御技術は、直接転送と間接転送がある。直接転送では、同一のネットワーク上のホストに転送を行い、ルータを経由する必要がない。一方間接転送は、異なるネットワーク上のホストへの転送を行う。\n経路選択には、事前に経路を決定する静的経路制御とルータ間でルーティングプロトコルを使用し、経路表を作成する動的経路制御の２種類がある。静的経路制御では、経路表が事前に作られているため、経路が安定する。しかし経路数が多くなった場合は設定が複雑になることやルータの障害の際に再設定が必要である。一方、動的経路制御はルータが経路を計算するため、経路計算の負荷や冗長性のある経路選択が行われるなどのデメリットがあるが、経路表を自動で作るため、障害迂回の際の経路変更が自動で行われるなどのメリットがある。今回の課題では、動的経路制御の一種であるOSPFのプロトコルについて調査を行う。\n")

#print(bag_of_words_sum(input_text_word,50,100))