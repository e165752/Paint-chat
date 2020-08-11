window.onload = function () {

    var chatSocket = new WebSocket(
        'ws://' + window.location.host +
        '/ws/chat/' + roomName + '/');

    chatSocket.onmessage = function(e) {
        var data = JSON.parse(e.data);
        var message = data['message'];
        document.querySelector('#chat-log').value += (message + '\n');
    };

    chatSocket.onclose = function(e) {
        console.error('Chat socket closed unexpectedly');
    };

    document.querySelector('#bms_send_message').focus();
    document.querySelector('#bms_send_message').onkeyup = function(e) {
        if (e.keyCode === 13) {  // enter, return
            document.querySelector('#bms_send_btn').click();
        }
    };

    // 「送信」ボタン
    document.querySelector('#bms_send_btn').onclick = function(e) {
        var messageInputDom = document.querySelector('#bms_send_message');
        var message = messageInputDom.value;
        chatSocket.send(JSON.stringify({
            'message': message
        }));

        messageInputDom.value = '';
    };

    // 「お絵かき」ボタン
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

};
