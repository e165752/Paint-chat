from django.http import HttpResponseRedirect, HttpResponse
from django.template import loader
from django.shortcuts import render
from django.utils.safestring import mark_safe
import json
from .scripts.communicate import *



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
    print('[Info] all_rooms : ', all_rooms)
    if 'error' in all_rooms.keys():
        return []
    return [r['name'] for r in all_rooms["result"]]
    



### Room に入る。
def room(request, room_name):
    # もし Room が存在しなければ、新しくサーバーに Room を作る。（Post）
    if room_name not in get_all_rooms():
        ### post
        client_rooms_ = UIUX_ClientxChat('--rooms') 
        print('\n[Info] {} が見つかりませんでした。Room を新規作成します！'.format(room_name))
        json_str = client_rooms_.post("users", {"name": room_name})
        json_print("[Info] Post new Room.", json_str)
    print('\n[Info] in_room_name : ', room_name)
    return render(request, 'chat/room.html', {
        'room_name_json': mark_safe(json.dumps(room_name))
    })

# def update_room(request, n_room_name='____', n_status="{ 'users': [1,3,4] }", n_tickets=""):
#     ### put
#     print('[Info] in_room_name : ', in_room_name)
#     json_str = client_rooms_.put("users/1", {"name": n_room_name, "status": n_status, "tickets": n_tickets})
#     json_print("[Info] Put (Update) room name.", json_str)
#     return HttpResponse()

# def send_message(request):
#     print(in_room_name)
#     print(request)
#     if request.method == 'POST':
#         if 'bms_send_btn' in request.POST:
#             # ボタン1がクリックされた場合の処理
#             print('[Info] bms_send_btn')
#         elif 'bms_pic_btn' in request.POST:
#             # ボタン2がクリックされた場合の処理
#             print('[Info] bms_pic_btn')


