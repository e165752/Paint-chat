from django.http import HttpResponseRedirect, HttpResponse, HttpResponseServerError, JsonResponse
from django.template import loader
from django.shortcuts import render
from django.utils.safestring import mark_safe

from io import BytesIO
import base64
import json
import re
import json
from .scripts.communicate import *
from .scripts.log_utils import *


### Room 画面
def index(request):
    # room_list = Room.objects.order_by('-created_at')[:5]
    template = loader.get_template('chat/index.html')
    context = {
        'room_list': get_all_rooms(),
    }
    return HttpResponse(template.render(context, request))

# 最新のRoom一覧を、データベースからダウンロードする。
def get_all_rooms():
    ### get
    client_rooms_ = UIUX_ClientxChat('--rooms') 
    all_rooms = json_to_dict(client_rooms_.get("users"))
    if 'error' in all_rooms.keys():
        return []
    return [r['name'] for r in all_rooms["result"]]
    



### Room 画面
def room(request, room_name):
    # もし Room が存在しなければ、新しくサーバーに Room を作る。（Post）
    if room_name not in get_all_rooms():
        ### post
        client_rooms_ = UIUX_ClientxChat('--rooms') 
        print_info('views', room_name, 'が見つかりませんでした。Room を新規作成します！')
        json_str = client_rooms_.post("users", {"name": room_name})
        json_print("[Info] Post new Room.", json_str)
    print_info_x('views', locals().items(), room_name)
    return render(request, 'chat/room.html', {
        'room_name_json': mark_safe(json.dumps(room_name))
    })

# def update_room(request, n_room_name='____', n_status="{ 'users': [1,3,4] }", n_tickets=""):
#     ### put
#     print('[Info] in_room_name : ', in_room_name)
#     json_str = client_rooms_.put("users/1", {"name": n_room_name, "status": n_status, "tickets": n_tickets})
#     json_print("[Info] Put (Update) room name.", json_str)
#     return HttpResponse()


def get_all_messages(request):
    if request.method == 'POST' and request.body:
        print('\n[Info]  ~~[get_all_messages]~~')
        # request.bodyに入っている。
        post_dict = json.loads(request.body)

        # データを抽出する。
        loc_path = post_dict['loc_path'].strip("/") 
        room_name = loc_path.split('/')[-1]
        print_info_x('views', locals().items(), loc_path, room_name)

        # メッセージをサーバーに送信する。
        _client = UIUX_ClientxChat(room_name)
        all_messages_dict = json_to_dict(_client.get("messages"))
        print_info_x('views', locals().items(), all_messages_dict)   # 確認
        # all_messages_dict = {
        #   "result": [
        #     {'id': 47, 'from': 'None', 'to': 'hogesan', 'content': 'メッセージテスト確認', 'timestamp': '2020-08-13_12:54:27', 'priority': 0, 'parent': -1}, {'id': 48, 'from': 'None', 'to': 'None', 'content': 'dotsubos-test_img_test_20200813_125529_paint_scripts_tmp.jpg', 'timestamp': '2020-08-13_12:55:29', 'priority': 1, 'parent': -1}]}}
        #   ]
        # }

        return JsonResponse(all_messages_dict)
    else:
        return HttpResponseServerError()



def send_message(request):
    if request.method == 'POST' and request.body:
        print('\n[Info]  ~~[send_message]~~')

        # request.bodyに入っている。
        post_dict = json.loads(request.body)
        # データを抽出する。
        message = post_dict['message']
        print_info_x('views', locals().items(), message)
        loc_path = post_dict['loc_path'].strip("/") 
        room_name = loc_path.split('/')[-1]
        # print_info_x('views', locals().items(), loc_path, room_name)

        # メッセージをサーバーに送信する。
        _client = UIUX_ClientxChat(room_name) 
        res = json_to_dict(_client.post("messages", {
                "to": "hogesan",
                "content": message,
            }) )
        # res -> {'result': {'id': 23}
        print_info_x('views', locals().items(), res)
        
        return JsonResponse(res['result'])
    else:
        return HttpResponseServerError()


