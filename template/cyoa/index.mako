<%inherit file="../base.mako"/>
<%block name="title">
    CYOA Browser - Main page
</%block>
<%block name="extracss">
    <link rel="stylesheet" href="/static/css/cyoa.css">
</%block>
<%block name="extrajs">
    <script src="/static/js/cyoa/cyoa.js"></script>
</%block>

<%def name="form_option(form, name, value, text)">
    <option value="${value}" ${form.option_selected(name, value)}>${text}</option>
</%def>

<% ls_perpage = [20, 50, 100, 200, 0] %>

<div class="bg-darkblue">
    <div class="container-lg bg-d25-darkblue py-2">
        <h1 class="text-center">CYOA List</h1>
        <hr class="mb-2">
        <form id="form-filter" class="d-block mx-2" action="/cyoa">
            <h2>Filter</h2>
            <input class="form-control w-100" name="q" type="text" placeholder="Search tag, title" value="${form['q']}">
            <div class="control-group mt-1">
                <button class="btn btn-success mr-1 order-xsm-last" type="submit"><i class="fas fa-filter"></i> Filter</button>
                <select class="form-control mr-1 fs-xsm" name="sf" id="sf">
                    ${form_option(form, 'sf', 'last_post_time', 'Sort by Last post time')}
                    ${form_option(form, 'sf', 'first_post_time', 'Sort by First post time')}
                    ${form_option(form, 'sf', 'quest_time', 'Sort by Quest time')}
                    ${form_option(form, 'sf', 'total_thread', 'Sort by Thread count')}
                    ${form_option(form, 'sf', 'total_image', 'Sort by Image count')}
                    ${form_option(form, 'sf', 'total_post', 'Sort by Post count')}
                    ${form_option(form, 'sf', 'total_fanart', 'Sort by Fanart count')}
                    ${form_option(form, 'sf', 'ratio', 'Sort by Image / Text ratio')}
                    ${form_option(form, 'sf', 'name', 'Sort by Title')}
                    ${form_option(form, 'sf', 'short_name', 'Sort by Short name')}
                    ${form_option(form, 'sf', 'id', 'Sort by ID')}
                </select>
                <select class="form-control mr-1 fs-xsm" name="sd" id="sd">
                    ${form_option(form, 'sd', 'desc', 'Descending')}
                    ${form_option(form, 'sd', 'asc', 'Ascending')}
                </select>
                <input type="hidden" name="perpage" value="${form['perpage']}">
                <input type="hidden" name="page" value="${form['page']}">
            </div>
        </form>
        <hr class="my-2">
        <div class="control-group px-2">
            <button id="btn-refresh" class="btn btn-primary mr-1" title="Refresh" onclick="refreshCyoaData()"><i class="fas fa-sync"></i></button>
            ${page_nav.html().markup()}
            <select id="select-perpage" class="form-control ml-1" name="perpage" id="perpage" onchange="changePerpage()">
                % for p in ls_perpage:
                    ${form_option(form, 'perpage', p, 'Show all' if p == 0 else f'Show {p}')}
                % endfor
            </select>
            <div id="page-stat" class="pl-2">Showing ${len(ls_cyoa.data)} of ${ls_cyoa.total_count}</div>
        </div>
        <hr class="mt-2">

        <div class="list-container m-1">
            % for cyoa in ls_cyoa.data:
                <div class="cyoa card bg-l15-darkblue">
                    <a class="cyoa card-image img-container" href="/cyoa/quest/${cyoa['short_name']}">
                        <img src="${cyoa['image_link']}" alt="${cyoa['name']}">
                    </a>
                    <div class="cyoa card-content p-1">
                        <h3 class="title">
                            % if cyoa['is_live'] == 1:
                                <a class="tag-item bg-l5-danger" href="?${form.get_form_query({'q': 'is_live=1'}, ['page', 'refresh'])}">LIVE</a>
                            % endif
                            <a class="name" href="/cyoa/quest/${cyoa['short_name']}">${cyoa['name']}</a>
                        </h3>
                        <div class="description mb-1">
                            ${cyoa['description']}
                        </div>
                        <div class="status">
                            <div class="stat">
                                <i class="fas fa-link fg-l10-warning"></i> ${cyoa['chan']} - ${cyoa['board']}
                                <i class="fas fa-link fg-l10-warning ml-1"></i> <a class="fg-white" href="https://www.anonpone.com/quest/${cyoa['short_name']}" target="_blank">${cyoa['short_name']}</a>
                                <i class="fas fa-hashtag fg-l10-warning ml-1"></i> ${cyoa['id']}
                            </div>
                            <div class="date">
                                <i class="fas fa-calendar-alt fg-l10-warning"></i> ${cyoa['first_post_date_str']} <i class="fas fa-arrow-right fg-l10-warning"></i> ${cyoa['last_post_date_str']}
                            </div>
                            <div class="stat mb-1">
                                <i class="fas fa-book fg-l10-warning"></i> ${cyoa['total_thread']}
                                <i class="fas fa-file fg-l10-warning ml-1"></i> ${cyoa['total_post']}
                                <i class="fas fa-align-left fg-l10-warning ml-1"></i> ${cyoa['word_count']}
                                <i class="fas fa-image fg-l10-warning ml-1"></i> ${cyoa['total_fanart']}
                            </div>
                            <div class="ratio" title="Image / Text ratio">
                                <div class="image" style="width:${cyoa['total_image_per']}"></div>
                                <div class="value"><i class="fas fa-image"></i> ${cyoa['total_image']} / ${cyoa['total_post'] - cyoa['total_image']} <i class="fas fa-align-left"></i></div>
                            </div>
                        </div>
                        <div class="tag">
                            <% lsstat = [['error', 'bg-danger'], ['active', 'bg-d5-info'], ['complete', 'bg-d5-success'], ['hiatus', 'bg-d5-warning'], ['cancelled', 'bg-danger'], ['hidden', 'bg-d15-danger']] %>
                            <a class="tag-item ${lsstat[cyoa['status']][1]}" href="?${form.get_form_query({'q': 'status=%d' % cyoa['status']}, ['page', 'refresh'])}">${lsstat[cyoa['status']][0]}</a>
                            % for tag in cyoa['tags']:
                                <a class="tag-item ${tag['tag']['color']}" href="?${form.get_form_query({'q': tag['tag']['name']}, ['page', 'refresh'])}">${tag['tag']['name']}</a>
                            % endfor
                            % if cyoa['steath_lewd']:
                                <a class="tag-item bg-pink" href="?${form.get_form_query({'q': 'lewd_exist=1'}, ['page', 'refresh'])}">lewd exist</a>
                            % endif
                        </div>
                    </div>
                </div>
            % endfor
        </div>

        <hr class="my-2">
        <div class="control-group px-2">
            <button id="btn-top" class="btn btn-primary mr-1" title="To page top" onclick="scrollToEl('#btn-refresh', 1000)"><i class="fas fa-arrow-to-top"></i></button>
            ${page_nav.html().markup()}
            <select id="select-perpage-b" class="form-control ml-1" name="perpage" id="perpage" onchange="changePerpage('form-filter', 'select-perpage-b')">
                % for p in ls_perpage:
                    ${form_option(form, 'perpage', p, 'Show all' if p == 0 else f'Show {p}')}
                % endfor
            </select>
            <div id="page-stat" class="pl-2">Showing ${len(ls_cyoa.data)} of ${ls_cyoa.total_count}</div>
        </div>
    </div>
</div>

