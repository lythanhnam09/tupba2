from flask import *
from flask_socketio import emit, SocketIO
from flask_cors import CORS, cross_origin
import lib.util.task_util as task_util
import logging


log = logging.getLogger('werkzeug')
log.setLevel(logging.WARNING)

app = Flask('__main__')
CORS(app, support_credentials=True)
socketio = SocketIO(app)

def send_task_update():
    emit('task_data', task_util.get_queue_stat())

@socketio.on('task_stat')
def socket_name(data):
    #print('socket: task_stat')
    res = task_util.get_queue_stat()
    #print(f'socket: task_data {res}')
    emit('task_data', res)

task_util.task_queue.on_task_update = send_task_update

@socketio.on('name')
def socket_name(data):
    print(f'Message {data = }')
    emit('response', {'data': f'Hi {data["name"]} from the server'})
