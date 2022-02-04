import re
import lib.model.web.element as element
import lib.util.util as util
import lib.util.db_util as db_util
import sqlite3

class Parser:
    def __init__(self, name):
        self.name = name
        self.result = []
    
    def to_format(self, text:str) -> str:
        return text

    def to_html(self, text:str) -> str:
        return text

class TagParser(Parser):
    def __init__(self, tagname, replace = '<{0}>', end_tag = '{0}'):
        super().__init__(tagname)
        self.tagname = tagname
        self.replace = replace
        self.end_tag = end_tag

    def to_format(self, text:str) -> str:
        return text

    def to_html(self, text:str) -> str:
        text = text.replace(f'[{self.tagname}]', self.replace.format(self.tagname))
        text = text.replace(f'[/{self.tagname}]', f'</{self.end_tag.format(self.tagname)}>')
        return text

class RegexParser:
    def __init__(self, name, regex, option = re.MULTILINE):
        self.name = name
        self.regex = regex
        self.option = option
        self.result = []
    
    def to_format(self, text:str) -> str:
        temp = text
        res = re.findall(self.regex, text, self.option)
        if (len(res) > 0):
            self.result = res
            return self.replace_format(res, temp)
        else:
            return text

    def replace_format(self, result:list, text:str) -> str:
        return text

    def to_html(self, text:str) -> str:
        temp = text
        res = re.findall(f'\[{self.name}\]\((.*)\)', text, re.MULTILINE)
        if (len(res) > 0):
            return self.replace_html(res, temp)
        else:
            return text

    def replace_html(self, result:list, text:str) -> str:
        return text

class Link:
    def __init__(self, protocol, host, port, path):
        self.protocol = protocol
        self.host = host
        self.port = port
        self.path = path

    def strip_query(self):
        qpos = self.path.rfind('?')
        if (qpos != -1):
            return f'{self.protocol}://{self.host}{self.port}{self.path[:qpos]}'
        return f'{self.protocol}://{self.host}{self.port}{self.path}'

    def get_file_ext(self):
        extpos = self.path.rfind('.')
        if (extpos != -1):
            qpos = self.path.rfind('?')
            if (qpos != -1):
                return self.path[extpos + 1:qpos].lower()
            return self.path[extpos + 1:].lower()
        return None

    def get_filename(self):
        qpos = self.path.rfind('?')
        if (qpos != -1):
            return self.path[self.path.rfind('/') + 1:qpos]
        return self.path[self.path.rfind('/')]

    def __str__(self):
        return f'{self.protocol}://{self.host}{self.port}{self.path}'

    def __repr__(self):
        return f'Link({self.protocol}://{self.host}{self.port}{self.path})'


class LinkParser(RegexParser):
    def __init__(self, name):
        self.regex = r"(http|ftp|https)://([\w_-]+(?:(?:\.[\w_-]+)+))(:\d+)?([\w.,@?^=%&:/+#-]*[\w@?^=%&/+#-])?"
        super().__init__(name, self.regex)
        self.links = []

    def to_format(self, text:str) -> str:
        temp = text
        res = re.findall(self.regex, text, self.option)
        if (len(res) > 0):
            self.result = res
            self.links = [Link(x[0], x[1], x[2], x[3]) for x in self.result]
            return self.replace_format(res, temp)
        else:
            return text
    
    def replace_format(self, result:list, text:str) -> str:
        for x in self.links:
            text = text.replace(str(x), f'[{self.name}]({x!s})', 1)
        return text

    def replace_html(self, result:list, text:str) -> str:
        for x in result:
            url = x
            text = text.replace(f'[{self.name}]({url})', f'<a href="{url}">{url}</a>', 1)
        return text

class ImgurLinkParser(LinkParser):
    def __init__(self, name, post):
        super().__init__(name)
        self.regex = r"(http|ftp|https)://(imgur.com)(:\d+)?([\w.,@?^=%&:/+#-]*[\w@?^=%&/+#-])"
        self.post = post
    
    def replace_format(self, result:list, text:str) -> str:
        from lib.model.cyoa.post import PostImage

        conn = sqlite3.connect(PostImage._dbfile)
        max_alt = db_util.db_get_single_cell(conn, 'select max(alt_id) from post_image where post_id = ?', (self.post['id'], )) or 2
        alt_index = max(max_alt + 1, 2)
        index = 1
        lsimg = []
        for x in self.links:
            print(f'ImgurLinkParser: [#{self.post["id"]}] found {x!s}')
            if (x.path.startswith('/a/')):
                id = x.path[3:]
                js = util.get_json_api(f'https://api.imgur.com/post/v1/albums/{id}?client_id=546c25a59c58ad7&include=media')
                if ('media' not in js): continue
                for jsimg in js['media']:
                    print(f'ImgurLinkParser: [#{self.post["id"]}] <{id}> found {jsimg["url"]}')
                    i = PostImage.select_one([['post_id', self.post['id']], ['link', jsimg['url']]], conn = conn)
                    if (i != None):
                        print(f'ImgurLinkParser: [#{self.post["id"]}] <{id}> Ignored duplicate {jsimg["url"]}')
                        continue
                    img = PostImage(data={
                        'post_id': self.post['id'],
                        'alt_id': alt_index,
                        'alt_name': f'Imgur {index}',
                        'filename': jsimg['name'],
                        'link': jsimg['url'],
                        'offline_link': None,
                        'status_code': 0
                    })
                    lsimg.append(img)
                    alt_index += 1
                    index += 1
            else:
                id = x.path[1:]
                js = util.get_json_api(f'https://api.imgur.com/post/v1/media/{id}?client_id=546c25a59c58ad7&include=media')
                if ('media' not in js): continue
                print(f'ImgurLinkParser: [#{self.post["id"]}] <{id}> found {js["media"][0]["url"]}')
                i = PostImage.select_one([['post_id', self.post['id']], ['link', js['media'][0]['url']]], conn = conn)
                if (i != None):
                    print(f'ImgurLinkParser: [#{self.post["id"]}] <{id}> Ignored duplicate {js["media"][0]["url"]}')
                    continue
                img = PostImage(data={
                    'post_id': self.post['id'],
                    'alt_id': alt_index,
                    'alt_name': f'Imgur {index}',
                    'filename': js['media'][0]['name'],
                    'link': js['media'][0]['url'],
                    'offline_link': None,
                    'status_code': 0
                })
                lsimg.append(img)
                alt_index += 1
                index += 1
        if (len(lsimg) > 0): PostImage.insert(lsimg, True, conn = conn)
        conn.close()

        return text

