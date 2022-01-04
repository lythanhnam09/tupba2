from flask import *
from flask_cors import CORS, cross_origin
import os
from datetime import datetime, tzinfo, timedelta
import math
import urllib
import lib.model.cyoa._ref
import lib.provider.anonpone as anonpone
from lib.model.web.navbar import *
from lib.model.cyoa.cyoa import *
from lib.model.cyoa.cyoa_thread import *
from lib.model.web.form import WebForm
from lib.model.web.page import SimplePageNav
from lib.util.task_util import get_queue_stat
from lib.util.util import serve_template


cyoa = Blueprint('cyoa', __name__, template_folder='template', root_path='.')
CORS(cyoa, support_credentials=True)

def cyoa_nav():
    right_btn = [NavButton('Saved CYOA', 'fas fa-server', href="/cyoa/?q=save_status>0"), NavButton('Tags', 'fas fa-tags')]

    left_btn = [NavButton('Back', 'fas fa-arrow-left', href='/cyoa'), NavButton('Previous', 'fas fa-chevron-left', on_click='history.back()'), NavButton('Next', 'fas fa-chevron-right', on_click='history.forward()')]
    nav_item = NavOption('CYOA Browser', title_link='/cyoa', theme='nav-cyoa', left_buttons=left_btn, right_buttons=right_btn)

    return nav_item

def thread_nav(cyoa, thread, ls_th, num, count):
    right_btn = [
        NavButton('Scroll top', 'fas fa-arrow-to-top', on_click="scrollToEl('body', 0)"), 
        NavButton('Scroll bottom', 'fas fas fa-arrow-to-bottom', on_click="scrollToEl('#hr-bottom', 0)"), 
        NavButton('First thread', 'fas fa-chevron-double-left', disabled=(num <= 0), href=f'{ls_th[0]["id"]}'), 
        NavButton('Previous thread', 'fas fa-chevron-left', disabled=(num <= 0), href=f'{ls_th[num - 1]["id"] if (num > 0) else ""}'), 
        NavLabel(f'{num+1}/{count}'),
        NavButton(f'Next thread', 'fas fa-chevron-right', disabled=(num + 1 >= count), href=f'{ls_th[num + 1]["id"] if (num+1 < count) else ""}'), 
        NavButton('Last thread', 'fas fa-chevron-double-right', disabled=(num + 1 >= count), href=f'{ls_th[count-1]["id"]}')
    ]

    left_btn = [
        NavButton('Back', 'fas fa-arrow-left', href=f'/cyoa/quest/{cyoa["short_name"]}')
    ]
    nav_item = NavOption(f'[{num+1}] {thread["title"]}' if thread['title'] not in ['', None] else f'[{num+1}] {cyoa["name"]} #{num+1}', theme='nav-cyoa-thread', left_buttons=left_btn, right_buttons=right_btn, title_size='12pt', show_progress=True)

    return nav_item

@cyoa.route('/')
def root():
    form = WebForm(data={'refresh':False, 'page':1, 'perpage':20, 'sf':'last_post_time', 'sd':'desc', 'q':''})
    form.get_arg_value(request.args)

    cnt = Cyoa.get_count()
    if (cnt == 0):
        anonpone.refresh_cyoa_list()
    
    if (form['refresh']):
        anonpone.refresh_cyoa_list()
        return redirect('/cyoa')
    else:
        ls = anonpone.get_cyoa_list(form['q'], form['page'], form['perpage'], [form['sf'], form['sd']])
    
    return serve_template('cyoa/index.mako', nav=cyoa_nav(), form=form, ls_cyoa=ls, page_nav=SimplePageNav(ls, 'form-filter'))

@cyoa.route('/quest/<sname>')
def cyoa_info(sname):
    form = WebForm(data={'page':1, 'perpage':40})
    form.get_arg_value(request.args)
    cy = Cyoa.find_shortname(sname)
    if (cy is None): abort(404)
    cy.check_steath_lewd()
    ls_th = anonpone.get_thread_list(cy, form['page'], form['perpage'])
    return serve_template('cyoa/info.mako', nav=cyoa_nav(), form=form, cyoa=cy, thread_page=ls_th, page_nav=SimplePageNav(ls_th, 'form-page'), worker_stat=get_queue_stat())

@cyoa.route('/quest/<sname>/thread/<thread_id>')
def thread_view(sname, thread_id):
    try:
        thread_id = int(thread_id)
    except Exception as e:
        abort(404)
    cy = Cyoa.find_shortname(sname)
    if (cy is None): abort(404)
    cyth = CyoaThread.find_id((cy['id'], thread_id))
    if (cyth is None): abort(404)
    th = Thread.find_id(thread_id)
    if (th == None): abort(404)
    ls_th = cy.get_ref('threads', get_many=True)
    num = [i for i,x in enumerate(ls_th) if x['id'] == th['id']][0]
    count = len(ls_th)
    ls_post = anonpone.get_post_list(cy, th)
    return serve_template('cyoa/thread_view.mako', nav=thread_nav(cy, th, ls_th, num, count), cyoa=cy, thread=th, ls_post=ls_post, thread_num=num)

@cyoa.route('/quest/<sname>/images')
def cyoa_image(sname):
    # qm: QM only ; link: Post with link only ; saved: Saved image ; thread: Thread num
    form = WebForm(data={'q':'is_qm=1,alt_id=0', 'page':1, 'perpage':40})
    form.get_arg_value(request.args)
    cy = Cyoa.find_shortname(sname)
    if (cy is None): abort(404)
    cy.check_steath_lewd()
    page = anonpone.get_cyoa_image(cy, form['q'], form['page'], form['perpage'])
    
    return serve_template('cyoa/image_view.mako', nav=cyoa_nav(), form=form, cyoa=cy, img_page = page, page_nav=SimplePageNav(page, 'form-page'), worker_stat=get_queue_stat())
