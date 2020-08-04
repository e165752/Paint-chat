from flask import Flask, Blueprint, jsonify, url_for
import sqlite3
from models import *
import db
import api
import os
import sys
import werkzeug

app = Flask(__name__)
app.register_blueprint(api.chat_api)
 
@app.route('/hello', methods=['GET'])
def hello():
    return "hello"

# limit upload file size : 1MB
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024
@app.errorhandler(werkzeug.exceptions.RequestEntityTooLarge)
def handle_over_max_file_size(error):
    print("werkzeug.exceptions.RequestEntityTooLarge")
    return jsonify({'error': error.description}), 413


@app.errorhandler(404)
def page_not_found(error):
    print(error.description)
    return jsonify({'error': error.description}), 404

@app.errorhandler(403)
def forbidden(error):
    print(error.description)
    return jsonify({'error': error.description}), 403

@app.errorhandler(413)
def payload_too_large(error):
    print(error.description)
    return jsonify({'error': error.description}), 413

@app.errorhandler(500)
def internal_error(error):
    print(error.description)
    return jsonify({'error': error.description}), 500

def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)

def site_map():
    print("end points are:")
    links = []
    for rule in app.url_map.iter_rules():
        # Filter out rules we can't navigate to in a browser
        # and rules that require parameters
        print(rule.endpoint)
        # if "GET" in rule.methods and has_no_empty_params(rule):
        #     url = url_for(rule.endpoint, **(rule.defaults or {}))
        #     links.append((url, rule.endpoint))

def daemonize():
    pid = os.fork()
    if pid > 0:
        pid_file = open('python_flask.pid','w')
        pid_file.write(str(pid)+"\n")
        pid_file.close()
        sys.exit()
    if pid == 0:
        api.create_db_session()
        app.run(host='0.0.0.0',port=5111, debug=False)
if __name__ == '__main__':
    site_map()
    daemonize()
    #app.run(host='0.0.0.0',port=5111, debug=True)
