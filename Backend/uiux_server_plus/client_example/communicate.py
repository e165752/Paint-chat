import requests
import json

base_url = ''
sec_key = ''

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
    return data


def init_client():
    with open('config.json', 'r') as cfg_f:
        cfg_data = json.load(cfg_f)
        print('cfg_data \n', json.dumps(cfg_data, indent=2))
    
    # base_URI = cfg_data['base_uri']    # to リモート サーバー
    base_URI = cfg_data['base_uri-local_test']    # to local サーバー
    # app_name = cfg_data['app-0']
    app_name = cfg_data['app-1']
    base_url = base_URI + app_name  # URLを作成。
    if base_url[-1] is not '/':
        base_url = base_url + '/'
    sec_key = cfg_data['sec_key']
    return base_url, sec_key


if __name__ == "__main__":
    ## secret key などを読み込み。
    base_url, sec_key = init_client()
    print('base_url : ', base_url, '\nsec_key : ', sec_key)
    
    json_print("post", post("messages", {"to":"hogesan","content":"hello"}))
    json_print("get by dst", get("messages/to/hogesan"))
    json_print("put", put("messages/32", {"content":"updated"}))
    json_data = json_print("updload", upload("jpeg", "canvas.jpg", 'image/jpeg'))  ## .jpg 画像を送信する。（普段はコメントアウト）
    get("jpeg/"+json_data["result"]["file_id"])

    # print(post("users", {"name":"hogesan","tickets":"3"}))
    # print(post("users", {"name":"asan"}))
    # print(put("users/2",{"status":"busy"}))


