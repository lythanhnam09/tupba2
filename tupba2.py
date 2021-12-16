from flask import *
import os
import lib.route.socket as socket
import lib.util.db_util as db_util
from lib.util.util import *
from lib.route.cyoa import cyoa
from lib.model.web.navbar import NavOption, NavButton
from lib.route.socket import app, socketio

#app.config['UPLOAD_FOLDER'] = 'upload'

#app.register_blueprint(rewatch)
#app.register_blueprint(booru)
app.register_blueprint(cyoa, url_prefix='/cyoa')

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
    return render_template('index.html', nav=NavOption('TUPBA II - the second', theme='nav-primary'))

@app.route('/sockettest')
def sockettest():
    return render_template('cyoa/socket.html')

@app.route('/csstest')
def csstest():
    #name = request.args.get('name', 'anon', type=str)
    return render_template('test.html')

def init():
    print('Root dir:', app.root_path)
    print('Static dir:', app.static_folder)
    print('Static path:', app.static_url_path)
    if (not check_file_exists('data/cyoa.db')):
        print('Creating cyoa.db')
        db_util.db_exec_script('data/cyoa.db', 'data/script/cyoa.sql')

if __name__ == '__main__':
    init()
    #app.run(host='0.0.0.0', port=8080, debug=True)
    socketio.run(app, host='0.0.0.0', port=8080, debug=True)
