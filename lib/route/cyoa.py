from flask import *
from flask_cors import CORS, cross_origin
import os
from datetime import datetime, tzinfo, timedelta
import math
import urllib
import lib.model.cyoa._ref
import lib.provider.anonpone as anonpone
from lib.model.web.navbar import NavOption, NavButton
from lib.model.cyoa.cyoa import *
from lib.model.web.form import WebForm


cyoa = Blueprint('cyoa', __name__, template_folder='template', root_path='.')
CORS(cyoa, support_credentials=True)

def cyoa_nav():
    right_btn = [NavButton('Saved CYOA', 'fas fa-server'), NavButton('Tags', 'fas fa-tags')]

    left_btn = [NavButton('Back', 'fas fa-arrow-left', href='/'), NavButton('Previous', 'fas fa-chevron-left', on_click='history.back()'), NavButton('Next', 'fas fa-chevron-right', on_click='history.forward()')]
    nav_item = NavOption('CYOA Browser', title_link='/cyoa', theme='nav-success', left_buttons=left_btn, right_buttons=right_btn)

    return nav_item

@cyoa.route('/')
def root():
    form = WebForm(data={'refresh':False, 'page':1, 'perpage':20, 'sf':'last_post_time', 'sd':'desc', 'q':''})
    form.get_arg_value(request.args)
    
    if (form['refresh']):
        anonpone.refresh_cyoa_list()
        return redirect('/cyoa')
    else:
        ls = anonpone.get_cyoa_list(form['q'], form['page'], form['perpage'], [form['sf'], form['sd']])
    
    return render_template('cyoa/index.html', nav=cyoa_nav(), form=form, ls_cyoa=ls)

@cyoa.route('/quest/<sname>')
def cyoa_info(sname):
    cy = Cyoa.find_shortmame(sname)
    if (cy is None): abort(404)
    cy.check_steath_lewd()
    return render_template('cyoa/info.html', nav=cyoa_nav(), cyoa=cy)

@cyoa.route('/api/cyoa/refresh')
def api_refresh_cyoa():
    anonpone.refresh_cyoa_list()
    return 'OK', 200

