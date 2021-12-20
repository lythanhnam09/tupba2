from markupsafe import Markup

class WebElement:
    def __init__(self, tag:str, prop:dict = None, children:list = None):
        self.tag = tag
        self.prop = prop
        self.children = children

    def render_html(self):
        propstr = ' '.join([(f'{k}=\"{self.prop[k]}\"' if type(self.prop[k]) != bool else (k if self.prop[k] else '')) for k in self.prop if self.prop[k] != None])
        childstr = ' '.join([f'{o}' for o in self.children])
        return f'<{self.tag} {propstr}>{childstr}</{self.tag}>'

    def markup(self):
        return Markup(self.render_html())

    def __repr__(self):
        return f'WebElement({self.render_html()!r})'

    def __str__(self):
        return self.render_html()

    def __html__(self):
        return self.render_html()
    
def fa_icon(name, style='fas', extra_cls=''):
    return f'<i class="{style} fa-{name} {extra_cls}"></i>'