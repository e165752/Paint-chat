from django.shortcuts import render
from django.template.context_processors import csrf
from django.http import QueryDict, HttpResponse

from PIL import Image
from io import BytesIO
import base64
import json
import re


# Create your views here.
def canvas(request, room_name):
    print('\n[Info] room_name : ', room_name)
    return render(request, 'paint/canvas.html', {})


def receiveAndSendJPG(request):
    canvasData = request.POST.get('canvasData', '')
    canvasData = request.POST.get('imgBase64', '')

    # res_data = base64.b64decode(request.body)
    print('[Info] request.body : ', request.body)
    print('[Info] json.loads(request.body) : ', json.loads(request.body))
    post_dict = json.loads(request.body)

    if request.method == 'POST':
        # request.bodyに入っている。
        # dic = QueryDict(request.body, encoding='utf-8')  #, encoding='utf-8'
        # print('[Info] dic : ', dic)
        # print('[Info] dic.keys : ', dic.keys())
        # print('[Info] dic.dict : ', dic.dict())
        canvasData = post_dict['imgBase64']
        loc_path = post_dict['loc_path']
        print('[Info] loc_path : ', loc_path)
        
        im_base64 = re.sub('^data:image/.+;base64,', '', canvasData)
        # base64 str を表示してみる。 
        # print(im_base64)
        im = Image.open(BytesIO(base64.b64decode(im_base64)))
        # 画像を表示してみる。
        im.show()
        
    return HttpResponse()

