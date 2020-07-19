from flask import Flask, render_template,request #追加
from bag_of_words import bag_of_words_sum
from MakeClassEasy import MakeClassEasy
app = Flask(__name__)

@app.route("/cos5year", methods=["GET", "POST"])
def odd_even():
    if request.method == "GET":
        return """
        <H1>我々はCos5year(こすごいやー)だ！！！！<H1>
        <H1>おそらく地球を侵略しにきた！！！！<H1>
        <H1>なんかいい感じの開発して世界を征服するぞ！！！！！<H1>
        （ごめんなさい...ふざけました...）
        開発者yamaより
        """

@app.route("/", methods=["GET", "POST"])
def main_page():
    if request.method == 'GET':
        #print("GET")
        text = "ここに結果が出力されます"
        data_word = [" "]
        val = False
        return render_template("make-class-easy.html",text=text,data_word=data_word,val = val)
    elif request.method == 'POST':
        #print("POST")
        val = True #フラグを１にする
        text = request.form["input_text"]
        try:
            result,data_word = bag_of_words_sum(str(text),50,100)
            return render_template("make-class-easy.html",text=result,data_word=data_word,val = val)
        except:
            return render_template("make-class-easy.html",text="Error:文章は２文以上にしてください。もう一度文章を入力してください")

@app.route("/develop", methods=["GET", "POST"])
def develop_page():
    if request.method == 'GET':
        #print("GET")
        text = "ここに結果が出力されます"
        data_word = [" "]
        val = False
        return render_template("make-class-easy-develop.html",text=text,data_word=data_word,val = val)
    elif request.method == 'POST':
        #print("POST")
        val = True #フラグを１にする
        text = request.form["input_text"]
        try:
            summary,explain,time = MakeClassEasy(str(text),50,100)
            return render_template("make-class-easy-develop.html",text=summary,data_explain=explain,val = val,process_time=time)
        except:
            return render_template("make-class-easy-develop.html",text="Error:文章は２文以上にしてください。もう一度文章を入力してください")


## おまじない
if __name__ == "__main__":
    app.run(debug=True,threaded=True)