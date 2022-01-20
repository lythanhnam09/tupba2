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

def booru_nav(backlink='/'):
    right_btn = [NavButton('Filters', 'fas fa-filter', href='/booru/filters'), NavButton('Feeds', 'fas fa-rss'), NavButton('Albums', 'fas fa-images', href='booru/albums'), NavButton('History', 'fas fa-history', href='booru/history')]

    left_btn = [NavButton('Back', 'fas fa-arrow-left', href=backlink), NavButton('Previous', 'fas fa-chevron-left', on_click='history.back()'), NavButton('Next', 'fas fa-chevron-right', on_click='history.forward()')]
    nav_item = NavOption('Booru Browser', title_link='/booru', theme='nav-booru', left_buttons=left_btn, right_buttons=right_btn)

    return nav_item

@booru.route('/')
def root():
    ls_img = derpibooru.get_main_page_indexed(5)
    return serve_template('booru/index.mako', nav=booru_nav(), ls_img=ls_img)

@booru.route('/search')
def search():
    form = WebForm({'q': '', 'sf': 'id', 'sd': 'desc', 'page': 1, 'perpage':20})
    form.get_arg_value(request.args)
    t = StopTimer('Fetching booru data')
    res = derpibooru.get_search(form['q'], form['sf'], form['sd'], form['page'], form['perpage'])
    t.measure()
    return serve_template('booru/search.mako', nav=booru_nav('/booru'), form=form, img_page=res, page_nav=SimplePageNav(res, 'form-filter'))

@booru.route('/view/<id>')
def view(id):
    try:
        id = int(id)
    except Exception as e:
        abort(404)

    form = WebForm({'q': '', 'sf': 'id', 'sd': 'desc', 'page': 1, 'perpage':20})
    next_link = None
    prev_link = None
    back_link = '/booru'
    
    if ('q' in request.args):
        form.get_arg_value(request.args)
        res = derpibooru.get_search(form['q'], form['sf'], form['sd'], form['page'], form['perpage'])

        ls_index = [i for i,x in enumerate(res.data) if x['id'] == id]
        if (len(ls_index) <= 0): abort(404)
        
        index = ls_index[0]
        if (index > 0):
            prev_link = f'/booru/view/{res.data[index - 1]["id"]}?{form.get_form_query()}'
        elif res.page_num > 1:
            prev_res = derpibooru.get_search(form['q'], form['sf'], form['sd'], form['page'] - 1, form['perpage'], False)
            prev_link = f'/booru/view/{prev_res.data[-1]["id"]}?{form.get_form_query({"page": form["page"] - 1})}'
        if (index < len(res.data) - 1):
            next_link = f'/booru/view/{res.data[index + 1]["id"]}?{form.get_form_query()}'
        elif res.page_num < res.page_count:
            next_res = derpibooru.get_search(form['q'], form['sf'], form['sd'], form['page'] + 1, form['perpage'], False)
            next_link = f'/booru/view/{next_res.data[0]["id"]}?{form.get_form_query({"page": form["page"] + 1})}'

        img = res.data[index]
        back_link = f'/booru/search?{form.get_form_query()}'
    else:
        img = derpibooru.get_image_by_id(id)
        if (img == None):
            abort(404)

    return serve_template('booru/view.mako', nav=booru_nav(back_link), form=form, img=img, next_link=next_link, prev_link=prev_link)

@booru.route('/filters')
def filter_list():
    ls_filter = derpibooru.get_filter_list()
    return serve_template('booru/filter.mako', nav=booru_nav('/booru'), ls_filter=ls_filter)