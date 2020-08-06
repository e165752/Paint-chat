# 概要
- uiux_server に送受信する、client 側の実装。
- 先生が Python版をは用意していたが、JavaScript から Pyhton を呼び出すのは、（クライアント側については）一般的ではないっぽいので、JavaScript に移植してみた。
- やったこと
  - Python版の（魔）改造。
  - JavaScriptへの移植。

# 使い方
## Python版
- Insntall
    ```
    touch config.json
    pip3 install -r source/requirements.txt
    ```
    - `config.json` という空ファイルができてるはず。
      - 以下を書き込む。
        ```
        {
            "base_uri": "http://db.denchu.cloud:5111/uiuxchat3287bivsgfbivf/",
            "base_uri-local_test": "http://0.0.0.0:5111/uiuxchat3287bivsgfbivf/",
            "app-0": "test2/",
            "app-1": "【アプリ名を自由に指定】",
            "sec_key": "【シークレットキー を書き込む】"
        }
        ```
      - `【〜】` は、指定された情報で書き換えること。
- 実行
    ```
    $ python3 communicate.py
    ```
    - 実装見れば、やってることは大体わかるはず？（笑）


## JavaScript版


