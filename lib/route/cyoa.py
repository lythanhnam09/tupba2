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


cyoa = Blueprint('cyoa', __name__, template_folder='template', root_path='.')
CORS(cyoa, support_credentials=True)

def cyoa_nav():
    right_btn = [NavButton('Saved CYOA', 'fas fa-server'), NavButton('Tags', 'fas fa-tags')]

    left_btn = [NavButton('Back', 'fas fa-arrow-left', href='/'), NavButton('Previous', 'fas fa-chevron-left', on_click='history.back()'), NavButton('Next', 'fas fa-chevron-right', on_click='history.forward()')]
    nav_item = NavOption('CYOA Browser', title_link='/cyoa', theme='nav-success', left_buttons=left_btn, right_buttons=right_btn)

    return nav_item

@cyoa.route('/')
def root():
    ref = request.args.get('refresh', False, type=bool)
    ls = anonpone.get_cyoa_list(ref)
    if (ref):
        return redirect('/cyoa')
    return render_template('cyoa/index.html', nav=cyoa_nav(), ls_cyoa=ls)

