import requests
import json
import os
from urllib.parse import urljoin


class UIUX_ClientxChat():
    def __init__(self, room_name):
        super().__init__()
        self.app_name = 'dotsubos-test'
        self.room_name = room_name
        # self.base_uri = os.environ.get('SERVER_LOCAL_BASE_URI')
        self.base_uri = os.environ.get('SERVER_BASE_URI')
        print('[Info] self.base_uri : ', self.base_uri)
        
        self.room_uri = urljoin(self.base_uri, '{}_{}/'.format(self.app_name, self.room_name))
        self.sec_key = os.environ.get('SERVER_SEC_KEY')

    def get(self, endpoint):
        print()
        rest_uri = urljoin(self.room_uri, endpoint)
        print('[Info][./scripts/communicate.py]\n     GET ', rest_uri)
        response = requests.get(rest_uri, cookies={"key":self.sec_key})
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

