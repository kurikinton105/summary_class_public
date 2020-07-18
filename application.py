from flask import Flask, render_template,request #追加
from bag_of_words import bag_of_words_sum
app = Flask(__name__)

@app.route("/cos5year", methods=["GET", "POST"])
def odd_even():
    if request.method == "GET":
        return """
        <H1>我々はCos5year(こすごいやー)だ！！！！<H1>
        <H1>おそらく地球を侵略しにきた！！！！<H1>
        <H1>なんかいい感じの開発して世界を征服するぞ！！！！！<H1>
        （ごめんなさい...ふざけました...）
        """

@app.route("/", methods=["GET", "POST"])
def main_page():
    #return render_template("make-class-easy.html")

    if request.method == 'GET':
        print("GET")
        #text = request.args.get("input_text")
        text = "ここに結果が出力されます"
        return render_template("make-class-easy.html",text=text)
    elif request.method == 'POST':
        print("POST")
        text = request.form["input_text"]
        #print(text)
        #return render_template("make-class-easy.html",text=text)

        try:
            result = bag_of_words_sum(str(text),50,100)
            #print(result)
            return render_template("make-class-easy.html",text=result)
        except:
            return render_template("make-class-easy.html",text="Error:文章は２文以上にしてください。もう一度文章を入力してください")


@app.route("/class", methods=["GET", "POST"])
def web():
    if request.method == "GET":
        #WEBリンクを代入
        return """
        <H1>bag-of-wordsを使った要約アプリ</H1>
        2文以上の文章を入力してください
        <form action="/" method="POST">
        <input name="text"></input>
        </form>"""
    else:
        try:
            result = bag_of_words_sum(str(request.form["text"]),50,100)
            return """
            <H1>bag-of-wordsを使った要約アプリ</H1>
            2文以上の文章を入力してください
            <form action="/" method="POST">
            <input name="text"></input>
            </form>
            {}<br>""".format(result)
        except:
            return """
                <H1>bag-of-wordsを使った要約アプリ</H1>
                文章は２文以上にしてください。もう一度文章を入力してください
                <form action="/" method="POST">
                <input name="text"></input>
                </form>"""

@app.route("/web", methods=["GET", "POST"])
def web2():
    if request.method == "GET":
        #WEBリンクを代入
        return """
        <H1>参考文献を自動生成してくれるチートツールを作りたかった</H1>
        URLを入力してください
        <form action="/" method="POST">
        <input name="url"></input>
        </form>"""
    else:
        try:
            result = scraping(str(request.form["url"]))
            return """
            <H1>参考文献を自動生成してくれるチートツールを作りたかった</H1>
            URLを入力してください
            <form action="/" method="POST">
            <input name="url"></input>
            </form>
            {}<br>""".format(result[0])+"""{}""".format(result[1])
        except:
            return"""
            <H1>参考文献を自動生成してくれるチートツールを作りたかった</H1>
            URLが間違っています<br>
            URLを入力してください
            <form action="/" method="POST">
            <input name="url"></input>
            </form>"""

## おまじない
if __name__ == "__main__":
    app.run(debug=True,threaded=True)