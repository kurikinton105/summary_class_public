from flask import Flask, render_template,request #追加
from bag_of_words import bag_of_words_sum
app = Flask(__name__)

@app.route("/num", methods=["GET", "POST"])
def odd_even():
    if request.method == "GET":
        return """
        下に整数を入力してください。奇数か偶数か判定します
        <form action="/" method="POST">
        <input name="num"></input>
        </form>"""
    else:
        try:
            return """
            下に整数を入力してください。奇数か偶数か判定します
            <form action="/" method="POST">
            <input name="num"></input>
            </form>
            {}は{}です！""".format(str(request.form["num"]), ["偶数", "奇数"][int(request.form["num"]) % 2])
        except:
            return """
                有効な数字ではありません！入力しなおしてください。
                <form action="/" method="POST">
                <input name="num"></input>
                </form>"""

@app.route("/", methods=["GET", "POST"])
def web():
    if request.method == "GET":
        #WEBリンクを代入
        return """
        <H1>bag-of-wordsを使った要約アプリ</H1>
        文章を入力してください
        <form action="/" method="POST">
        <input name="text"></input>
        </form>"""
    else:
        #try:
        result = bag_of_words_sum(str(request.form["text"]),50,100)
        return """
        <H1>bag-of-wordsを使った要約アプリ</H1>
        文章を入力してください
        <form action="/" method="POST">
            <input name="text"></input>
            </form>
            {}<br>""".format(result)

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

@app.route('/hello')
def hello():
    name = "Hoge"
    #return name
    return render_template('hello.html', name=name) #変更

#/goodのところに反映される。テンプレが
@app.route('/good')
def good():
    name = "Good"
    return render_template('good.html', name=name)

@app.route('/form')
def form():
   return render_template('form.html')

@app.route('/confirm', methods = ['POST', 'GET'])
def confirm():
   if request.method == 'POST':
      result = request.form
      return render_template("confirm.html",result = result)

## おまじない
if __name__ == "__main__":
    app.run(debug=True)