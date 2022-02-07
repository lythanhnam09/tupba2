<%inherit file="../base.mako"/>
<%namespace name="misc" file="misc.mako"/>
<%block name="title">
    Booru Browser - Album images
</%block>
<%block name="extracss">
    <link rel="stylesheet" href="/static/css/booru.css">
</%block>
<%block name="extrajs">
    <script src="/static/js/booru/booru.js"></script>
</%block>

<%def name="form_option(form, name, value, text)">
    <option value="${value}" ${form.option_selected(name, value)}>${text}</option>
</%def>

<% ls_perpage = [5, 10, 15, 20, 25] %>

<div class="bg-d10-dark">
    <div class="container-lg bg-d5-dark py-2">
        <h1 class="text-center">Album - ${album['name']}</h1>
        <hr class="my-1">
        <div class="px-1">
            <h2 class="">Search</h2>
            <form id="form-filter" action="/booru/albums/${album['id']}" method="get">
                <input type="hidden" name="page" value="1">
                <input type="hidden" name="perpage" value="${form['perpage']}">
            </form>
        </div>
        <hr class="my-1">
        <div class="control-group px-2 gap-1">
            <button id="btn-bottom" class="btn btn-primary " title="Refresh" onclick="scrollToEl('#btn-top', 600)"><i class="fas fa-arrow-to-bottom"></i></button>
            ${page_nav.html().markup()}
            <select id="select-perpage" class="form-control " name="perpage" id="perpage" onchange="changePerpage()">
                % for p in ls_perpage:
                    ${form_option(form, 'perpage', p, f'Show {p}')}
                % endfor
            </select>
            <div id="page-stat" class="">Showing ${len(img_page.data)} of ${img_page.total_count}</div>
        </div>
        <hr class="my-1">
        <div class="px-1">
            <div class="list-container p-1">
                % for img in img_page.data:
                    ${misc.booru_album_image(img, f'/booru/view/{img["id"]}')}
                % endfor
            </div>
        </div>
        <hr class="my-1">
        <div class="control-group px-2 gap-1">
            <button id="btn-top" class="btn btn-primary " title="To page top" onclick="scrollToEl('#btn-bottom', 600)"><i class="fas fa-arrow-to-top"></i></button>
            ${page_nav.html().markup()}
            <select id="select-perpage-b" class="form-control " name="perpage" id="perpage" onchange="changePerpage('form-filter', 'select-perpage-b')">
                % for p in ls_perpage:
                    ${form_option(form, 'perpage', p, f'Show {p}')}
                % endfor
            </select>
            <div id="page-stat" class="">Showing ${len(img_page.data)} of ${img_page.total_count}</div>
        </div>
    </div>
</div>

