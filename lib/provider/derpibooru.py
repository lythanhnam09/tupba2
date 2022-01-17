import lib.util.util as util
import lib.util.task_util as task_util
import lib.util.booru_util as booru_util
from lib.model.booru.image import BooruImage, BooruImageSize
from lib.model.booru.tag import BooruTag, BooruImageTag
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
        # print(self.meta)

    # need override
    async def do_next(self, enum, i):
        await self.do_request(enum + i) 
    
    # need override
    async def do_previous(self, enum, i):
        await self.do_request(enum - i) 
    
    # need override
    def has_next(self, enum, i):
        # print(f'has next: {enum + i=} {self.meta["pagecount"]=} {(enum + i <= self.meta["pagecount"])=}')
        return enum + i <= self.meta['pagecount']

    # need override
    def has_previous(self, enum, i):
        # print(f'has prev: {enum - i=} {self.meta["pagecount"]=} {(enum + i <= self.meta["pagecount"])=}')
        return enum - i >= 1

    # optional override
    def is_meta_diff(self, mt):
        tmpmt = self.meta.copy()
        if ('pagecount' in tmpmt): tmpmt.pop('pagecount')
        return tmpmt != mt

    # need override (the main funtion to run)
    async def run_request(self, enum):
        qp = booru_util.QueryProcessor()
        qp.set_query(self.meta['q'])
        qp.add_filter('explicit, -anthro, -eqg, -equestria girls, -human, -humanized, -scat, -fart, -vore, -diaper,  -artist:pony_dreaming, -artist:wildviolet-m')
        link = f'https://derpibooru.org/api/v1/json/search/images?q={qp.export_query()}&filter_id={booru_config.data["booru_filter_id"]}&page={enum}&per_page={self.meta["perpage"]}&sf={self.meta["sf"]}&sd={self.meta["sd"]}'
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

    img.get_ref('tags', order_by=['sort_index', 'asc'], save_result=True, conn=conn)
    img.get_ref('sizes', order_by=['size_index', 'asc'], save_result=True, conn=conn)
    conn.close()
    return img