import urllib

class WebForm:
    def __init__(self, data:dict = None):
        if (data != None):
            self.param = data.copy()
        else:
            self.param = {}

    def __getitem__(self, key):
        return self.param[key]

    def __setitem__(self, key, value):
        self.param[key] = value

    def get_arg_value(self, request):
        for k in self.param:
            self.param[k] = request.get(k, self.param[k], type=type(self.param[k]))

    def option_selected(self, name, value):
        if (self.param[name] == value):
            return 'selected'
        return ''

    def get_form_query(self, set_value:dict = {}, blacklist:list = []):
        d = self.param.copy()
        for k in set_value:
            d[k] = set_value[k]
        for k in blacklist:
            d.pop(k)
        return urllib.parse.urlencode(d)