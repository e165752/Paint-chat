import requests
import json

# base_url = "http://db.denchu.cloud:5111/uiuxchat3287bivsgfbivf/test2/"
base_url = "http://db.denchu.cloud:5111/uiuxchat3287bivsgfbivf/dotsubos-test/"
#test2はapp名. app名は任意です
#uiuxchat3287bivsgfbivfは変更できません．セキュリティのため公開しないでください
sec_key = "gfg43827hnfdsfai"

def get(endpoint):
    print()
    response = requests.get(base_url+endpoint, cookies={"key":sec_key})
    print(response.url)
    return response.text

def post(endpoint, data):
    print()
    response = requests.post(base_url+endpoint, cookies={"key":sec_key}, json=data)
    return response.text

def put(endpoint, data):
    print()
    response = requests.put(base_url+endpoint, cookies={"key":sec_key}, json=data)
    return response.text

def upload(endpoint, file_path, mimetype):
    print()
    fileDataBinary = open(file_path, 'rb').read()
    files = {'uploadFile': (file_path, fileDataBinary, mimetype)}

    url = base_url+endpoint
    response = requests.post(url, cookies={"key":sec_key}, files=files)    
    return response.text

def json_print(caption, json_str):
    data = json.loads(str(json_str))
    print(caption)
    print(json.dumps(data, indent=2))



if __name__ == "__main__":    
    json_print("get", post("messages", {"to":"someone","content":"hello"}))
    json_print("get", post("messages", {"to":"hogesan","content":"hello"}))
    json_print("get by dst", get("messages/to/hogesan"))
    json_print("put", put("messages/32", {"content":"updated"}))
    # json_print("updload", upload("jpeg", "canvas.jpg", 'image/jpeg'))   ## .jpg 画像を送信する。（普段はコメントアウト）
    get("jpeg/dotsubos-test_20200802_232627_canvas.jpg")

    # print(post("users", {"name":"hogesan","tickets":"3"}))
    # print(post("users", {"name":"asan"}))
    # print(put("users/2",{"status":"busy"}))


