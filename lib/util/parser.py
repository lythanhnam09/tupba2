import re
import lib.model.web.element as element
# from lib.model.cyoa.post import PostReplyTo, PostReplyBy

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

class LinkParser(RegexParser):
    def __init__(self, name):
        regex = r"(http|ftp|https)://([\w_-]+(?:(?:\.[\w_-]+)+))(:\d+)?([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?"
        super().__init__(name, regex)
    
    def replace_format(self, result:list, text:str) -> str:
        for x in result:
            url = f'{x[0]}://{x[1]}{x[2]}{x[3]}'
            text = text.replace(url, f'[{self.name}]({url})', 1)
        return text

    def replace_html(self, result:list, text:str) -> str:
        for x in result:
            url = x
            text = text.replace(f'[{self.name}]({url})', f'<a href="{url}">{url}</a>', 1)
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
            text = text.replace(f'&gt;&gt;{p}', element.cyoa_reply_button(p, is_valid=True))
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
            LinkParser('link'),
            BoardLinkParser('board'),
            ReplyParser('reply', post),
            QuoteParser('quote'),
            TagParser('spoiler', '<span class="{0}">', 'span'),
            TagParser('b')
        ]

    def process(self):
        self.text = self.text.replace('>', '&gt;')
        self.text = self.text.replace('\n\n\n', '\n\n')

        for p in self.parsers:
            self.text = p.to_format(self.text)
        for p in self.parsers:
            self.text = p.to_html(self.text)

        self.text = self.text.replace('\n', '<br>')
        return self.text