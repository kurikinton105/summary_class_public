# MakeClassEasy

## 概要
Azure Speech と bag-of-wordsを使って、録音した授業の音声データから授業の要約を作ろうというプロジェクト


### 作成者
yama [@kurikinton105](https://github.com/kurikinton105)

tomSoya [@tomsoyaN](https://github.com/tomsoyaN)

jima884 [@jima884](https://github.com/jima884)

## 実行方法
全手順において,まずこのレポジトリをダウンロードしておきます.  
初めに必要なライブラリのインストールを行います.  
### ライブラリのインストール
ターミナルでsummary_class_publicフォルダ内に移動し
```bash
   $echo termextract==0.12b0 >> requirements.txt
```
を実行した後,
```bash
    $pip install -r requirements.txt
    または
    $py -m install -r requirements.txt
```
を実行する  

### ・音声ファイルからテキストファイルに変換する.
音声ファイルをテキスト化する処理を行いたい場合,このレポジトリ内のipynbsディレクトリ内の
Speech2Text.ipynbを使用します.  
前提としてAzureのSpeechAPIのアクセスキーを取得しておく必要があります.  
取得したキー及び地域をipynbs/password.py内に記載してください.  

### ・JupyterNoteBook上で実行する場合
JupyterNoteBookを起動.このレポジトリ内の
ipynbsフォルダのProgram.ipynbを実行することで,結果が出力されます.  
sampledata.txtの内容を置き換えることで,別のテキストの要約ができます.  
詳しくはipynb内のREADMEを参照.  
### ・Flask上で実行する場合
このレポジトリをダウンロードし,ターミナルを起動.    
cdでこのレポジトリに移動した後,以下のコマンドを実行する.  

#### MAC,Linux系のターミナルの場合
```bash
    export FLASK_APP=application.py
    flask run
```
#### WindowsのCMDプロンプトの場合
```bash
    set FLASK_APP=application.py
    flask run
```
#### Windowsのパワーシェルの場合
```bash
    $env:FLASK_APP = "application.py"
    flask run
```

127.0.0.1:5000及び127.0.0.1:5000/developにアクセスすることで,WEBアプリケーション版を利用できます.
  
## デモ
#### AzureにWEBアプリケーションとして公開しています。

文章か要約,重要語抽出を行う部分のみです

WEBアプリケーション

https://summary-classes-web.azurewebsites.net/





## 使用技術
Azure Speech

Bag-of-words

Cos類似度

## 参照
termextract

http://gensen.dl.itc.u-tokyo.ac.jp/

のコードを使用しています。

## Python 実行環境

このリポジトリの開発・ビルド対象は **Python 3.14.x** です。セットアップ前に `python --version` で確認し、必要なら Python 3.14 の仮想環境を作ってから `python -m pip install -r requirements.txt` を実行してください。

Azure App Service のランタイム設定と GitHub Actions のビルド時バージョンは別物です。`.github/workflows/master_summary-classes-web.yml` のビルド設定を変更しても、**既存 Azure Web App の実行ランタイム (`linuxFxVersion`) は自動では更新されません**。Python 3.14 対応版をデプロイする前に、Azure Portal か Azure CLI で App Service の実行ランタイムを `PYTHON|3.14` に変更してください。現在値は以下で確認できます。

```sh
az webapp config show --resource-group <resource-group-name> --name summary-classes-web --query linuxFxVersion
```

実行ランタイムの変更後、Python 3.14 上で依存関係のインストールと `python -m unittest discover -s tests -v` を確認してください。

参考: https://learn.microsoft.com/ja-jp/azure/app-service/configure-language-python
