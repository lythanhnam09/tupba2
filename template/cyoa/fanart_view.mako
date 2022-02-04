<%inherit file="../base.mako"/>
<%block name="title">
    Fanart view - ${cyoa['name']}
</%block>
<%block name="extracss">
    <link rel="stylesheet" href="/static/css/cyoa.css">
</%block>
<%block name="extrajs">
    <script src="/static/js/util/loader.js"></script>
    <script src="/static/js/util/gesture.js"></script>
    <script src="/static/js/cyoa/cyoa.js"></script>
    <script src="/static/js/cyoa/cyoainfo.js"></script>
    <script src="/static/js/cyoa/fanartview.js"></script>
</%block>

<% ls_perpage = [40, 80, 100, 200, 0] %>

<%def name="form_option(form, name, value, text)">
    <option value="${value}" ${form.option_selected(name, value)}>${text}</option>
</%def>

<div class="bg-darkblue">
    <div class="container-lg bg-d25-darkblue py-2">
        <div class="cyoa-info">
            <div class="image img-container ${'' if cyoa['image_path'] == None else 'saved'}">
                <img src="${cyoa['image_link']}" alt="${cyoa['short_name']}">
            </div>
            <div class="info">
                <h1 class="title">
                    % if cyoa['is_live'] == 1:
                        <a class="tag-item bg-l5-danger" href="/cyoa?q=is_live=1">LIVE</a>
                    % endif
                    ${cyoa['name']}
                </h1>
                <hr>
                <div class="tag">
                    <% lsstat = [['error', 'bg-danger'], ['active', 'bg-d5-info'], ['complete', 'bg-d5-success'], ['hiatus', 'bg-d5-warning'], ['cancelled', 'bg-danger'], ['hidden', 'bg-d15-danger']] %>
                    <a class="tag-item ${lsstat[cyoa['status']][1]}" href="?q=status=${cyoa['status']}">${lsstat[cyoa['status']][0]}</a>
                    % for tag in cyoa['tags']:
                        <a class="tag-item ${tag['tag']['color']}" href="?${form.get_form_query({'q': tag['tag']['name']})}">${tag['tag']['name']}</a>
                    % endfor
                    % if cyoa['steath_lewd']:
                        <a class="tag-item bg-pink" href="?q=lewd_exist=1">lewd exist</a>
                    % endif
                </div>
                <div class="ratio mt-1" title="Image / Text ratio">
                    <div class="image" style="width:${cyoa['total_image_per']}"></div>
                    <div class="value"><i class="fas fa-image"></i> ${cyoa['total_image']} Images / Texts ${cyoa['total_post'] - cyoa['total_image']} <i class="fas fa-align-left"></i></div>
                </div>
                <div class="stat mt-1">
                    <i class="fas fa-calendar-alt fg-l10-warning"></i> <span class="fg-l10-warning">Date: </span> ${cyoa['first_post_date_str']}
                    <i class="fas fa-arrow-right fg-l10-warning"></i> ${cyoa['last_post_date_str']}
                </div>
                <div class="stat">
                    <i class="fas fa-hashtag fg-l10-warning"></i> <span class="fg-l10-warning">ID: </span> ${cyoa['id']}
                    <i class="fas fa-link fg-l10-warning ml-1"></i> <span class="fg-l10-warning">Link: </span> <a class="fg-white" href="https://www.anonpone.com/quest/${cyoa['short_name']}" target="_blank">anonpone.com/${cyoa['short_name']}</a>
                </div>
                <div class="stat">
                    <i class="fas fa-link fg-l10-warning"></i> <span class="fg-l10-warning">Chan: </span> ${cyoa['chan']} - ${cyoa['board']}
                </div>
                <div class="stat">
                    <i class="fas fa-book fg-l10-warning"></i> <span class="fg-l10-warning">Thread count: </span> ${cyoa['total_thread']}
                    <i class="fas fa-file fg-l10-warning ml-1"></i> <span class="fg-l10-warning">Post count: </span> ${cyoa['total_post']}
                </div>
                <div class="stat mb-1">
                    <i class="fas fa-align-left fg-l10-warning"></i> <span class="fg-l10-warning">Word count: </span> ${cyoa['word_count']}
                    <i class="fas fa-image fg-l10-warning ml-1"></i> <span class="fg-l10-warning">Fanart count: </span> ${cyoa['total_fanart']}
                </div>
                <h2 class="fg-l10-warning">Description</h2>
                <hr >
                <div class="description mt-1">
                    ${cyoa['description']}
                </div>
                % if cyoa['save_status'] > 0:
                    <hr class="mt-1">
                    <div class="control-group">
                        <a class="btn btn-success mr-1 mt-1 reload-disable" href="/cyoa/quest/${cyoa['short_name']}"><i class="fas fa-book"></i> View threads</a>
                        <button class="btn btn-success mr-1 mt-1 reload-disable"><i class="fas fa-file"></i> View by post</button>
                    </div>
                % endif
            </div>
        </div>
        
        <hr class="mb-1">

        % if cyoa['fanarts'].total_count > 0:
            <form id="form-page" action="/cyoa/quest/${cyoa['short_name']}/fanarts">
                <input id="inp-page" type="hidden" name="page" value="1">
                <input id="inp-perpage" type="hidden" name="perpage" value="${form['perpage']}">
            </form>
            
            <div class="control-group px-2">
                <button id="btn-refresh" class="btn btn-primary mr-1" title="Refresh" onclick="refreshCyoaFanart(${cyoa['id']})"><i class="fas fa-sync"></i></button>
                ${page_nav.html().markup()}
                <select id="select-perpage" class="form-control ml-1" name="perpage" id="perpage" onchange="changePerpage('form-page')">
                    % for p in ls_perpage:
                        ${form_option(form, 'perpage', p, 'Show all' if p == 0 else f'Show {p}')}
                    % endfor
                </select>
                <div id="page-stat" class="pl-2">Showing ${len(cyoa['fanarts'].data)} of ${cyoa['fanarts'].total_count}</div>
            </div>
            <hr class="my-1">

            <div class="thread-image list-container m-1">
                % for img in cyoa['fanarts'].data:
                    <div class="thread-image card bg-l15-darkblue img-container lim-h" onclick="showImageView(${cyoa['id']}, ${cyoa['fanarts'].page_num}, ${cyoa['fanarts'].page_count}, ${cyoa['fanarts'].total_count}, ${cyoa['fanarts'].per_page}, ${loop.index})">
                        <img src="${img['link']}" title="${img['artist']} - ${img['title']}">
                    </div>
                % endfor
            </div>
            <hr>

            <div class="control-group px-2 py-1">
                <button id="btn-top" class="btn btn-primary mr-1" title="To page top" onclick="scrollToEl('#btn-refresh', 1000)"><i class="fas fa-arrow-to-top"></i></button>
                ${page_nav.html().markup()}
                <select id="select-perpage-b" class="form-control ml-1" name="perpage" id="perpage" onchange="changePerpage('form-page', 'select-perpage-b')">
                    % for p in ls_perpage:
                        ${form_option(form, 'perpage', p, 'Show all' if p == 0 else f'Show {p}')}
                    % endfor
                </select>
                <div id="page-stat" class="pl-2">Showing ${len(cyoa['fanarts'].data)} of ${cyoa['fanarts'].total_count}</div>
            </div>
            <hr>
        % else:
            <div class="emty-frame text-center h-100">
                <h1 class="mt-3 fg-d25-light">Nothing here, lol</h1>
                <button id="btn-refresh" class="btn btn-primary mt-1 reload-disable" onclick="refreshCyoaFanart(${cyoa['id']})"><i class="fas fa-sync"></i> Refresh</button>
            </div>
        % endif

    </div>
