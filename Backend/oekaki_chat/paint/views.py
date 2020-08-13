from django.shortcuts import render
from django.template.context_processors import csrf
from django.http import QueryDict, HttpResponse, HttpResponseServerError, JsonResponse

from PIL import Image
from io import BytesIO
import base64
import json
import re

from .scripts.communicate import *
from .scripts.log_utils import *
from django.utils.safestring import mark_safe


# Create your views here.
def canvas(request, room_name):
    print_info_x('views', locals().items(), room_name)
    return render(request, 'paint/canvas.html', {
        'room_name_json': mark_safe(json.dumps(room_name))
    })


def receiveAndSendJPG(request):
    if request.method == 'POST':
        print('\n[Info]  ~~[receiveAndSendJPG]~~')
        # request.bodyに入っている。
        post_dict = json.loads(request.body)

        # データを抽出する。(JS で jpeg ファイルに保存するのは、あまりよろしくないらしいので、Python でやる方向で)
        jpg_path = convert_base64_to_jpg_file(post_dict['imgBase64'])
        loc_path = post_dict['loc_path'].strip("/") 
        room_name = loc_path.split('/')[-1]
        # print_info_x('views', locals().items(), loc_path, room_name)  # 確認

        # 画像をサーバーに送信する。
        _client = UIUX_ClientxChat(room_name) 
        img_file_name = json_to_dict(_client.upload("jpeg", jpg_path, 'image/jpeg'))["result"]["file_id"]
        # res = {
        #   "result": {
        #     "file_id": "dotsubos-test_--rooms_20200811_170847_paint_scripts_tmp.jpg"
        #   }
        # }

        # サーバーからの返答の file_id を、messages の content に追加して、メッセージを送信する。
        content_img_src = '<img src="{}jpeg/{}" width="50%" height="50%">'.format(_client.room_uri, img_file_name)
        # print_info_x('views', locals().items(), content_img_src)  # 確認
        res = json_to_dict(_client.post("messages", {
                # "priority": 1,  # textは 0,  imgは 1
                "content": content_img_src,
            }) )
        print_info_x('views', locals().items(), res)
        # res -> {'result': {'id': 23}

        return JsonResponse(res['result'])
    else:
        return HttpResponseServerError()


def convert_base64_to_jpg_file(imgBase64, jpg_path='paint/scripts/tmp.jpg'):
    im_base64 = re.sub('^data:image/.+;base64,', '', imgBase64)
    im = Image.open(BytesIO(base64.b64decode(im_base64)))
    # im.show()    # 画像を表示してみる。
    # ファイル（tmp.jpg）にするのが一番楽だったので、それで。
    im.save(jpg_path, quality=100)
    return jpg_path


