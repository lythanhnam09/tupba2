import lib.util.util as util
import lib.util.task_util as task_util
import lib.util.booru_util as booru_util
from lib.model.booru.image import *
from lib.model.booru.tag import *
from lib.model.booru.filter import *
from lib.model.booru.album import *
from lib.model.booru.feed import *
from lib.model.booru.config import booru_config
from lib.util.sql_table import ResultPage
import asyncio
import math
import sqlite3

class BooruSearchPreloader(task_util.Preloader):
    def __init__(self, range:int = 1, cache:int = 4):
        super().__init__(range, cache)
        self.meta = {
            'perpage': 20,
            'pagecount': 1, 
            'sf': 'id', 
            'sd':'desc',
            'q': '*'
        }

    # need override
    def is_loaded(self, page, enum) -> bool:
        return page.page_num == enum and page.per_page == self.meta['perpage']

    # optional override
    def on_receive_data(self, data):
        super().on_receive_data(data)
        self.meta['pagecount'] = data.page_count

    # need override
    def do_next(self, enum, i):
        self.do_request(enum + i) 
    
    # need override
    def do_previous(self, enum, i):
        self.do_request(enum - i) 
    
    # need override
    def has_next(self, enum, i):
        return enum + i <= self.meta['pagecount']

    # need override
    def has_previous(self, enum, i):
        return enum - i >= 1

    # optional override
    def is_meta_diff(self, mt):
        tmpmt = self.meta.copy()
        if ('pagecount' in tmpmt): tmpmt.pop('pagecount')
        return tmpmt != mt

    # need override (the main funtion to run)
    def run_request(self, enum):
        booru_config.ensure_loaded()
        link = f'https://derpibooru.org/api/v1/json/search/images?q={self.meta["q"]}&filter_id={booru_config.data["booru_filter_id"]}&page={enum}&per_page={self.meta["perpage"]}&sf={self.meta["sf"]}&sd={self.meta["sd"]}'
        print(link)
        js = util.get_json_api(link)
        page_count = math.ceil(js['total'] / self.meta['perpage']) if self.meta['perpage'] > 0 and math.ceil(js['total'] / self.meta['perpage']) > 0 else 1
        page_data = ResultPage(enum, page_count, self.meta['perpage'], js['total'], [])
        lssz = []
        lstagimg = []
        conn = sqlite3.connect(BooruImage._dbfile)
        for jsimg in js['images']:
            img = BooruImage.from_json(jsimg)
            for sname in jsimg['representations']:
                sz = BooruImageSize.from_key_pair(sname, jsimg['representations'][sname], jsimg['id'], jsimg['format'])
                lssz.append(sz)
            for jstag in jsimg['tags']:
                tag = BooruTag.from_name(jstag)
                tag = BooruTag.find_or_insert(tag, where=[['name', jstag]], conn=conn)
                lstagimg.append(BooruImageTag(row=(jsimg['id'], tag['id'])))

            page_data.data.append(img)
        BooruImage.insert(page_data.data, update_conflict=True, set_col=['upvote', 'downvote', 'score', 'fave', 'comment_count', 'wilson_score', 'link_source', 'updated_at', 'description', 'delete_reason', 'thumbnail_generated', 'duration'], conn=conn)
        BooruImageSize.insert(lssz, or_ignore=True, conn=conn)
        BooruImageTag.insert(lstagimg, or_ignore=True, conn=conn)

        for img in page_data.data:
            img.get_ref('tags', order_by=['sort_index', 'asc'], save_result=True, conn=conn)
            img.get_ref('sizes', order_by=['size_index', 'asc'], save_result=True, conn=conn)

        conn.close()

        return page_data

search_loader = BooruSearchPreloader(range=1)

def get_search(q = '', sf = 'id', sd = 'asc', page = 1, perpage = 20, preload = True):
    booru_config.ensure_loaded()
    qp = booru_util.QueryProcessor()
    qp.set_query(q)
    qp.set_filters(booru_config.filters)
    img_page = search_loader.do_get(page, {'q':qp.export_query(), 'sf':sf, 'sd':sd, 'perpage':perpage}, preload_other=preload)
    for img in img_page.data:
        qp.apply_spoiler(img)
    return img_page

def get_image_by_id(id, refresh = False):
    conn = sqlite3.connect(BooruImage._dbfile)
    img = BooruImage.find_id(id, conn=conn)
    if (img == None or refresh):
        link = f'https://derpibooru.org/api/v1/json/images/{id}'
        try:
            js = util.get_json_api(link)
        except Exception as e:
            print(f'Image id {id} not found')
            return None
        jsimg = js['image']
        img = BooruImage.from_json(jsimg)
        lssz = []
        lstagimg = []
        for sname in jsimg['representations']:
            sz = BooruImageSize.from_key_pair(sname, jsimg['representations'][sname], jsimg['id'], jsimg['format'])
            lssz.append(sz)
        for jstag in jsimg['tags']:
            tag = BooruTag.from_name(jstag)
            tag = BooruTag.find_or_insert(tag, where=[['name', jstag]], conn=conn)
            lstagimg.append(BooruImageTag(row=(jsimg['id'], tag['id'])))
        BooruImage.insert(img, update_conflict=True, set_col=['upvote', 'downvote', 'score', 'fave', 'comment_count', 'wilson_score', 'link_source', 'updated_at', 'description', 'delete_reason', 'thumbnail_generated', 'duration'], conn=conn)
        BooruImageSize.insert(lssz, or_ignore=True, conn=conn)
        BooruImageTag.insert(lstagimg, or_ignore=True, conn=conn)

    img.get_ref('tags', order_by=[['sort_index', 'asc'], ['name', 'asc']], save_result=True, conn=conn)
    img.get_ref('sizes', order_by=['size_index', 'asc'], save_result=True, conn=conn)
    conn.close()
    return img

