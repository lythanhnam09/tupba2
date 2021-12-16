

class NavOption:
    def __init__(self, title:str = 'TUPBA II', title_link:str = None, theme:str = 'nav-primary', show_menu_button = True, left_buttons:list = [], right_buttons:list = []):
        self.left_buttons = left_buttons
        self.right_buttons = right_buttons
        self.show_menu_button = show_menu_button
        self.theme = theme
        self.title = title
        self.title_link = title_link

    def show_prop(self, name, value):
        return f'{name}={value}' if (value != None) else ''

    def show_title_href(self):
        return self.show_prop('href', self.title_link)

class NavButton:
    def __init__(self, text:str = 'Button', icon:str = 'fas fa-menu', icon_only = True, on_click:str = None, href:str = None, id:str = None):
        self.href = href
        self.icon = icon
        self.icon_only = icon_only
        self.on_click = on_click
        self.text = text
        self.id = id

    def show_prop(self, name, value):
        return f'{name}={value}' if (value != None) else ''

    def show_href(self):
        return self.show_prop('href', self.href)

    def show_on_click(self):
        return self.show_prop('onclick', self.on_click)
