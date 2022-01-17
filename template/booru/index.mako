<%inherit file="../base.mako"/>
<%block name="title">
    Booru Browser - Main page
</%block>
<%block name="extracss">
    <link rel="stylesheet" href="/static/css/booru.css">
</%block>
<%block name="extrajs">
    <script src="/static/js/booru.js"></script>
</%block>

<%def name="form_option(form, name, value, text)">
    % if form != UNDEFINED:
        <option value="${value}" ${form.option_selected(name, value)}>${text}</option>
    % else:
        <option value="${value}">${text}</option>
    % endif
</%def>

<% ls_perpage = [20, 50, 100, 200, 0] %>

<div class="bg-d10-dark">
    <div class="container-lg bg-d5-dark py-2">
        <h1 class="text-center">Main page</h1>
        <hr class="my-1">
        <div class="px-1">
            <h2 class="">Search</h2>
            <form id="form-filter" action="/booru/search" method="get">
                <input name="q" type="text" class="form-control dark w-100 mb-1" placeholder="Enter search tags">
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
                    <input type="hidden" name="page" value="1">
                    <input type="hidden" name="perpage" value="20">
                </div>
            </form>
        </div>
        <hr class="my-1">
        <div class="px-1">
            <div class="card bg-dark">
                <div class="card-header bg-d5-pink">
                    <h3><i class="fas fa-history"></i> Last indexed</h3>
                </div>
                <div class="card-content list-container p-1">
                    % for i in range(20):
                        <div class="galery-image card bg-l10-dark">
                            <div class="card-header bg-d20-pink text-center pos-relative">
                                <span class="d-iblock "><i class="fas fa-arrow-up fg-l10-success"></i> 99999 <i class="fas fa-arrow-down fg-l10-danger"></i></span>
                                <span class="d-iblock fg-warning">9999 <i class="fas fa-star fg-warning"></i></span>
                                <span class="d-iblock fg-light fg-l25-darkblue">999 <i class="fas fa-comment"></i></span>
                            </div>
                            <a href="">
                                <div class="img-container image-square">
                                    <img src="https://derpicdn.net/img/2022/1/13/2784104/thumb.jpg" alt="">
                                </div>
                            </a>
                        </div>
                    % endfor
                    
                </div>
            </div>
        </div>
    </div>
</div>

