from flask import *
from flask_socketio import emit, SocketIO
# from flask_cors import CORS, cross_origin
import lib.util.task_util as task_util
import lib.util.util as util
import logging
import lib.provider.anonpone as anonpone
import lib.provider.derpibooru as derpibooru
import lib.model.cyoa.cyoa as cyoa
import lib.model.booru.tag as btag
import lib.model.booru.filter as bfilter
import lib.model.booru.album as balbum
from lib.model.booru.config import booru_config


log = logging.getLogger('werkzeug')
log.setLevel(logging.WARNING)

app = Flask('__main__')
# CORS(app, support_credentials=True)
socketio = SocketIO(app)

# booru_config.load()

@socketio.on('task_stat')
def task_update(data = {}):
    #print('socket: task_stat')
    res = task_util.get_queue_stat()
    #print(f'socket: task_data {res}')
    emit('task_data', res)

    @copy_current_request_context
    def update_task(worker, task_item, result):
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
        
    task_util.worker_queue.on_task_update.append(update_task)
    task_util.worker_queue.on_worker_done.append(done_task)
    task_util.worker_queue.on_worker_error.append(error_task)

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
    print(f'socketio: Refresh CYOA Threads data ({data})')
    cy = cyoa.Cyoa.find_id(data['id'])
    @copy_current_request_context
    def update_task(worker, task_item, result):
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
        print(f'Worker {worker.name!r} throw an exception: {e}')
        print(trace)
        emit('task_data', task_util.get_queue_stat())
        # emit('throw_error', {'exception': f'{e}', 'trace': trace, 'name': worker.name})
        emit('show_error',  {'message': f'Worker {worker.name!r} throw an exception: {e}'})
    if (cy != None):
        anonpone.refresh_thread_list(cy, force_refresh_all=data.get('force', False), reparse_post=data.get('parse', False))

        task_util.worker_queue.on_task_update.append(update_task)
        task_util.worker_queue.on_worker_done.append(done_task)
        task_util.worker_queue.on_worker_error.append(error_task)

        emit('task_data', task_util.get_queue_stat())
    else:
        emit('show_error',  {'message': f'Cyoa id {data["id"]} not found'})

@socketio.on('cyoa_thread_reparse')
def cyoa_thread_reparse(data):
    print(f'socketio: Reparse CYOA thread {data["id"]} posts')
    res = anonpone.parse_thread(data['id'])
    print('Done')
    if (res): emit('refresh_page', {'context': None})

@socketio.on('cyoa_image_data')
def get_image_page(data):
    print(f'socketio: Get CYOA image data {data=}')
    cy = cyoa.Cyoa.find_id(data['cyoaId'])
    if (cy == None):
        return {'error':'Not found'}
    # page = await anonpone.img_loader.get(cy, data['q'], data['page'], data['perpage'])
    page = anonpone.get_cyoa_image(cy, data['q'], data['page'], data['perpage'])
    return util.to_json_str(page)

@socketio.on('cyoa_fanart_data')
def get_image_page(data):
    print(f'socketio: Get CYOA fanart data {data=}')
    cy = cyoa.Cyoa.find_id(data['cyoaId'])
    if (cy == None):
        return {'error':'Not found'}
    # page = await anonpone.img_loader.get(cy, data['q'], data['page'], data['perpage'])
    page = anonpone.get_cyoa_fanart(cy, data['page'], data['perpage'])
    return util.to_json_str(page)

@socketio.on('cyoa_fanart_refresh')
def cyoa_refresh(data):
    print(f'socketio: Refresh CYOA fanart {data=}')
    cy = cyoa.Cyoa.find_id(data['id'])
    if (cy == None):
        return {'error':'Not found'}
    anonpone.refresh_cyoa_fanart(cy)
    emit('refresh_page', {'context': f'/cyoa/quest/{cy["short_name"]}/fanarts'})

@socketio.on('search_tag')
def search_tag(data):
    ls_tag = btag.BooruTag.select(where=[['name', 'like', f'%{data["name"]}%']], order_by=['name', 'asc'], limit=20)
    return util.to_json_str(ls_tag)

@socketio.on('new_filter')
def new_filter(data):
    print(f'socketio: Create new filter {data=}')
    bfilter.BooruFilter.add_filter(data['name'], data['text'])
    emit('refresh_page', {'context': '/booru/filters'})

@socketio.on('edit_filter')
def edit_filter(data):
    print(f'socketio: Edit filter {data=}')
    ft = bfilter.BooruFilter.find_id(data['id'])
    if (ft == None): return
    ft.update_filter(data['name'], data['text'])
    booru_config.update_filter()
    emit('refresh_page', {'context': '/booru/filters'})

@socketio.on('swap_filter')
def swap_filter(data):
    print(f'socketio: Swap filter {data=}')
    bfilter.BooruFilter.swap_filter_order(data['id1'], data['id2'])
    emit('refresh_page', {'context': '/booru/filters'})

@socketio.on('delete_filter')
def delete_filter(data):
    print(f'socketio: Delete filter {data=}')
    bfilter.BooruFilter.delete(where=[['id', data['id']]])
    emit('refresh_page', {'context': '/booru/filters'})

@socketio.on('save_filter')
def delete_filter(data):
    print(f'socketio: Save filter {data=}')
    booru_config.set_filters(data['filters'])
    emit('refresh_page', {'context': '/booru/filters'})

@socketio.on('fav_booru_pic')
def fav_booru_pic(data):
    print(f'socketio: Add booru pic to favorite {data=}')
    derpibooru.add_pic_to_favorite(data['id'])
    # emit('refresh_page', {'context': '/booru/filters'})

@socketio.on('add_album_list')
def add_album_list(data):
    print(f'socketio: Get album list to add {data=}')
    ls = derpibooru.get_add_album_list(data['id'])
    return util.to_json_str(ls)

@socketio.on('add_album')
def add_album(data):
    print(f'socketio: Create new album {data=}')
    ls = derpibooru.add_album(data['name'])
    emit('refresh_page', {'context': '/booru/albums'})

@socketio.on('edit_album')
def add_album(data):
    print(f'socketio: Edit album {data=}')
    derpibooru.edit_album(data['id'], data['name'])
    emit('refresh_page', {'context': '/booru/albums'})

@socketio.on('add_to_albums')
def add_pic_to_albums(data):
    print(f'socketio: Add pic to albums {data=}')
    derpibooru.add_to_albums(data['pid'], data['lsid'])

@socketio.on('delete_album')
def delete_filter(data):
    print(f'socketio: Delete album {data=}')
    balbum.BooruAlbum.delete(where=[['id', data['id']]])
    emit('refresh_page', {'context': '/booru/albums'})