import lib.util.util as util
import lib.model.cyoa.cyoa as cyoa
import lib.model.cyoa.cyoa_thread as cyoa_thread
import lib.model.cyoa.post as cyoa_post
import lib.model.cyoa.cyoa_tag as tag
import lib.util.task_util as task_util
import lib.util.db_util as db_util


def image_link(filename:str) -> str:
    return f'https://img.anonpone.com/image/{filename[:2]}/{filename}'

def refresh_cyoa_list():
    link = 'https://www.anonpone.com/api/cyoa'
    js = util.get_json_api(link)
    result = []

    for k in js:
        cy = cyoa.Cyoa.from_json(js[k])
        lst = tag.Tag.save_from_name_list(js[k]['_tags'])
        lsct = [tag.CyoaTag(row=(cy['id'], t['id'])) for t in lst]
        tag.CyoaTag.insert(lsct, or_ignore=True)
        result.append(cy)
    cyoa.Cyoa.insert(result, update_conflict=True, set_col=cyoa.Cyoa.get_props_name(no_id=True, blacklist=['image_path', 'save_status']))
    return result

def refresh_thread_post(cy:cyoa.Cyoa = None, th:cyoa_thread.Thread = None):
    print(f'{th["id"]=} {cy["id"]=}')
    # print(f'{cy=}')
    link_anon = f'https://www.anonpone.com/api/thread/{cy["id"]}/{th["id"]}/false'
    link_desu = f'https://desuarchive.org/_/api/chan/thread/?board={th["board"]}&num={th["id"]}'
    try:
        anon_js = util.get_json_api(link_anon)
        if (th['chan'] == '4chan'): desu_js = util.get_json_api(link_desu)
        else: desu_js = {}
    except Exception as e:
        print('Fetch url error: ' + e)
        return
    
    lsimg = []
    ls_post = []
    index = 0
    for p in anon_js:
        js_ap = anon_js[p]
        # print(f'{js_ap=}')
        post = cyoa_post.Post.from_json(js_ap)
        if (js_ap['_filename'] not in [None, '', '0']):
            img = cyoa_post.PostImage.from_json(js_ap)
            if (js_ap['_lewd'] == '1' and (js_ap['_filenameLewd'] == '' or js_ap['_filenameLewd'] == None)):
                img['alt_id'] = 1
                img['alt_name'] = 'Lewd'
            lsimg.append(img)
        # Yeah... I have no idea why this site api being so retarded (sometime null, sometime '0', '' and probally more)
        if (js_ap['_lewd'] == '1' and (js_ap['_filenameLewd'] not in [None, '', '0'])):
            img = cyoa_post.PostImage.from_lewd_json(js_ap)
            lsimg.append(img)
        
        if (index == 0):
            post['title'] = th['title']
            if ((str(th['id']) in desu_js) and th['chan'] == '4chan' and th['board'] == 'mlp'):
                js_dp = desu_js[f'{th["id"]}']['op']
                post['comment_plain'] = js_dp['comment_sanitized']
                if (js_dp['media'] != None):
                    img = cyoa_post.PostImage.from_desu_json(js_dp)
                    if (js_ap['_filename'] not in [None, '', '0']):
                        img['link'] = image_link(js_ap['_filename'])
                    lsimg.append(img)
        else:
            if ((str(th['id']) in desu_js) and th['chan'] == '4chan' and th['board'] == 'mlp'):
                if (str(post['id']) in desu_js[f'{th["id"]}']['posts']):
                    js_dp = desu_js[f'{th["id"]}']['posts'][f'{post["id"]}']
                    post['comment_plain'] = js_dp['comment_sanitized']
                    if (js_dp['media'] != None):
                        img = cyoa_post.PostImage.from_desu_json(js_dp)
                        if (js_ap['_filename'] not in [None, '', '0']):
                            img['link'] = image_link(js_ap['_filename'])
                        lsimg.append(img)
        ls_post.append(post)
        index += 1
    th['thread_image'] = image_link(lsimg[0]['link'])
    th['total_post'] = len(ls_post)
    th['op_name'] = ls_post[0]['username']
    cyoa_post.Post.insert(ls_post, update_conflict=True, set_col=['comment_plain', 'comment_html'])
    cyoa_post.PostImage.insert(lsimg, update_conflict=True, set_col=['filename', 'link'])
    cyoa_thread.Thread.update(th, set_col=['thread_image', 'total_post', 'op_name'])

def parse_thread_post(cy:cyoa.Cyoa = None, th:cyoa_thread.Thread = None):
    ls_post = th['posts']
    for post in ls_post:
        post.process_html()
    cyoa_post.Post.update(ls_post, set_col=['comment_html'])

