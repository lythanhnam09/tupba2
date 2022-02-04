import lib.util.util as util
import lib.model.cyoa.cyoa as cyoa
import lib.model.cyoa.cyoa_thread as cyoa_thread
import lib.model.cyoa.post as cyoa_post
import lib.model.cyoa.fanart as fanart
import lib.model.cyoa.cyoa_tag as tag
import lib.util.task_util as task_util
import lib.util.db_util as db_util
import re
import asyncio
import sqlite3


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
    conn = db_util.make_conn(cyoa.Cyoa._dbfile)
    cyoa_post.Post.insert(ls_post, update_conflict=True, set_col=['comment_plain', 'comment_html'], conn=conn)
    cyoa_post.PostImage.insert(lsimg, update_conflict=True, set_col=['filename', 'link'], conn=conn)
    cyoa_thread.Thread.update(th, set_col=['thread_image', 'total_post', 'op_name'], conn=conn)
    conn.close()

def parse_thread(id:int):
    th = cyoa_thread.Thread.find_id(id)
    if (th == None): return False
    ls_post = th['posts']
    for post in ls_post:
        post.process_html()
    cyoa_post.Post.update(ls_post, set_col=['comment_html'])
    threadpost_loader.clear_data()
    return True

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
    conn = db_util.make_conn(cyoa_thread.CyoaThread._dbfile)
    cyoa_thread.Thread.insert(result, update_conflict=True, set_col=cyoa_thread.Thread.get_props_name(no_id=True, blacklist=['thread_image', 'op_name', 'total_op_post', 'total_post']), conn=conn)
    cyoa_thread.CyoaThread.insert(lsct, or_ignore=True, conn=conn)
    conn.close()
    threadpost_loader.clear_data()
    if (refresh_post):
        if (force_refresh_all):
            wk = task_util.TaskWorker(f'Refresh cyoa thread data (force): {cy["name"]}', meta={'id':cy['short_name'], 'category':'CYOA', 'short_name': cy['short_name'], 'cyoa_id': cy['id']})
            delete_task = task_util.Task.from_single_item(f'Delete all thread data', cy.delete_all_thread)
            wk.add(delete_task)

            refresh_task = task_util.Task('Refresh thread data')
            for th in result:
                refresh_task.add(task_util.TaskItem(refresh_thread_post, cy, th))
            wk.add(refresh_task)

            parse_task = task_util.Task('Parsing post')
            for th in result:
                parse_task.add(task_util.TaskItem(parse_thread_post, cy, th))
            wk.add(parse_task)

            task_util.worker_queue.add(wk)
        elif (reparse_post):
            wk = task_util.TaskWorker(f'Reparsing cyoa post: {cy["name"]}', meta={'id':cy['short_name'], 'category':'CYOA', 'short_name': cy['short_name'], 'cyoa_id': cy['id']})
            parse_task = task_util.Task('Parsing post')
            for th in result:
                parse_task.add(task_util.TaskItem(parse_thread_post, cy, th))
            wk.add(parse_task)

            task_util.worker_queue.add(wk)
        else:
            ls_emty = cy.get_list_emty()
            if (len(ls_emty) > 0):
                wk = task_util.TaskWorker(f'Refresh cyoa thread data: {cy["name"]}', meta={'id':cy['short_name'], 'category':'CYOA', 'short_name': cy['short_name'], 'cyoa_id': cy['id']})
                print(f'refresh_thread_list: {len(ls_emty)} threads have no post, begin worker task')
                refresh_task = task_util.Task('Refresh thread data')
                for th in ls_emty:
                    refresh_task.add(task_util.TaskItem(refresh_thread_post, cy, th))
                wk.add(refresh_task)

                parse_task = task_util.Task('Parsing post')
                for th in ls_emty:
                    parse_task.add(task_util.TaskItem(parse_thread_post, cy, th))
                wk.add(parse_task)

                task_util.worker_queue.add(wk)
            else:
                th = cy.get_ref_one('threads', order_by=['thread_date', 'desc'])['thread']
                wk = task_util.TaskWorker(f'Refresh last thread data: {cy["name"]}', meta={'id':cy['short_name'], 'category':'CYOA', 'short_name': cy['short_name'], 'cyoa_id': cy['id']})
                
                task_refresh = task_util.Task.from_single_item('Refresh last thread data', refresh_thread_post, cy=cy, th=th)
                wk.add(task_refresh)

                task_parse = task_util.Task.from_single_item('Parsing posts', parse_thread_post, cy=cy, th=th)
                wk.add(task_parse)

                task_util.worker_queue.add(wk)
    return result

