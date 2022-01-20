from lib.util.util import JsonConfig
import lib.util.db_util as db_util
from lib.model.booru.filter import *

class BooruConfig(JsonConfig):
    def __init__(self, path):
        super().__init__(path)
        self.data = {
            'filters': [],
            'booru_filter_id': 56027
        }
        self.filters = []

    def update_filter(self):
        if (len(self.data["filters"]) <= 0): 
            self.filters.clear()
            return
        lsid = [str(x) for x in self.data["filters"]]
        lst = f'({",".join(lsid)})'
        self.filters = BooruFilter.select(where=[['id', 'in', [lst]]])

    def load(self):
        super().load()
        self.update_filter()
        return self

    def set_filters(self, ls:list):
        self.data['filters'] = ls
        self.update_filter()
        self.save()

booru_config = BooruConfig('config/booru.json')
