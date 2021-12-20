from markupsafe import Markup
from lib.model.web.element import WebElement, fa_icon

class Button():
    def __init__(self, tag_name = 'button', text = '0', disabled = False, id = None, on_click=None, href=None, style_cls='btn btn-primary'):
        self.tag_name = tag_name
        self.text = text
        self.disabled = disabled
        self.id = id
        self.on_click = on_click
        self.href = href
        self.style_cls = style_cls

    def html(self):
        return WebElement(self.tag_name, {'id': self.id, 'class': self.style_cls, 'href': self.href if (not self.disabled) else None, 'onclick': self.on_click if (not self.disabled) else None, 'disabled': self.disabled}, [self.text])

class SimplePageNav:
    def __init__(self, page_data, form_id, color='primary', extra_cls=''):
        self.page_data = page_data
        self.color = color
        self.extra_cls = extra_cls
        self.form_id = form_id
        self.button = []

        self.button.append(Button(text=fa_icon('chevron-double-left'), disabled=self.page_data.page_num <= 1, on_click=f'gotoPage(1, {self.form_id!r})', style_cls=f'btn btn-{self.color}'))
        self.button.append(Button(text=fa_icon('chevron-left'), disabled=self.page_data.page_num <= 1, on_click=f'gotoPage({self.page_data.page_num - 1}, {self.form_id!r})', style_cls=f'btn btn-{self.color}'))
        self.button.append(Button(text=f'Page {self.page_data.page_num} of {self.page_data.page_count}', on_click=f'showPageDialog({self.page_data.page_num}, {self.page_data.page_count}, {self.form_id!r})', style_cls=f'btn btn-{self.color}'))
        self.button.append(Button(text=fa_icon('chevron-right'), disabled=self.page_data.page_num >= self.page_data.page_count, on_click=f'gotoPage({self.page_data.page_num + 1}, {self.form_id!r})', style_cls=f'btn btn-{self.color}'))
        self.button.append(Button(text=fa_icon('chevron-double-right'), disabled=self.page_data.page_num >= self.page_data.page_count, on_click=f'gotoPage({self.page_data.page_count}, {self.form_id!r})', style_cls=f'btn btn-{self.color}'))
    
    def html(self):
        child = [x.html() for x in self.button]
        return WebElement('div', {'class': f'control-group-round {self.extra_cls}'}, child)
