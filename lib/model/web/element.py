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

def cyoa_reply_button(id, is_op=False, is_valid=True, theme='btn-primary', op_theme='btn-warning', invalid_theme='btn-secondary'):
    rtheme = theme
    if is_op: rtheme = op_theme
    if not is_valid: rtheme = invalid_theme
    return f'<div class="control-group-round btn-reply"><button class="btn {rtheme}">&gt;&gt;{id}</button><a href="#p{id}" class="btn {rtheme}">#</a></div>'