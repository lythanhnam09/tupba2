from flask import *
from flask_socketio import emit, SocketIO
from flask_cors import CORS, cross_origin
import lib.util.task_util as task_util
import lib.util.util as util
import logging
import lib.provider.anonpone as anonpone
import lib.model.cyoa.cyoa as cyoa


log = logging.getLogger('werkzeug')
log.setLevel(logging.WARNING)

app = Flask('__main__')
CORS(app, support_credentials=True)
socketio = SocketIO(app, async_mode="threading")

@socketio.on('task_stat')
def task_update(data = {}):
    #print('socket: task_stat')
    res = task_util.get_queue_stat()
    #print(f'socket: task_data {res}')
    emit('task_data', res)

    @copy_current_request_context
    def update_task(worker):
        emit('task_data', task_util.get_queue_stat())
    @copy_current_request_context
    def done_task(worker):
        cy = cyoa.Cyoa.find_id(worker.meta["cyoa_id"])
        cy['save_status'] = 1
        cyoa.Cyoa.update(cy, set_col=['save_status'])
        emit('task_data', task_util.get_queue_stat())
        emit('refresh_page', {'context': f'/cyoa/quest/{worker.meta["short_name"]}'})
    @copy_current_request_context
    def error_task(worker, e, trace):
        emit('task_data', task_util.get_queue_stat())
        emit('throw_error', {'exception': f'{e}', 'trace': trace, 'name': worker.name})
    task_util.task_queue.on_task_update = update_task
    task_util.task_queue.on_task_done = done_task
    task_util.task_queue.on_task_error = error_task

@socketio.on('name')
def socket_name(data):
    print(f'socketio: Message {data = }')
    emit('response', {'data': f'Hi {data["name"]} from the server'})

@socketio.on('cyoa_refresh')
def cyoa_refresh(data):
    print(f'socketio: Refresh CYOA data')
    anonpone.refresh_cyoa_list()
    emit('refresh_page', {'context': '/cyoa/'})

@socketio.on('cyoa_thread_refresh')
def cyoa_refresh_thread(data):
    print(f'socketio: Refresh CYOA Threads data')
    cy = cyoa.Cyoa.find_id(data['id'])
    @copy_current_request_context
    def update_task(worker):
        emit('task_data', task_util.get_queue_stat())
    @copy_current_request_context
    def done_task(worker):
        cy = cyoa.Cyoa.find_id(worker.meta["cyoa_id"])
        cy['save_status'] = 1
        cyoa.Cyoa.update(cy, set_col=['save_status'])
        emit('task_data', task_util.get_queue_stat())
        emit('refresh_page', {'context': f'/cyoa/quest/{worker.meta["short_name"]}'})
    @copy_current_request_context
    def error_task(worker, e, trace):
        emit('task_data', task_util.get_queue_stat())
        emit('throw_error', {'exception': f'{e}', 'trace': trace, 'name': worker.name})
    if (cy != None):
        anonpone.refresh_thread_list(cy, force_refresh_all=data.get('force', False), reparse_post=data.get('parse', False))
        # emit('refresh_page', {})
        task_util.task_queue.on_task_update = update_task
        task_util.task_queue.on_task_done = done_task
        task_util.task_queue.on_task_error = error_task
        emit('task_data', task_util.get_queue_stat())
    else:
        emit('show_error',  {'message': f'Cyoa id {data["id"]} not found'})

@socketio.on('cyoa_image_data')
def get_image_page(data):
    print(f'socketio: Get CYOA image data {data=}')
    cy = cyoa.Cyoa.find_id(data['cyoaId'])
    if (cy == None):
        return {'error':'Not found'}
    # page = await anonpone.img_loader.get(cy, data['q'], data['page'], data['perpage'])
    page = anonpone.get_cyoa_image(cy, data['q'], data['page'], data['perpage'])
    return util.to_json_str(page)
