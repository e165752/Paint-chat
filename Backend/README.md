## チャットアプリとして結合！
- Django で。
- 参考サイト
  - [DjangoとChannelsで簡単なチャットサーバーを構築(1)](https://blog.fantom.co.jp/2019/06/22/build-a-simple-chat-server-with-django-and-channels-1/)
  - [DjangoとChannelsで簡単なチャットサーバーを構築(2)](https://blog.fantom.co.jp/2019/06/25/build-a-simple-chat-server-with-django-and-channels-2/)
  - [DjangoとChannelsで簡単なチャットサーバーを構築(3)](https://blog.fantom.co.jp/?s=DjangoとChannelsで簡単なチャットサーバーを構築)

## インストール
- Djangoアプリ （: client server）
  - pyenv や virtualenv などで、仮想環境を作ることをオススメします。
  - 必要なライブラリのインストール
      ```
      $ pip3 install -r oekaki_chat/requirements.txt
      ```
- ログサーバー（: server） local 版
  1. pip
      ```
      $ pip3 install  flask sqlalchemy requests
      ```
  2. データベースの初期化
      ```
      cd uiux_server_plus/DB
      python3 create_tables.py
      cd ../..
      ```
  3. brew （やらなくてもできた）
      ```
      $ brew install  db-browser-for-sqlite
      ```


## 起動
- Djangoアプリ （: client server）
    ```
    $ python3 manage.py runserver
    ```
- ブラウザ （: client）
  - チャットUI
    - http://127.0.0.1:8000/chat
    - ルーム名を入力すると、http://127.0.0.1:8000/chat/【ルーム名】 に飛ぶはず。
      - 「URLに使えない文字」を入れると落ちるので注意。
      - （なぜか WebSocket が落ちる...）
  - お絵かき機能
    - http://127.0.0.1:8000/paint
    - やること？
      - 別ウィンドウで開く
        - https://blog.narito.ninja/detail/62
      - サーバーへの送信
        - Pythonを呼び出す方法も調査中。
        - [DjangoでGET／POSTから値を取得する方法](https://intellectual-curiosity.tokyo/2019/02/27/DjangoでGET／POSTから値を取得する方法)

- ログサーバー（: server） local 版
    ```
    $ python3 uiux_server_plus/run.py
    ```




## （おまけ）ページの追加方法
1. viewを作成
2. urlを設定
3. [テスト] 2.で設定したURLにブラウザでアクセスしてみる。
