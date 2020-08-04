## 概要
UI/UX チャットサーバー の ソースコードを、ローカルで動かせるようにしました。

その他やったこと
- Client 側の `post.py` を、自分なりに改造した。 → [`client_example/communicate.py`](client_example/communicate.py)
- Server 側の ソースコードを（少し）リファクタリングした。
- ローカルで動かすまでの手順を、↓ にまとめた。


## インストール
1. pip
    ```
    $ pip3 install  flask sqlalchemy requests
    ```
2. データベースの初期化
    ```
    $ python3 create_tables.py
    ```
3. brew （やらなくてもできた）
    ```
    $ brew install  db-browser-for-sqlite
    ```

## サーバー 起動
```
$ python3 DB/create_tables.py
```

## サーバー 動作確認
```
$ cd client_example
$ python3 communicate.py
```
- 細かい動作確認
  1. `jpg/` に、[`client_example/canvas.jpg`](client_example/canvas.jpg) がコピーされている？
     - `【アプリ名】_【日付】_canvas.jpg` というファイル名で
     - 複数回実行すると、`【日付】` が異なる画像ファイルが複数できるはず。
  2. `$ python3 communicate.py` の出力の最後に表示される URL を開いてみる。
     - ブラウザ や `$ curl` などで。
     - `http://0.0.0.0:5111/uiuxchat3287bivsgfbivf/dotsubos-test/jpeg/【アプリ名】_【日付】_canvas.jpg` みたいなやつ。
     - ブラウザで画像が表示された？
  3. サーバー側の出力にエラーは出てない？

