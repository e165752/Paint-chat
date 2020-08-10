import requests
import json
import os
from urllib.parse import urljoin


class UIUX_ClientxChat():
    def __init__(self, room_name):
        super().__init__()
        self.app_name = 'dotsubos-test'
        self.room_name = room_name
        self.base_uri = os.environ.get('SERVER_LOCAL_BASE_URI')
        # self.base_uri = os.environ.get('SERVER_BASE_URI')
        
        self.room_uri = urljoin(os.environ.get('SERVER_LOCAL_BASE_URI'), '{}_{}/'.format(self.app_name, self.room_name))
        self.sec_key = os.environ.get('SERVER_SEC_KEY')

    def get(self, endpoint):
        print()
        rest_uri = urljoin(self.room_uri, endpoint)
        response = requests.get(rest_uri, cookies={"key":self.sec_key})
        print('[Info][./scripts/communicate.py]\n     GET ', response.url)
        return response.text

    def post(self, endpoint, data):
        print()
        rest_uri = urljoin(self.room_uri, endpoint)
        response = requests.post(rest_uri, cookies={"key":self.sec_key}, json=data)
        return response.text

    def put(self, endpoint, data):
        print()
        rest_uri = urljoin(self.room_uri, endpoint)
        response = requests.put(rest_uri, cookies={"key":self.sec_key}, json=data)
        return response.text

    def upload(self, endpoint, file_path, mimetype):
        print()
        fileDataBinary = open(file_path, 'rb').read()
        files = {'uploadFile': (file_path, fileDataBinary, mimetype)}

        rest_uri = urljoin(self.room_uri, endpoint)
        response = requests.post(rest_uri, cookies={"key":self.sec_key}, files=files)    
        return response.text

def json_print(caption, json_str):
    data = json.loads(str(json_str))
    print(caption)
    print(json.dumps(data, indent=2))
    return data

def json_to_dict(json_str):
    return json.loads(str(json_str))



if __name__ == "__main__":
    ## secret key などを読み込み。
    uiux_client = UIUX_ClientxChat('--rooms')
    print('uiux_client.base_url : ', uiux_client.base_uri, '\nuiux_client.sec_key : ', uiux_client.sec_key)
    

    # json_print("get user 1", client_rooms_.get("users/1"))
    # json_print("post", client_rooms_.post("messages", {"to": "someone", "content": "hello"}))
    # json_print("get all messages", client_rooms_.get("messages"))


    # json_print("get", post("messages", {"to":"someone","content":"hello"}))
    json_print("get", uiux_client.post("messages", {"to":"hogesan","content":"hello"}))
    json_print("get by dst", uiux_client.get("messages/to/hogesan"))
    json_print("put", uiux_client.put("messages/32", {"content":"updated"}))
    json_data = json_print("updload", uiux_client.upload("jpeg", "canvas.jpg", 'image/jpeg'))  ## .jpg 画像を送信する。（普段はコメントアウト）
    uiux_client.get("jpeg/"+json_data["result"]["file_id"])

    # print(post("users", {"name":"hogesan","tickets":"3"}))
    # print(post("users", {"name":"asan"}))
    # print(put("users/2",{"status":"busy"}))