class MediaLinkParser(LinkParser):
    def __init__(self, name, post):
        super().__init__(name)
        self.post = post
    
    def replace_format(self, result:list, text:str) -> str:
        from lib.model.cyoa.post import PostImage

        conn = sqlite3.connect(PostImage._dbfile)
        max_alt = db_util.db_get_single_cell(conn, 'select max(alt_id) from post_image where post_id = ?', (self.post['id'], )) or 1
        alt_index = max(max_alt + 1, 2)
        index = 1
        lsimg = []
        for x in self.links:
            ext = x.get_file_ext()
            if (ext != None and ext in ['webm', 'gif', 'png', 'jpg', 'jpeg', 'webp', 'mp4']):
                filename = x.get_filename()
                link = x.strip_query()
                print(f'MediaLinkParser: [#{self.post["id"]}] found {link}')
                i = PostImage.select_one([['post_id', self.post['id']], ['link', link]], conn = conn)
                if (i != None):
                    print(f'MediaLinkParser: [#{self.post["id"]}] Ignored duplicate {link}')
                    continue
                img = PostImage(data={
                    'post_id': self.post['id'],
                    'alt_id': alt_index,
                    'alt_name': f'Link {index}',
                    'filename': filename,
                    'link': link,
                    'offline_link': None,
                    'status_code': 0
                })
                lsimg.append(img)
                alt_index += 1
                index += 1
        if (len(lsimg) > 0): PostImage.insert(lsimg, True, conn = conn)
        conn.close()

        return text

class BoardLinkParser(RegexParser):
    def __init__(self, name):
        regex = r"^\s?&gt;&gt;&gt;/(\w+)/"
        super().__init__(name, regex)

    def replace_format(self, result:list, text:str) -> str:
        for x in result:
            text = text.replace(f'&gt;&gt;&gt;{x}', f'[{self.name}]({x})', 1)
        return text

    def replace_html(self, result:list, text:str) -> str:
        for x in result:
            text = text.replace(f'[{self.name}]({x})', f'<span class="board-link">&gt;&gt;&gt;/{x}/</span>', 1)
        return text

class ReplyParser(RegexParser):
    def __init__(self, name, post):
        regex = r"&gt;&gt;([0-9]+)"
        super().__init__(name, regex, 0)
        self.post = post
        self.ls_rep = []

    def replace_format(self, result:list, text:str) -> str:
        ls_id = [int(x) for x in result]
        self.post.add_replies(ls_id)
        self.ls_rep = self.post.get_ref('reply_to')
        for p in self.ls_rep:
            text = text.replace(f'&gt;&gt;{p["reply_id"]}', f'[{self.name}]({p["reply_id"]})')
            ls_id.remove(p['reply_id'])
        for p in ls_id:
            text = text.replace(f'&gt;&gt;{p}', element.cyoa_reply_button(p, is_valid=False))
        return text

    def replace_html(self, result:list, text:str) -> str:
        for p in self.ls_rep:
            text = text.replace(f'[{self.name}]({p["reply_id"]})', element.cyoa_reply_button(p['reply_id'], is_op=p['reply']['is_qm'] == 1))
        return text

class QuoteParser(RegexParser):
    def __init__(self, name):
        regex = r"^\s?&gt;(.*)"
        super().__init__(name, regex)

    def replace_format(self, result:list, text:str) -> str:
        for x in result:
            text = text.replace(f'&gt;{x}', f'[{self.name}]({x})', 1)
        return text

    def replace_html(self, result:list, text:str) -> str:
        for x in result:
            text = text.replace(f'[{self.name}]({x})', f'<span class="quote">&gt;{x}</span>', 1)
        return text


class PostProcessor:
    def __init__(self, text, post):
        self.text = text
        self.post = post
        self.parsers = [
            MediaLinkParser('link', post),
            ImgurLinkParser('link', post),
            LinkParser('link'),
            BoardLinkParser('board'),
            ReplyParser('reply', post),
            QuoteParser('quote'),
            TagParser('spoiler', '<span class="{0}">', 'span'),
            TagParser('b')
        ]

    def process(self):
        self.text = self.text.replace('>', '&gt;')
        self.text = self.text.replace('<', '&lt;')
        self.text = self.text.replace('\n\n\n', '\n\n')

        for p in self.parsers:
            self.text = p.to_format(self.text)
        for p in self.parsers:
            self.text = p.to_html(self.text)

        self.text = self.text.replace('\n', '<br>')
        return self.text