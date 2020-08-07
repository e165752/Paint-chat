## チャットアプリとして結合！
- Django で。
- 参考サイト
  - [DjangoとChannelsで簡単なチャットサーバーを構築(1)](https://blog.fantom.co.jp/2019/06/22/build-a-simple-chat-server-with-django-and-channels-1/)
  - [DjangoとChannelsで簡単なチャットサーバーを構築(2)](https://blog.fantom.co.jp/2019/06/25/build-a-simple-chat-server-with-django-and-channels-2/)
  - [DjangoとChannelsで簡単なチャットサーバーを構築(3)](https://blog.fantom.co.jp/?s=DjangoとChannelsで簡単なチャットサーバーを構築)

## インストール
- pyenv や virtualenv などで、仮想環境を作ることをオススメします。
- 必要なライブラリのインストール
    ```
    $ pip3 install -r oekaki_chat/requirements.txt
    ```
- 


## 起動
- Djangoアプリ ：server（中間）
    ```
    $ python3 manage.py runserver
    ```
- ブラウザ ：client
  - チャットUI
    - http://127.0.0.1:8000/chat
    - ルーム名を入力すると、http://127.0.0.1:8000/chat/【ルーム名】 に飛ぶ。
      - 現在は、英語のみ対応。
      - 英語以外のルーム名にすると、WebSocket が落ちるっぽい。
  - お絵かき機能
    - http://127.0.0.1:8000/paint
    - ボタンから飛ぶようにする場合は、WebSocket 周りの同期もあるので、起動まではバックエンドが担当する形が良いかも？
      - 「別ウィンドウで開く」を調査中。
        - https://blog.narito.ninja/detail/62
      - サーバーへの送信などもまだなので、そこもやらないと...
        - Pythonを呼び出す方法も調査中。
        - [DjangoでGET／POSTから値を取得する方法](https://intellectual-curiosity.tokyo/2019/02/27/DjangoでGET／POSTから値を取得する方法)




## （おまけ）ページの追加方法
1. viewを作成
2. urlを設定
3. [テスト] 2.で設定したURLにブラウザでアクセスしてみる。

