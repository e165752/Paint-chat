from flask import Blueprint, jsonify, request, make_response, abort, send_file
import urllib.parse
import werkzeug
import os

from DB.models import *
from DB import db

chat_api = Blueprint('uiuxchat3287bivsgfbivf', __name__, url_prefix='/uiuxchat3287bivsgfbivf')
SECRET_KEY = "gfg43827hnfdsfai"

JPG_DIR = "jpg/"

session = None
def create_db_session():
    global session
    session = db.session()

def protected():
    key = request.cookies.get('key', "no key")
    print(key)
    if key != SECRET_KEY:
        abort(403, {'code': 'Forbidden', 'message': 'invalid access key'})

def succeed(contents):
    ret = {"result":contents}
    return jsonify(ret)

@chat_api.route('/', methods=['GET'])
def hello():
    key = request.cookies.get('key', "no key")
    return "hello_uiux:key:" + key

@chat_api.route('/<string:app_name>/jpeg/<string:file_id>', methods=['GET'])
def download_jpg(app_name, file_id):

    downloadFile = JPG_DIR + file_id
    downloadFileName = file_id + '.jpg'
    try:
        return send_file(downloadFile, as_attachment = False, \
            attachment_filename = downloadFileName, \
            mimetype = 'image/jpeg')
    except FileNotFoundError:
        abort(404, {'code': 'Not found', 'message': 'jpeg not found'})
        

@chat_api.route('/<string:app_name>/jpeg', methods=['POST'])
def upload_multipart(app_name):
    protected()
    if 'uploadFile' not in request.files:
        abort(400, {'code': 'bad request', 'message': 'uploadFile required'})

    file = request.files['uploadFile']
    fileName = file.filename
    if '' == fileName:
        make_response(jsonify({'result':'filename must not empty.'}))

    saveFileName = app_name + "_" + datetime.now().strftime("%Y%m%d_%H%M%S_") \
        + urllib.parse.quote(fileName)
    saveFileName = saveFileName.replace('/','_')
    file.save(os.path.join(JPG_DIR, saveFileName))

    return succeed({'file_id':saveFileName})


@chat_api.route('/<string:app_name>/messages', methods=['GET'])
def get_messages(app_name):
    messages = session.query(Message).filter(Message.app==app_name).all()
    if not messages:
        abort(404, {'code': 'Not found', 'message': 'message not found'})

    return succeed(messages)

@chat_api.route('/<string:app_name>/messages/<int:mid>', methods=['GET'])
def get_message_by_id(app_name, mid=None):
    messages = session.query(Message).filter_by(id=mid).first()
    if not messages:
        abort(404, {'code': 'Not found', 'message': 'message not found by id'+str(mid)})

    return succeed(messages)

@chat_api.route('/<string:app>/messages/to/<string:to>', methods=['GET'])
def get_messages_to(app, to=None):
    messages = session.query(Message).filter(Message.app==app, Message.to_==to).all()
    if not messages:
        abort(404, {'code': 'Not found', 'message': 'message not found'})
    return succeed(messages)

@chat_api.route('/<string:app>/messages/from/<string:from_>/to/<string:to_>', methods=['GET'])
def get_messages_from_to(app, to=None):
    messages = session.query(Message).filter(Message.app==app, Message.from_ == from_, Message.to_==to_).all()
    if not messages:
        abort(404, {'code': 'Not found', 'message': 'message not found'})
    return succeed(messages)

@chat_api.route('/<string:app>/messages/after/<string:time>', methods=['GET'])
def get_messages_after(app, time=None):
    try:
        dt = datetime.strptime(time,'%Y-%m-%d_%H:%M:%S')
    except ValueError as err:
        return abort(404, str(err))
    messages = session.query(Message).filter(Message.app == app, Message.timestamp > dt).all()

    return succeed(messages)

def get_message_params(app, message):
    payload = request.json
    message.app = app

    if payload.get('from'):
        message.from_ = payload.get('from')
    if payload.get('to'):
        message.to_ = payload.get('to')
    if payload.get('content'):
        message.content = payload.get('content')
    if payload.get('priority'):
        message.priority = payload.get('priority')
    if payload.get('timestamp'):
        message.timestamp = payload.get('timestamp')
    if payload.get('parent'):
        message.parent = payload.get('parent')

@chat_api.route('/<string:app>/messages', methods=['POST'])
def send_message(app):
    protected()
    message = Message()

    get_message_params(app, message)
    
    session.add(message)
    session.commit()

    return succeed({"id":message.id})

@chat_api.route('/<string:app>/messages/<int:message_id>', methods=['PUT'])
def update_message(app, message_id):
    protected()
    message = session.query(Message).filter(Message.app==app,Message.id==message_id).first()
    if not message:
        abort(404, {'code': 'Not found', 'message': 'message not found by id'+str(message_id)})

    get_message_params(app,message)
    session.commit()

    return succeed({"id":message.id})



def get_user_params(app, user):
    payload = request.json
    user.app = app
    if payload.get('name'):
        user.name = payload.get('name')
    if payload.get('status'):
        user.status = payload.get('status')
    if payload.get('tickets'):
        user.tickets = payload.get('tickets')


@chat_api.route('/<string:app>/users', methods=['POST'])
def add_user(app):
    user = UserInfo()

    get_user_params(app, user)
    
    session.add(user)
    session.commit()

    return succeed({"id":user.id})

@chat_api.route('/<string:app>/users', methods=['GET'])
def get_users(app):
    users = session.query(UserInfo).filter(UserInfo.app == app).all()
    if not users:
        abort(404, {'code': 'Not found', 'message': 'users not found'})

    return succeed(users)

@chat_api.route('/<string:app>/users/<int:user_id>', methods=['GET'])
def get_user_by_id(app, user_id=None):
    user = session.query(UserInfo).filter_by(id=user_id).first()
    if not user:
        abort(404, {'code': 'Not found', 'message': 'user not found'})

    return succeed(user)

@chat_api.route('/<string:app>/users/<int:uid>', methods=['PUT'])
def update_user(app, uid):
    user = session.query(UserInfo).filter(UserInfo.app==app, UserInfo.id==uid).first()
    if not user:
        abort(404, {'code': 'Not found', 'message': 'user not found'})

    get_user_params(app, user)
    session.commit()

    return succeed({"id":user.id})


@chat_api.route('/post', methods=['POST'])
def post_test():
    payload = request.json

    return succeed({"json":payload})
