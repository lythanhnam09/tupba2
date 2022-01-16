from flask import *
from flask_cors import CORS, cross_origin
import os
from datetime import datetime, tzinfo, timedelta
import math
import urllib
import lib.model.booru._ref
import lib.provider.anonpone as anonpone
from lib.model.web.navbar import *
from lib.model.web.form import WebForm
from lib.model.web.page import SimplePageNav
from lib.util.task_util import get_queue_stat
from lib.util.util import serve_template,StopTimer
import asyncio
import lib.provider.derpibooru as derpibooru

booru = Blueprint('booru', __name__, template_folder='template', root_path='.')
CORS(booru, support_credentials=True)

def booru_nav():
    right_btn = [NavButton('Filters', 'fas fa-filter'), NavButton('Feeds', 'fas fa-rss'), NavButton('Albums', 'fas fa-images'), NavButton('History', 'fas fa-history')]

    left_btn = [NavButton('Back', 'fas fa-arrow-left', href='/'), NavButton('Previous', 'fas fa-chevron-left', on_click='history.back()'), NavButton('Next', 'fas fa-chevron-right', on_click='history.forward()')]
    nav_item = NavOption('Booru Browser', title_link='/booru', theme='nav-booru', left_buttons=left_btn, right_buttons=right_btn)

    return nav_item

@booru.route('/')
def root():
    return serve_template('booru/index.mako', nav=booru_nav())

@booru.route('/search')
async def search():
    form = WebForm({'q': '', 'sf': 'id', 'sd': 'desc', 'page': 1, 'perpage':20})
    form.get_arg_value(request.args)
    t = StopTimer('Fetching booru data')
    res = await derpibooru.search_loader.do_get(form['page'], {'q':form['q'], 'sf':form['sf'], 'sd':form['sd'], 'perpage':form['perpage']})
    t.measure()
    return serve_template('booru/search.mako', nav=booru_nav(), form=form, img_page=res, page_nav=SimplePageNav(res, 'form-filter'))