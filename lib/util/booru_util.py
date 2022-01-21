
# Everything filter: 56027

class QueryProcessor:
    def __init__(self):
        self.tags = {}
        self.filter_tags = {}
        self.filters = []
        self.ls_spoiler = set()

    def parse_query(self, q:str, ls:dict):
        if (q.strip(' ') == ''): return
        lsq = [s.strip(' ') for s in q.split(',')]
        ls_spoiler = {}
        for t in lsq:
            if t[0] in ['+', '-', '`']:
                tname = t[1:]
                if (t in ls):
                    if ls[tname] == '':
                        ls[tname] = t[0]
                else:
                    ls[tname] = t[0]
            else:
                ls[t] = ''

    def set_query(self, query_str):
        self.parse_query(query_str, self.tags)
        for t in self.tags:
            if (self.tags[t] == '`'):
                self.ls_spoiler.add(t)
    
    def add_filter(self, filter_str):
        self.parse_query(filter_str, self.filter_tags)

    def set_filters(self, ls_filter):
        ls_spoiler = []
        self.filters = ls_filter
        for f in ls_filter:
            self.add_filter(f.cols['filter_text'])
            ls_spoiler += f.cols['spoilers']
        self.ls_spoiler |= set(ls_spoiler)

    def to_booru_query(self, ls:dict, include_spoiler = False):
        lst = [ls[k] + k for k in ls if (include_spoiler or ls[k] != '`')]
        return ','.join(lst)

    def export_query(self, include_spoiler = False):
        tmp_f = self.filter_tags.copy()
        tmp_tag = self.tags.copy()
        for t in tmp_tag:
            if (t in tmp_f): tmp_f.pop(t)
        result = []
        
        if (len(tmp_f.keys()) > 0): result.append(f'({self.to_booru_query(tmp_f, include_spoiler)})')
        if (len(tmp_tag.keys()) > 0): result.append(f'({self.to_booru_query(tmp_tag, include_spoiler)})')
        if (len(result) == 0): return '*'

        return ', '.join(result)

    def apply_spoiler(self, img, col_name = 'spoiler_tag'):
        ls_stag = []
        ls_tag = img['tags']
        for tag in ls_tag:
            tname = tag['tag']['name']
            if (tname in self.ls_spoiler): ls_stag.append(tname)
        img.cols[col_name] = ', '.join(ls_stag)
        return img