from django.http import HttpResponseRedirect, HttpResponse
from django.template import loader
from django.shortcuts import render
from django.utils.safestring import mark_safe
import json

def index(request):
    # room_list = Room.objects.order_by('-created_at')[:5]
    room_list = [Room(), Room()]
    template = loader.get_template('chat/index.html')
    context = {
        'room_list': room_list,
    }
    return HttpResponse(template.render(context, request))

class Room():
    def __init__(self):
        # リモートサーバー からダウンロード？
        self.name = "test-room"


def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name_json': mark_safe(json.dumps(room_name))
    })


def send_message(request):
    print(request)
    if request.method == 'POST':
        if 'bms_send_btn' in request.POST:
            # ボタン1がクリックされた場合の処理
            print('[Info] bms_send_btn')
        elif 'bms_pic_btn' in request.POST:
            # ボタン2がクリックされた場合の処理
            print('[Info] bms_pic_btn')


