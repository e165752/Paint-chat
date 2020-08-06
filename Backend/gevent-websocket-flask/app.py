# -*- coding: utf-8 -*-

import json
import datetime
import time

from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler, Client
from geventwebsocket.websocket import WebSocket
from geventwebsocket import WebSocketError

from flask import Flask, request, render_template

app = Flask(__name__)
app.config.from_object(__name__)

clients = {} # 1

# app.py
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/pipe')
def pipe():
    ws: WebSocket = request.environ.get('wsgi.websocket')
    if not ws:
        raise Exception("Expected WebSocket request.")

    print("\n[Info] 接続しました！")
    
    while True:
        handler: WebSocketHandler = ws.handler
        message: str = ws.receive()
        if message is None:
            print("[Info] 切断された？")
            break
        print('\n[Info] handler.server.clients : ', handler.server.clients)

        datetime_now = datetime.datetime.now()
        data = {
            'time': str(datetime_now),
            'message': message
        }
        # ws.send(json.dumps(data))
        print(data)

        # WSGIServerには本来、clientというプロパティは無いけど、コレを継承しているWebSocketHandlerで動的に追加されてる。
        # なので、型ヒントが利用できない（？）のでignoreするように
        for client_tmp in handler.server.clients.values(): # type: ignore
            # for文では型ヒントが利用できないので、以下のように型ヒントを付けた変数に再代入している。
            client: Client = client_tmp
            if client.ws.environ:
                print('[Info] client.ws.environ["HTTP_SEC_WEBSOCKET_KEY"] : ', client.ws.environ.get('HTTP_SEC_WEBSOCKET_KEY', ''))
            else:
                print('空。ブラウザを閉じたり画面を更新したりすると、クライアントから「切断したよ」、という情報が飛んでくる。')

            # client.ws.send('message: %s, (client_address :%s)' % (message, client.address))
            client.ws.send(json.dumps(data))
    return 'Disconnected (?)'



if __name__ == '__main__':
   app.debug = True

   host = 'localhost'
   port = 8181
   print(" * Running on http://{}:{}/ (Press CTRL+C to quit)".format(host, port))

   host_port = (host, port)
   server = WSGIServer(
       host_port,
       app,
       handler_class=WebSocketHandler
   )
   server.serve_forever()


