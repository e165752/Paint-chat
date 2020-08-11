from django.shortcuts import render
from django.template.context_processors import csrf
from django.http import QueryDict, HttpResponse

from PIL import Image
from io import BytesIO
import base64
import json
import re

from .scripts.communicate import *
from .scripts.log_utils import *


# Create your views here.
def canvas(request, room_name):
    print_info_x('views', locals().items(), room_name)
    return render(request, 'paint/canvas.html', {})


def receiveAndSendJPG(request):
    if request.method == 'POST':
        print('\n[Info]  ~~[receiveAndSendJPG]~~')
        # request.bodyに入っている。
        post_dict = json.loads(request.body)
        # データを抽出する。
        canvasData = post_dict['imgBase64']
        # print_info_x('views', locals().items(), canvasData)
        loc_path = post_dict['loc_path'].strip("/") 
        room_name = loc_path.split('/')[-1]
        print_info_x('views', locals().items(), loc_path, room_name)

        im_base64 = re.sub('^data:image/.+;base64,', '', canvasData)
        # base64 str を表示してみる。 
        # print(im_base64)
        im = Image.open(BytesIO(base64.b64decode(im_base64)))
        # 画像を表示してみる。
        # im.show()

        # tmp.jpg ファイルにするのが一番楽だったので、それで。
        jpg_path = 'paint/scripts/tmp.jpg'
        im.save(jpg_path, quality=100)

        # 画像をサーバーに送信する。
        _client = UIUX_ClientxChat(room_name) 
        # json_print("updload", _client.upload("jpeg", jpg_path, 'image/jpeg'))
        file_id = json_to_dict(_client.upload("jpeg", jpg_path, 'image/jpeg'))["result"]["file_id"]
        # サーバーからの返答の file_id を、メッセージ のコンテンツに追加して、メッセージを送信する。
        # res = {
        #   "result": {
        #     "file_id": "dotsubos-test_--rooms_20200811_170847_paint_scripts_tmp.jpg"
        #   }
        # }
        print_info_x('views', locals().items(), file_id)
        
    return HttpResponse()

