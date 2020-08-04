import requests
import json

base_url = "http://db.denchu.cloud:5111/uiuxchat3287bivsgfbivf/test2/"
#base_url = "http://0.0.0.0:5111/uiuxchat3287bivsgfbivf/test2/"
sec_key = "gfg43827hnfdsfai"

def get(endpoint):
    response = requests.get(base_url+endpoint, cookies={"key":sec_key})
    if response.status_code != 200:
        return response.text
    return response.text


def post(endpoint, data):
    response = requests.post(base_url+endpoint, cookies={"key":sec_key}, json=data)
    if response.status_code != 200:
        return response.text
    return response.text

def put(endpoint, data):
    response = requests.put(base_url+endpoint, cookies={"key":sec_key}, json=data)
    if response.status_code != 200:
        return response.text
    return response.text

def upload_jpeg(endpoint, file_path):
    fileDataBinary = open(file_path, 'rb').read()
    files = {'uploadFile': (file_path, fileDataBinary, 'image/jpeg')}

    url = base_url+endpoint
    response = requests.post(url, cookies={"key":sec_key}, files=files)    
    return response.text

def json_print(caption, json_str):
    data = json.loads(str(json_str))
    print(caption)
    print(json.dumps(data, indent=2))

json_print("post",post("messages", {"to":"someone","content":"hello"}))
json_print("post",post("messages", {"to":"hogesan","content":"hello"}))
json_print("get by dst", get("messages/to/hogesan"))
json_print("put", put("messages/2", {"content":"updated","priority":2}))
json_print("updload", upload_jpeg("jpeg", "test.jpg"))

print(post("users", {"name":"hogesan","tickets":"3"}))
print(post("users", {"name":"asan"}))
print(put("users/2",{"status":"busy"}))
