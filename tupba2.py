from flask import *
import os
import sqlite3
import lib.route.socket as socket
import lib.util.db_util as db_util
from lib.util.util import *
from lib.route.cyoa import cyoa
from lib.route.booru import booru
from lib.model.web.navbar import NavOption, NavButton
from lib.route.socket import app, socketio
from lib.model.booru.config import booru_config

#app.config['UPLOAD_FOLDER'] = 'upload'

#app.register_blueprint(rewatch)
#app.register_blueprint(booru)
app.register_blueprint(cyoa, url_prefix='/cyoa')
app.register_blueprint(booru, url_prefix='/booru')

#@app.errorhandler(404)
#def page_not_found(e):
    #return render_template('error_404.html'), 404

#@app.route('/favicon.ico')
#def favicon():
    #return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

#@app.route('/api/test1')
#@cross_origin(supports_credentials=True)
#def api_test1():
    #return jsonify(message='Tesing ting number 1 (No delay)')

@app.route('/')
def root():
    #name = request.args.get('name', 'anon', type=str)
    return serve_template('index.mako', nav=NavOption('TUPBA II - the second', theme='nav-primary'))

@app.route('/sockettest')
def sockettest():
    return serve_template('cyoa/socket.html')

@app.route('/csstest')
def csstest():
    #name = request.args.get('name', 'anon', type=str)
    return serve_template('test.html')

@app.route('/preloader')
def preloader_test():
    #name = request.args.get('name', 'anon', type=str)
    return serve_template('test_preloader.mako', nav=NavOption('Preloader test', theme='nav-danger'))

@app.route('/testjmobile')
def jmobile_test():
    return serve_template('test_jmobile.mako', nav=NavOption('Touch gesture test', theme='nav-danger'))

def init():
    print('Root dir:', app.root_path)
    print('Static dir:', app.static_folder)
    print('Static path:', app.static_url_path)
    if (not check_file_exists('data/cyoa.db')):
        print('Creating cyoa.db')
        try:
            db_util.db_exec_script('data/cyoa.db', 'data/script/cyoa.sql')
        except sqlite3.OperationalError as e:
            print(e)
            os.system('rm -f data/cyoa.db')
            raise Exception('Can not create database cyoa.db')
    if (not check_file_exists('data/booru.db')):
        print('Creating booru.db')
        try:
            db_util.db_exec_script('data/booru.db', 'data/script/booru.sql')
        except sqlite3.OperationalError as e:
            print(e)
            os.system('rm -f data/booru.db')
            raise Exception('Can not create database booru.db')
    print('Current database file size:')
    print(f' - cyoa.db: {get_file_size_str("data/cyoa.db")}')
    print(f' - booru.db: {get_file_size_str("data/booru.db")}')

if __name__ == '__main__':
    init()
    #app.run(host='0.0.0.0', port=8080, debug=True)
    socketio.run(app, host='0.0.0.0', port=8080, debug=True)