def get_main_page_indexed(limit = 15):
    booru_config.ensure_loaded()
    qp = booru_util.QueryProcessor()
    qp.set_filters(booru_config.filters)
    ls = BooruImage.select(order_by=['id', 'desc'], limit=limit)
    # for img in ls:
    #     qp.apply_spoiler(img)
    return ls

def get_filter_list():
    ls = BooruFilter.select(order_by=['sort_index', 'asc'])
    # print(booru_config)
    for f in ls:
        f.cols['checked'] = f['id'] in booru_config.data['filters']
    return ls

def add_pic_to_favorite(id):
    conn = sqlite3.connect(BooruAlbum._dbfile)
    album = BooruAlbum.select_one(where=[['name', 'Favorited']], conn=conn)
    if (album == None):
        album = BooruAlbum(data={'id': 0,'thumbnail_id': id,'name': 'Favorited','color': ''})
        album.cols['id'] = BooruAlbum.insert(album, conn=conn)
    max_sort = db_util.db_get_single_cell(conn, 'select max(sort_index) from album_image where album_id = ?', (album.cols['id'],))
    if (max_sort == None): max_sort = 0
    ali = BooruAlbumImage(data={'album_id': album.cols['id'],'image_id': id,'sort_index': max_sort + 1})
    BooruAlbumImage.insert(ali, or_ignore=True, conn=conn)
    conn.close()

def add_to_album(pid, aid, conn = None):
    if (conn == None): nconn = sqlite3.connect(BooruAlbum._dbfile)
    else: nconn = conn
    album = BooruAlbum.find_id(aid, conn=nconn)
    if (album == None): return False

    max_sort = db_util.db_get_single_cell(conn, 'select max(sort_index) from album_image where album_id = ?', (album.cols['id'],))
    if (max_sort == None): max_sort = 0
    ali = BooruAlbumImage(data={'album_id': aid,'image_id': pid,'sort_index': max_sort + 1})
    BooruAlbumImage.insert(ali, or_ignore=True, conn=nconn)

    if (conn == None): nconn.close()

def get_album_list(preload = True):
    conn = sqlite3.connect(BooruAlbum._dbfile)
    ls = BooruAlbum.select(conn=conn)
    for a in ls:
        if (preload):
            img = a.get_ref('thumbnail', save_result=True, conn=conn)
            if (img != None):
                img.get_ref('sizes', order_by=['size_index', 'asc'], save_result=True, conn=conn)
        a.get_ref_count('images', save_result=True, save_name='image_count', conn=conn)
    conn.close()
    return ls

def get_add_album_list(pid):
    conn = sqlite3.connect(BooruAlbum._dbfile)
    ls = BooruAlbum.select(conn=conn)
    for a in ls:
        a.get_ref_count('images', save_result=True, save_name='image_count', conn=conn)
        ali = BooruAlbumImage.find_id((a.cols['id'], pid))
        a.cols['is_added'] = (ali != None)
    conn.close()
    return ls

def get_album_image(album, page, perpage):
    conn = sqlite3.connect(BooruAlbum._dbfile)
    ls_img = album.get_ref_page('images', page, perpage, order_by=['sort_index', 'asc'], get_many=True, save_result=True)
    for img in ls_img.data:
        img.get_ref('sizes', order_by=['size_index', 'asc'], save_result=True, conn=conn)
        img.get_ref('tags', order_by=['sort_index', 'asc'], save_result=True, conn=conn)
        img.cols['spoiler_tag'] = ''
    conn.close()
    return ls_img

def add_album(name):
    album = BooruAlbum(data={'id': 0,'thumbnail_id': None,'name': name,'color': ''})
    BooruAlbum.insert(album)

def edit_album(id, name):
    album = BooruAlbum.find_id(id)
    if (album == None): return False
    album.cols['name'] = name
    BooruAlbum.update(album)
    return True

def add_to_albums(pid, lsid):
    conn = sqlite3.connect(BooruAlbum._dbfile)
    ls = []
    for aid in lsid:
        max_sort = db_util.db_get_single_cell(conn, 'select max(sort_index) from album_image where album_id = ?', (aid,))
        if (max_sort == None): max_sort = 0
        ali = BooruAlbumImage(data={'album_id': aid,'image_id': pid,'sort_index': max_sort + 1})
        ls.append(ali)
    BooruAlbumImage.insert(ls, or_ignore=True, conn=conn)
    conn.close()
