from lib.util.util import JsonConfig

class BooruConfig(JsonConfig):
    def __init__(self, path):
        super().__init__(path)
        self.data = {
            'filters': [],
            'booru_filter_id': 56027
        }

booru_config = BooruConfig('config/booru.json').load()
