## 基本系
```
http://db.denchu.cloud:5111/uiuxchat3287bivsgfbivf/【アプリ名】/【関数名(endpoint)】?=【jsonデータ】
```

1. API の（URI 固定）
   - `http://db.denchu.cloud:5111/uiuxchat3287bivsgfbivf/`

2. アプリ名
   - 自由？
     - URL 的な拡張は出来ないので、静的な使い方（：一度決めたら変更しない）として使うのが良いかも。
   - ここをうまく使えば、チャットルーム 的な使い方もできるはず？
   - `【アプリ名】.【ルーム名】.【オプション】`
     - DM なら、`【アプリ名】.dm.【ユーザー名】` ？

3. 関数名(endpoint)
   - /messages や /user など。
   - get / post / put でそれぞれ異なる関数を用意しているらしい。
   - GET : データ取得
     - `/messages`： アプリ内の全てのメッセージを取得
       - `/<int:message_id>`： message_idのメッセージのみを取得
       - `/to/<string:to>` ： 宛先で絞り込み
       - `/from/<string:from_>/to/<string:to_>` ： 宛先と発信者で絞り込み
       - `/after/<string:time>` ： 発信時刻で絞り込み(time以降のメッセージ)
     - `/users`： 全ユーザ情報の取得
       - `/<int:user_id>` ： user_idのユーザ情報を取得
     - `/jpeg`
       - `/<string:file_id>` ： file_idのjpegファイルをダウンロード.file_idはPOST時に返るIDを指定する
   - POST : メッセージの送信(メソッド)
     - `/messages`： メッセージを送信. idが返る．データ構造に従ってJSONで送る
     - `/users`： ユーザを追加. idが返る. データ構造に従ってJSONで送る
     - `/jpeg`： jpegファイルをアップロード(jpegファイル限定). file_idが返る。ファイルは，multipart/form-dataでname = 'uploadFile'として送信する(htmlのformタブでアップロードするのと同じ)
   - PUT : メッセージの更新
       - `/<int:message_id>` ： message_idのメッセージを更新する。指定したフィールドのみが更新される（JSONに記述されていないフィールドは変更されない）
       - `/<int:uid>` ： ユーザ情報の更新

4.  json データ（言語側が、get, post の引数として用意している）
    - /message
      - from
        - 発信者 :string
      - to
        - 宛先 :string
      - content
        - 本文 :string
      - timestamp
        - 発信時刻（省略すると現在時刻） :%Y-%m-%d_%H:%M:%S
      - priority
        - 重要度など :int
      - parent
        - 親メッセージIDなど :int
    - /user
      - name
        - 名前:string
      - status
        - 状態など:string
      - tickets
        - チケットなど:string

