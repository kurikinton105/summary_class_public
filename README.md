# summary_class

## 概要
Azure Speech と bag-of-wordsを使って、録音した授業の音声データから授業の要約を作ろうというプロジェクト


### 作成者
yama [@kurikinton105](https://github.com/kurikinton105)

tomSoya [@tomsoyaN](https://github.com/tomsoyaN)

jima884 [@jima884](https://github.com/jima884)

## 使うための前準備
#### Azure からアクセスキーを取得

Azureからアクセスキーをゲットしてください。password.py内に記述します。

#### ライブラリのインストール
1. コマンドでsummary_class_publicフォルダ内に移動し 
```bash
    $pip install -r requirements.txt
    または
    $py -m install -r requirements.txt
```
を実行する  
  
2. 下記よりtermextractをダウンロードし解凍する.  
  http://gensen.dl.itc.u-tokyo.ac.jp/soft/pytermextract-0_01.zip  
  コマンドにて解凍先に移動し,
  ```bash
    $pip install .
    または
    $py -m install .
  ```
を実行する  
  
## デモ
#### AzureにWEBアプリケーションとして公開しています。

文字を要約する部分のみです。

WEBアプリケーション

https://summary-classes-web.azurewebsites.net/


ローカル環境での実行方法

```bash
    export FLASK_APP=application.py
    flask run
```

