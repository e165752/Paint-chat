from django.http import HttpResponseRedirect, HttpResponse
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


### Room 選択
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
    # all_rooms = json_print("get all users", client_rooms_.get("users"))
    all_rooms = json_to_dict(client_rooms_.get("users"))
    ## room の {"__room_name" : "__id"} 辞書を作成する。
    print_info_x('views', locals().items(), all_rooms)
    if 'error' in all_rooms.keys():
        return []
    return [r['name'] for r in all_rooms["result"]]
    



### Room に入る。
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


def send_message(request):
    post_dict = json.loads(request.body)

#     if request.method == 'POST':
#         # request.bodyに入っている。
#         message = post_dict['message']
#         loc_path = post_dict['loc_path']
#         room_name = loc_path.split('/')[-1]
#         print('[Info] loc_path, room_name : ', loc_path, room_name)
#         print('[Info] message : ', message)

#         # メッセージをサーバーに送信する。
#         _client = UIUX_ClientxChat('--rooms') 
#         # json_print("post", _client.post("messages", {"to":"hogesan","content":"hello"}))
#         file_id = json_to_dict(_client.post("messages", {"to":"hogesan","content":"hello"}))#["result"]["file_id"]
#         # サーバーからの返答の file_id を、メッセージ のコンテンツに追加して、メッセージを送信する。
#         # res = {
#         #   "result": {
#         #     "file_id": "dotsubos-test_--rooms_20200811_170847_paint_scripts_tmp.jpg"
#         #   }
#         # }
#         print('[Info] file_id : ', file_id)
        
#     return HttpResponse()


