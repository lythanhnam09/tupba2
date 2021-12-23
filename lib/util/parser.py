import re
import lib.model.web.element as element
# from lib.model.cyoa.post import PostReplyTo, PostReplyBy

class RegexParser:
    def __init__(self, name, regex):
        self.name = name
        self.regex = regex
        self.result = []
    
    def to_format(self, text:str) -> str:
        temp = text
        res = re.findall(self.regex, text, re.MULTILINE)
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
        regex = r"^\s?>>>/(\w+)/"
        super().__init__(name, regex)

    def replace_format(self, result:list, text:str) -> str:
        for x in result:
            text = text.replace(f'>>>{x}', f'[{self.name}]({x})', 1)
        return text

    def replace_html(self, result:list, text:str) -> str:
        for x in result:
            text = text.replace(f'[{self.name}]({x})', f'<span class="board-link">&gt;&gt;&gt;/{x}/</span>', 1)
        return text

class ReplyParser(RegexParser):
    def __init__(self, name, post):
        regex = r">>([0-9]+)"
        super().__init__(name, regex)
        self.post = post
        self.ls_rep = []

    def replace_format(self, result:list, text:str) -> str:
        ls_id = [int(x) for x in result]
        self.post.add_replies(ls_id)
        self.ls_rep = self.post['reply_to']
        for x in result:
            text = text = text.replace(f'>>{x}', f'[{self.name}]({x})', 1)
        return text

    def replace_html(self, result:list, text:str) -> str:
        for rep in self.ls_rep:
            text = text.replace(f'[{self.name}]({rep["reply_id"]})', element.cyoa_reply_button(rep["reply_id"], is_op=rep['reply']['is_qm'] == 1), 1)
        return text

class QuoteParser(RegexParser):
    def __init__(self, name):
        regex = r"^\s?>(.*)"
        super().__init__(name, regex)

    def replace_format(self, result:list, text:str) -> str:
        for x in result:
            text = text = text.replace(f'>{x}', f'[{self.name}]({x})', 1)
        return text

    def replace_html(self, result:list, text:str) -> str:
        for x in result:
            text = text.replace(f'[{self.name}]({x})', f'<span class="quote">&gt;{x}</span>', 1)
        return text

class SpoilerParser(RegexParser):
    def __init__(self, name):
        regex = r"\[spoiler\](.*)\[/spoiler\]"
        super().__init__(name, regex)

    def replace_format(self, result:list, text:str) -> str:
        for x in result:
            text = text = text.replace(f'[spoiler]{x}[/spoiler]', f'[{self.name}]({x})', 1)
        return text

    def replace_html(self, result:list, text:str) -> str:
        for x in result:
            text = text.replace(f'[{self.name}]({x})', f'<span class="spoiler">{x}</span>', 1)
        return text

class BoldParser(RegexParser):
    def __init__(self, name):
        regex = r"\[b\]([.\n]*)\[/b\]"
        super().__init__(name, regex)

    def replace_format(self, result:list, text:str) -> str:
        for x in result:
            text = text = text.replace(f'[b]{x}[/b]', f'[{self.name}]({x})', 1)
        return text

    def replace_html(self, result:list, text:str) -> str:
        for x in result:
            text = text.replace(f'[{self.name}]({x})', f'<b>{x}</b>', 1)
        return text

class PostProcessor:
    def __init__(self, text, post):
        self.text = text
        self.parsers = [
            LinkParser('link'),
            BoardLinkParser('board'),
            ReplyParser('reply', post),
            QuoteParser('quote'),
            SpoilerParser('spoiler'),
            BoldParser('b')
        ]

    def process(self):
        for p in self.parsers:
            self.text = p.to_format(self.text)
        for p in self.parsers:
            self.text = p.to_html(self.text)

        self.text = self.text.replace('\n', '<br>')
        return self.text