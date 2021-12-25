from lib.model.web.element import WebElement, fa_icon

class NavOption:
    def __init__(self, title:str = 'TUPBA II', title_link:str = None, theme:str = 'nav-primary', show_menu_button = True, left_buttons:list = [], right_buttons:list = [], title_size:str = None, show_progress = False):
        self.left_buttons = left_buttons
        self.right_buttons = right_buttons
        self.show_menu_button = show_menu_button
        self.theme = theme
        self.title = title
        self.title_link = title_link
        self.title_size = title_size
        self.show_progress = show_progress

    def show_prop(self, name, value):
        return f'{name}={value}' if (value != None) else ''

    def show_title_href(self):
        return self.show_prop('href', self.title_link)

class NavElement:
    def __init__(self, text, on_click, id):
        self.on_click = on_click
        self.text = text
        self.id = id

    def add_prop(self, props, name, value, disabled = False):
        if (not disabled and value != None): props[name] = value
    
    def html(self):
        return WebElement(
            'span', {}, [
                'Sample text'
            ]
        ).markup()

class NavButton(NavElement):
    def __init__(self, text:str = 'Button', icon:str = 'fa-menu', icon_only = True, on_click:str = None, href:str = None, disabled = False, id:str = None):
        super().__init__(text, on_click, id)
        self.href = href
        self.icon = icon
        self.icon_only = icon_only
        self.disabled = disabled

    def get_style_class(self) -> str:
        return 'nav-item px-2' + (' disabled' if self.disabled else '')

    def html(self):
        props = {'class': self.get_style_class(), 'title': self.text}
        self.add_prop(props, 'href', self.href, self.disabled)
        self.add_prop(props, 'onclick', self.on_click, self.disabled)
        self.add_prop(props, 'id', self.id)
        return WebElement(
            'a', props, [
                fa_icon(self.icon),
                f'<div class="text">{self.text}</div>'
            ]
        ).markup()

class NavLabel(NavElement):
    def __init__(self, text:str = 'Label', on_click:str = None, id = None, disabled = False):
        super().__init__(text, on_click, id)
        self.disabled = disabled

    def html(self):
        props = {'class': 'nav-title nav-title-xsm-center', 'title': self.text}
        self.add_prop(props, 'onclick', self.on_click, self.disabled)
        self.add_prop(props, 'id', self.id)
        return WebElement(
            'a', props, [
                self.text
            ]
        ).markup()