def get_cyoa_list(q:str = '', page = 1, per_page = 20, order_by:list = ['last_post_time', 'desc'], refresh = False) -> list:
    if (refresh):
        refresh_cyoa_list()
    conn = db_util.make_conn(cyoa.Cyoa._dbfile)
    if (order_by[0] == 'ratio'):
        result = cyoa.Cyoa.filter_tags(q, page, per_page, order_by=[['(cast(total_image as real) / total_post)', order_by[1]], ['total_image', order_by[1]]], conn=conn)
    else:
        result = cyoa.Cyoa.filter_tags(q, page, per_page, order_by=order_by, conn=conn)
    for cy in result.data:
        cy.check_steath_lewd(conn=conn)
    conn.close()
    return result

def get_thread_list(cyoa:cyoa.Cyoa, page = 1, per_page = 0, refresh = False):
    if (refresh):
        refresh_cyoa_list()
    return cyoa.get_ref_page('threads', page, per_page, order_by=['thread_date', 'asc'], get_many=True)

def get_post_list(cyoa:cyoa.Cyoa , thread:cyoa_thread.Thread, refresh = False):
    if (refresh):
        refresh_thread_post(cyoa, thread)
    return thread.get_ref('posts', save_result=True)

def get_cyoa_image(cyoa:cyoa.Cyoa, query, page = 1, perpage = 40):
    is_qm = None
    alt_id = None
    alt_op = None
    thread = None
    offline = False
    if (query.strip(' ') != ''):
        lsq = [x.strip(' ') for x in query.strip(' ').split(',')]
        print(f'{lsq=}')
        
        for q in lsq:
            lsop = list(re.findall('(\w+)([:<>=~][>=]?)(\(?[\d;]+\)?)', q)[0])
            if (lsop[0] == 'is_qm'):
                is_qm = int(lsop[2])
            if (lsop[0] == 'alt_id'):
                alt_id = lsop[2]
                alt_op = lsop[1].replace('~', 'in')
                alt_id = alt_id.replace(';', ',')
            if (lsop[0] == 'offline'):
                offline = lsop[1] != '0'
            if (lsop[0] == 'thread'):
                thread = int(lsop[2]).split(';')
    
    return cyoa.get_image_list(is_qm, alt_id, alt_op, thread, offline, page, perpage)

def refresh_cyoa_fanart(cyoa:cyoa.Cyoa):
    link = f'https://www.anonpone.com/api/fanart/{cyoa["id"]}'
    js = util.get_json_api(link)

    ls = []

    for rimg in js:
        fimg = fanart.Fanart.from_json(rimg)
        ls.append(fimg)
    
    fanart.Fanart.insert(ls, or_ignore=True)

def get_cyoa_fanart(cyoa:cyoa.Cyoa, page = 1, per_page = 40):
    return cyoa.get_ref_page('fanarts', page, per_page, save_result=True)


