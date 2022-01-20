import sqlite3
import json
from datetime import datetime, timedelta
# from urllib.request import Request, urlopen
import urllib3
from pathlib import Path
from mako.template import Template
from mako.lookup import TemplateLookup
import time


class Page:
    def __init__(self, current_page = 0, item_per_page = 1, page_count = 1, item_count = 1, data = []):
        self.current_page = current_page
        self.item_per_page = item_per_page
        self.page_count = page_count
        self.item_count = item_count
        self.data = data

def to_json_str(obj, indent:int = None):
    js = json.dumps(obj, default=lambda o: o.__dict__, indent=indent)
    return js

def from_json_str(txt):
    js = json.loads(txt)
    return js

def read_text_file_line(dir):
    with open(dir) as f:
        txt = f.readlines()
    return txt

def read_text_file(dir):
    with open(dir) as f:
        txt = f.read()
    return txt

def write_text_file(dir, txt):
    with open(dir, 'wt') as f:
        f.write(txt)

def write_json(dir:str, js):
    txt = to_json_str(js)
    write_text_file(dir, txt)

def read_json(dir:str):
    txt = read_text_file(dir)
    return from_json_str(txt)

def check_file_exists(path):
    return Path(path).exists()

def get_current_timestamp(delta = 0):
    return (datetime.now() + timedelta(hours=delta)).timestamp()

def parse_to_timestamp(date_str, format):
    date = datetime.strptime(date_str, format)
    return date.timestamp()

def date_str_from_timestamp(timestamp, format):
    date = datetime.fromtimestamp(timestamp)
    return date.strftime(format)

useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'

def get_json_api(link):
    http = urllib3.PoolManager(headers={'User-Agent': useragent})
    r = http.request('GET', link)
    js = json.loads(r.data.decode('utf-8'))
    return js

def download_file(link, path):
    http = urllib3.PoolManager(headers={'User-Agent': useragent})
    r = http.request('GET', link)
    res = r.data
    with open(path, 'wb') as f:
        f.write(res)

def get_file_size_str(path):
    sz = Path(path).stat().st_size
    return get_size_str(sz)

def get_size_str(num, round = 2, threshold = 1024):
    lsu = ['B', 'KB', 'MB', 'GB', 'TB']
    ui = 0
    while (num >= threshold) and (ui < len(lsu)):
        ui += 1
        num /= 1024
    return f'{num:.{round}f}{lsu[ui]}'

mylookup = TemplateLookup(directories=['template'], module_directory='tmp/mako_modules')

def serve_template(templatename, **kwargs):
    mytemplate = mylookup.get_template(templatename)
    return mytemplate.render(**kwargs)

class StopTimer:
    def __init__(self, name = 'Timer'):
        self.delta = 0
        self.name = name
        print(f'{self.name} started')
        self.start = time.perf_counter()

    def get(self):
        self.delta = time.perf_counter() - self.start
        return self.delta

    def measure(self):
        self.delta = time.perf_counter() - self.start
        print(f'{self.name} finnished in ({self.delta:.3f})')
        return self.delta
    
    def restart(self, name = None):
        self.delta = 0
        self.name = name or self.name
        print(f'{self.name} started')
        self.start = time.perf_counter()

class CallBackList(list):
    def fire(self, *args, **kwargs):
        for listener in self:
             listener(*args, **kwargs)

class Queue(list):
    def put(self, data):
        self.append(data)

    def get(self):
        if (len(self) <= 0):
            raise Exception('Queue is emty')
        return self.pop(0)

class JsonConfig:
    def __init__(self, path):
        self.path = path
        self.data = {}
        self.is_loaded = False

    def save(self):
        write_json(self.path, self.data)
    
    def load(self):
        if (check_file_exists(self.path)):
            self.data = read_json(self.path)
        else:
            write_json(self.path, self.data)
        self.is_loaded = True
        return self
    
    def ensure_loaded(self):
        if (not self.is_loaded): self.load()