</div>

<div id="image-view" class="image-view" style="display:none">
    <div id="image-view-control" class="image-view-control card-inline bg-l20-darkblue">
        <div class="control-group">
            <div id="image-control-drag" class="d-iflex vflex-center fg-white"><i class="fas fa-bars px-2"></i></div>
            <button class="btn btn-darkblue px-1 ml-1" onclick="viewPrevious()"><i class="fas fa-chevron-left"></i></button>
            <button class="btn btn-darkblue px-1 ml-1" onclick="viewNext()"><i class="fas fa-chevron-right"></i></button>
            <button id="image-control-zoom" class="btn btn-darkblue progress-bar px-1 ml-1"><div class="value bg-d10-primary"></div><i class="fas fa-minus mr-1"></i> <span id="zoom-per" class="text-bold">100%</span> <i class="fas fa-plus ml-1"></i></button>
            <button class="btn btn-darkblue px-1 ml-1" onclick="resetImageView()"><i class="fas fa-expand"></i></button>
            <button class="btn btn-danger px-1 ml-1" onclick="closeImageView()"><i class="fas fa-times"></i></button>
        </div>
    </div>
    <div class="image-view-main">
        <div id="image-view-drag" draggable="false" class="img-container">
            <img id="image-view-image" style="width:100%" draggable="false" src="/static/img/no-image.png" alt="no-image named no-image here">
        </div>
    </div>
</div>