class CyoaImageLoader(task_util.PagePreLoader):
    def __init__(self):
        super().__init__()
        self.query = ''
        self.cyoa = None

    def check_page_loaded(self, page):
        for pg in self.page_data.data:
            if (page == pg.page_num): return pg
        return None

    async def do_request(self, page):
        # print(f'CyoaImageLoader: Loading page {page}')
        pg = self.check_page_loaded(page)
        if (pg == None):
            pg = await self.get_cyoa_image_async(self.cyoa, self.query, page, self.per_page)
            self.receive_data(pg)
            # print(f'CyoaImageLoader: Page {page} loaded')
            return pg
        # print(f'CyoaImageLoader: Page {page} loaded from cache')
        return pg

    async def get(self, cyoa, query, page, per_page):
        # print(f'CyoaImageLoader: Requesting page {page}')
        if (self.cyoa == None or self.cyoa['id'] != cyoa['id'] or self.query != query or self.per_page != per_page):
            # print(f'CyoaImageLoader: Different data, clear cache')
            self.cyoa = cyoa
            self.query = query
            self.per_page = per_page
            self.page_data.data.clear()
        self.page = page

        result = await self.do_request(page)
        for i in range(1,self.range + 1):
            if (self.page + 1 <= self.page_count): asyncio.create_task(self.do_request(self.page + 1))
            if (self.page - 1 >= 1): asyncio.create_task(self.do_request(self.page - 1))
        return result
    
    async def get_cyoa_image_async(self, cyoa:cyoa.Cyoa, query, page = 1, perpage = 40):
        is_qm = None
        alt_id = None
        alt_op = None
        thread = None
        offline = False
        if (query.strip(' ') != ''):
            lsq = [x.strip(' ') for x in query.strip(' ').split(',')]
            
            for q in lsq:
                lsop = list(re.findall('(\w+)([:<>=~][>=]?)(\(?[\d;]+\)?)', q)[0])
                if (lsop[0] == 'is_qm'):
                    is_qm = int(lsop[2])
                if (lsop[0] == 'alt_id'):
                    alt_id = lsop[2]
                    alt_op = lsop[1].replace('~', 'in')
                    alt_id = alt_id.replace(';', ',')
                if (lsop[0] == 'offline'):
                    offline = lsop[1] != '0'
                if (lsop[0] == 'thread'):
                    thread = int(lsop[2]).split(';')
        
        return cyoa.get_image_list(is_qm, alt_id, alt_op, thread, offline, page, perpage)

class ThreadPostLoader():
    def __init__(self, range = 1, cache = 4):
        self.thread_num = 0
        self.thread_count = 0
        self.cyoa = None
        self.range = range
        self.cache = cache
        self.thread_data = task_util.DQueue()

    def check_page_loaded(self, thread):
        for th in self.thread_data.data:
            if (thread['id'] == th['id']): return th
        return None

    async def do_request(self, thread):
        # print(f'CyoaImageLoader: Loading page {page}')
        # print(f'{thread=}')
        th = self.check_page_loaded(thread)
        if (th == None):
            th = await self.get_thread_posts(thread)
            self.receive_data(th)
            # print(f'CyoaImageLoader: Page {page} loaded')
            return th
        # print(f'CyoaImageLoader: Page {page} loaded from cache')
        return th

    def receive_data(self, thread):
        self.thread_data.enqueue(thread)
        self.thread_data.limit(self.cache)

    def clear_data(self):
        self.thread_data.data.clear()

    async def get(self, cyoa, thread, num=None, count=None):
        # print(f'CyoaImageLoader: Requesting page {page}')
        if (self.cyoa == None or self.cyoa['id'] != cyoa['id']):
            # print(f'CyoaImageLoader: Different data, clear cache')
            self.cyoa = cyoa
            self.thread_data.data.clear()
        self.thread_num = num
        self.thread_count = count

        result = await self.do_request(thread)
        for i in range(1,self.range + 1):
            if (num + 1 < count): asyncio.create_task(self.do_request(self.cyoa['threads'][num + 1]))
            if (num - 1 >= 0): asyncio.create_task(self.do_request(self.cyoa['threads'][num - 1]))
        return result
    
    async def get_thread_posts(self, thread):
        conn = sqlite3.connect(cyoa.Thread._dbfile)
        thread.get_ref('posts', save_result=True, conn=conn)
        for post in thread['posts']:
            post.get_ref('images', save_result=True, conn=conn)
            post.get_ref('reply_by', save_result=True, conn=conn)
        conn.close()
        return thread

img_loader = CyoaImageLoader()
threadpost_loader = ThreadPostLoader()