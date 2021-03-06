window.onload = function () {

    // CSRF token 設定
    axios.defaults.xsrfCookieName = 'csrftoken'
    axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"

    //*--  WebSocket 初期化  --*//
    var socket_url = 'ws://' + window.location.host + '/ws/chat/' + roomName + '/';
    var chatSocket = new WebSocket(socket_url);
    console.log('[Info][room.js] chatSocket :', chatSocket);

    var board = document.querySelector('#jsi-board');
    //  [WebSocket] メッセージ受信時
    chatSocket.onmessage = function(e) {
        var data = JSON.parse(e.data);
        var message_dict = JSON.parse(data['text_data']);   // 'text_data' (key) は、WebSocket側で調整可能。
        if (last_message_id < message_dict['id']) {
            addText(message_dict['message'])
            addText('-')
            // 表示済みメッセージの id をメモ（していいのはここだけ！）
            last_message_id = message_dict['id'];
        }
    };
    //  [WebSocket] メッセージ切断時
    chatSocket.onclose = function(e) {
        console.error('Chat socket closed unexpectedly');
        // ウィンドウを再読み込み
        // location.reload(true);
        setTimeout("location.reload()", 1500);
    };

    //受け取り後の処理
    function addText(json){
        var msgDom = $('<li>');
        msgDom.html(json);

        board.append(msgDom[0]);
        // console.log('[Info] message : ', msgDom[0]);
    }

    // Room のチャットログを全件取得する。
    var last_message_id = 0;
    function getAllMessages() {
        csrftoken = Cookies.get('csrftoken');
        headers = { 'X-CSRFToken': csrftoken };
        axios.post('/chat/messages/', {
            'loc_path': location.pathname,
            headers: headers,
        })
        .then(function (response) {
            if (response.data['result']) {
                for (let [idx, m_json] of Object.entries(response.data['result'])) {
                    if (last_message_id < m_json.id) {
                        chatSocket.send(JSON.stringify({
                            'id': m_json.id,
                            'message': m_json.content,
                        }));
                    }
                }
            } else {
                console.log('[Error][getAllMessages()] message が受信できませんでした。')
            }
        })
        .catch(function (error) {
            console.log(error);
        });
    }


    // document.querySelector('#bms_send_message').focus();
    // document.querySelector('#bms_send_message').onkeyup = function(e) {
    //     if (e.keyCode === 13) {  // enter, return
    //         document.querySelector('#bms_send_btn').click();
    //     }
    // };

    //*--  「送信」ボタン  --*//
    document.querySelector('#bms_send_btn').onclick = function(e) {
        var messageInputDom = document.querySelector('#jsi-msg');
        var message = messageInputDom.value;

        axios.post('/chat/message/', {
            message : message,
            loc_path : location.pathname,
          })
          .then(function (response) {
            // console.log(response.data);
            chatSocket.send(JSON.stringify({
                'id': response.data.id,
                'message': message
            }));
        })
          .catch(function (error) {
            console.log(error);
          }
        );

        // 入力欄を初期化
        messageInputDom.value = '';
    };

    //*--  「お絵かき」ボタン  --*//
    document.querySelector('#bms_pic_btn').onclick = function(e) {
        var win;
        if (!win || win.closed) {
            var loc_host = location.hostname,
                loc_port = location.port,
                loc_path = location.pathname;
            // console.info("loc_host, loc_path : ", loc_host, loc_path);
            var loc_paint = `http://${loc_host}:${loc_port}/paint${loc_path}`
            console.info("loc_paint : ", loc_paint);
            // ウィンドウオブジェクトを格納した変数が存在しない or ウィンドウが閉じられている場合は，新規ウィンドウを開く。
            win = window.open(loc_paint, 'お絵かき',
                    'menubar=no, toolbar=no, scrollbars=no, '
                    + 'width=930, height=450');
        }else{
            win.focus();
        }
    };


    // サーバーからログをダウンロード（最初の1回目）
    (function () {
        getAllMessages();
        console.log('[Info] getAllMessages() （初回実行）完了！');
        // 定期的に、サーバーにアクセスして、更新がないか確認する（ポーリング）
        const timer = setInterval(getAllMessages, 10000);
    }());

};
