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
    f = open(dir)
    txt = f.readlines()
    f.close()
    return txt

def read_text_file(dir):
    f = open(dir)
    txt = f.read()
    f.close()
    return txt

def write_text_file(dir, txt):
    f = open(dir, 'wt')
    txt = f.write(txt)
    f.close()
    return txt

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

class PageButton:
    def __init__(self, text='0', link='', disabled=False, num=0):
        self.text = text
        self.num = num
        self.disabled = disabled
        self.link = link

def get_page_link(page, page_count, template):
    ls = []
    scroll = 5
    if (page_count < 10):
        start = 1
        end = page_count
    else:
        start = page - 5
        end = page + 5
        if (start < 1):
            end -= start - 1
            start = 1
        if (end > page_count):
            start -= page_count - end
            if (start < 1): start = 1
            end = page_count
    #print(f'start={start} end={end}')
    if (page <= 1):
        ls.append(PageButton('<<', '', True))
        ls.append(PageButton('<', '', True))
    else:
        ls.append(PageButton('<<', template.format(1), num=1))
        ls.append(PageButton('<', template.format(page - 1), num=page-1))

    for p in range(start, end+1):
        if (p == page):
            ls.append(PageButton(f'{p}', template.format(p), True))
        else:
            ls.append(PageButton(f'{p}', template.format(p), num=p))

    if (page >= page_count):
        ls.append(PageButton('>', '', True))
        ls.append(PageButton('>>', '', True))
    else:
        ls.append(PageButton('>', template.format(page + 1), num=page+1))
        ls.append(PageButton('>>', template.format(page_count), num=page_count))

    return ls

def get_file_size_str(num, round = 2, threshold = 1024):
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
        self.start = time.perf_counter()