def refresh_thread_list(cy:cyoa.Cyoa, refresh_post = True, force_refresh_all = False, reparse_post = False):
    link = f'https://www.anonpone.com/api/threads/{cy["id"]}'
    js = util.get_json_api(link)
    result = []
    lsct = []
    for k in js:
        # print(f'{js[k] = }')
        cth = cyoa_thread.Thread.from_json(js[k])
        result.append(cth)
        lsct.append(cyoa_thread.CyoaThread(row=(cy['id'], cth['id'])))
    cyoa_thread.Thread.insert(result, update_conflict=True, set_col=cyoa_thread.Thread.get_props_name(no_id=True, blacklist=['thread_image', 'op_name', 'total_op_post', 'total_post']))
    cyoa_thread.CyoaThread.insert(lsct, or_ignore=True)
    if (refresh_post):
        if (force_refresh_all):
            qw = task_util.QueueWorker(name=f'Delete all thread data: {cy["name"]}', limit=1, dequeue_on_done = True, meta={'id':cy['short_name'], 'category':'CYOA', 'short_name': cy['short_name'], 'cyoa_id': cy['id'], 'operation': 'delete-thread'})
            for th in result:
                qw.enqueue(task_util.WorkerTask(cyoa_post.Post.delete, None, where=[['thread_id', th['id']]]))
            task_util.task_queue.enqueue(qw)

            qw = task_util.QueueWorker(name=f'Refresh thread data: {cy["name"]}', dequeue_on_done = True, meta={'id':cy['short_name'], 'category':'CYOA', 'short_name': cy['short_name'], 'cyoa_id': cy['id'], 'operation': 'get-thread'})
            for th in result:
                qw.enqueue(task_util.WorkerTask(refresh_thread_post, None, cy=cy, th=th))
            task_util.task_queue.enqueue(qw)

            qw = task_util.QueueWorker(name=f'Parsing posts: {cy["name"]}', dequeue_on_done = True, meta={'id':cy['short_name'], 'category':'CYOA', 'short_name': cy['short_name'], 'cyoa_id': cy['id'], 'operation': 'parse-post'})
            for th in result:
                qw.enqueue(task_util.WorkerTask(parse_thread_post, None, cy=cy, th=th))
            task_util.task_queue.enqueue(qw)
        elif (reparse_post):
            qw = task_util.QueueWorker(name=f'Parsing posts: {cy["name"]}', dequeue_on_done = True, meta={'id':cy['short_name'], 'category':'CYOA', 'short_name': cy['short_name'], 'cyoa_id': cy['id'], 'operation': 'parse-post'})
            for th in result:
                qw.enqueue(task_util.WorkerTask(parse_thread_post, None, cy=cy, th=th))
            task_util.task_queue.enqueue(qw)
        else:
            ls_emty = cy.get_list_emty()
            if (len(ls_emty) > 0):
                print(f'refresh_thread_list: {len(ls_emty)} threads have no post, begin worker task')
                qw = task_util.QueueWorker(name=f'Refresh thread data: {cy["name"]}', dequeue_on_done = True, meta={'id':cy['short_name'], 'category':'CYOA', 'short_name': cy['short_name'], 'cyoa_id': cy['id'], 'operation': 'get-thread'})
                for th in ls_emty:
                    qw.enqueue(task_util.WorkerTask(refresh_thread_post, None, cy=cy, th=th))
                task_util.task_queue.enqueue(qw)

                qw = task_util.QueueWorker(name=f'Parsing posts: {cy["name"]}', dequeue_on_done = True, meta={'id':cy['short_name'], 'category':'CYOA', 'short_name': cy['short_name'], 'cyoa_id': cy['id'], 'operation': 'parse-post'})
                for th in ls_emty:
                    qw.enqueue(task_util.WorkerTask(parse_thread_post, None, cy=cy, th=th))
                task_util.task_queue.enqueue(qw)
            else:
                th = cy.get_ref_one('threads', order_by=['thread_date', 'desc'])['thread']
                qw = task_util.QueueWorker(name=f'Refresh last thread data: {cy["name"]}', dequeue_on_done = True, meta={'id':cy['short_name'], 'category':'CYOA', 'short_name': cy['short_name'], 'cyoa_id': cy['id'], 'operation': 'get-thread'})
                qw.enqueue(task_util.WorkerTask(refresh_thread_post, None, cy=cy, th=th))
                task_util.task_queue.enqueue(qw)

                qw = task_util.QueueWorker(name=f'Parsing posts: {cy["name"]}', dequeue_on_done = True, meta={'id':cy['short_name'], 'category':'CYOA', 'short_name': cy['short_name'], 'cyoa_id': cy['id'], 'operation': 'parse-post'})
                qw.enqueue(task_util.WorkerTask(parse_thread_post, None, cy=cy, th=th))
                task_util.task_queue.enqueue(qw)
    return result

def get_cyoa_list(q:str = '', page = 1, per_page = 20, order_by:list = ['last_post_time', 'desc'], refresh = False) -> list:
    if (refresh):
        refresh_cyoa_list()
    if (order_by[0] == 'ratio'):
        result = cyoa.Cyoa.filter_tags(q, page, per_page, order_by=[['(cast(total_image as real) / total_post)', order_by[1]], ['total_image', order_by[1]]])
    else:
        result = cyoa.Cyoa.filter_tags(q, page, per_page, order_by=order_by)
    for cy in result.data:
        cy.check_steath_lewd()
    return result

def get_thread_list(cyoa:cyoa.Cyoa, page = 1, per_page = 0, refresh = False):
    if (refresh):
        refresh_cyoa_list()
    return cyoa.get_ref_page('threads', page, per_page, order_by=['thread_date', 'asc'], get_many=True)

def get_post_list(cyoa:cyoa.Cyoa , thread:cyoa_thread.Thread, refresh = False):
    if (refresh):
        refresh_thread_post(cyoa, thread)
    return thread.get_ref('posts', save_result=True)
    
