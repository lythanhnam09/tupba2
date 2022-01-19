<%inherit file="../base.mako"/>
<%namespace name="misc" file="misc.mako"/>
<%block name="title">
    Booru Browser - Search result
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
        <h1 class="text-center">Search result</h1>
        <hr class="my-1">
        <div class="px-1">
            <h2 class="">Search</h2>
            <div class="card my-1 bg-dark">
                <div class="card-content p-1 bg-dark">
                    <div class="control-group gap-1" id="tag-suggestion">
                        Tag suggestion...
                    </div>
                </div>
            </div>
            <form id="form-filter" action="/booru/search" method="get">
                <input id="q" name="q" type="text" class="form-control dark w-100 mb-1" placeholder="Enter search tags" value="${form['q']}">
                <div class="control-group gap-1">
                    <button class="btn btn-pink"><i class="fas fa-search"></i> Search</button>
                    <select class="form-control dark" name="sf">
                        ${form_option(form, 'sf', 'id', 'Sort by Image ID')}
                        ${form_option(form, 'sf', 'score', 'Sort by Score')}
                        ${form_option(form, 'sf', 'upvotes', 'Sort by Upvote')}
                        ${form_option(form, 'sf', 'downvotes', 'Sort by Downvote')}
                        ${form_option(form, 'sf', 'wilson_score', 'Sort by Wilson score')}
                        ${form_option(form, 'sf', 'faves', 'Sort by Favorites')}
                        ${form_option(form, 'sf', 'comment_count', 'Sort by Comment count')}
                        ${form_option(form, 'sf', 'tag_count', 'Sort by Tag count')}
                        ${form_option(form, 'sf', 'size', 'Sort by File size')}
                        ${form_option(form, 'sf', 'duration', 'Sort by Duration')}
                        ${form_option(form, 'sf', 'updated_at', 'Sort by Updated at')}
                        ${form_option(form, 'sf', 'first_seen_at', 'Sort by First seen at')}
                        ${form_option(form, 'sf', 'aspect_ratio', 'Sort by Aspect Ratio')}
                        ${form_option(form, 'sf', '_score', 'Sort by Relevance')}
                        ${form_option(form, 'sf', 'width', 'Sort by Image width')}
                        ${form_option(form, 'sf', 'height', 'Sort by Image width')}
                        ${form_option(form, 'sf', 'pixels', 'Sort by Pixels')}
                    </select>
                    <select class="form-control dark" name="sd">
                        ${form_option(form, 'sd', 'desc', 'Descending')}
                        ${form_option(form, 'sd', 'asc', 'Ascending')}
                    </select>
                </div>
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
                    ${misc.booru_image(img, f'/booru/view/{img["id"]}?{form.get_form_query()}')}
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

