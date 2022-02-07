<%inherit file="../base.mako"/>
<%block name="title">
    Booru Browser - View image ${img['id']}
</%block>
<%block name="extracss">
    <link rel="stylesheet" href="/static/css/booru.css">
</%block>
<%block name="extrajs">
    <script src="/static/js/booru/booru.js"></script>
    <script src="/static/js/booru/view.js"></script>
</%block>

<%def name="form_option(form, name, value, text)">
    <option value="${value}" ${form.option_selected(name, value)}>${text}</option>
</%def>

<% ls_perpage = [5, 10, 15, 20, 25] %>

<% prefer_size = img.get_image('Medium', True) %>

<div class="bg-d10-dark">
    <div class="container-lg bg-d5-dark py-2">
        <div class="px-1">
            <div class="card bg-dark">
                <div class="card-content bg-dark">
                    <div><b class="fg-l15-pink">File name:</b> ${img['name']}</div>
                    <div><b class="fg-l15-pink">File size:</b> ${img['image_size_str']}</div>
                    <div><b class="fg-l15-pink">Image size:</b> ${img['width']} x ${img['height']} </div>
                    <div><b class="fg-l15-pink">Uploader:</b> ${img['uploader'] or '<i class="fg-secondary">Anonymous</i>'}</div>
                    <div><b class="fg-l15-pink">Date created:</b> ${img['created_at']}</div>
                    <div><b class="fg-l15-pink">Last updated:</b> ${img['updated_at']}</div>
                    <div><b class="fg-l15-pink">Source:</b> ${f'<a href="{img["link_source"]}">{img["link_source"]}</a>' if (img["link_source"] not in [None, '']) else '<i class="fg-secondary">Not provided</i>'}</div>
                    <div><b class="fg-l15-pink">Booru link:</b> <a href="https://derpibooru.org/images/${img['id']}">https://derpibooru.org/images/${img['id']}</a></div>
                    % if img['delete_reason'] != None:
                        <div><b class="fg-danger">Image is deleted: ${img['delete_reason']}</div>
                    % endif
                    <div>
                        <div class="d-iblock">
                            <span class="fg-l5-success">${img['upvote']} <i class="fas fa-arrow-up"></i></span>
                            ${img['score']}
                            <span class="fg-danger"><i class="fas fa-arrow-down"></i> ${img['downvote']}</span>
                        </div>
                        <div class="d-iblock ml-1">
                            <span class="fg-l5-warning">${img['fave']} <i class="fas fa-star"></i></span>
                        </div>
                        <div class="d-iblock ml-1">
                            <span class="fg-l5-pink">${img['comment_count']} <i class="fas fa-comment"></i></span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <hr class="my-1">
        <div class="control-group px-1 gap-1">
            % if prev_link != None:
                <a href="${prev_link}" class="btn btn-primary"><i class="fas fa-chevron-left"></i></a>
            % else:
                <button class="btn btn-primary" disabled><i class="fas fa-chevron-left"></i></button>
            % endif
             % if next_link != None:
                <a href="${next_link}" class="btn btn-primary"><i class="fas fa-chevron-right"></i></a>
            % else:
                <button class="btn btn-primary" disabled><i class="fas fa-chevron-right"></i></button>
            % endif
            <button class="btn btn-primary" onclick="favorite(${img['id']})"><i class="fas fa-star"></i> Add to favortie</button>
            <button class="btn btn-primary" onclick="showAlbumDialog(${img['id']})"><i class="fas fa-plus"></i> Add to album</button>
        </div>
        <hr class="my-1">
        <div class="control-group gap-1 px-1">
            <div class="control-group-round">
                % for sz in img['sizes']:
                    <% if sz['name'].find('Thumb') != -1: continue %>
                    % if sz['name'].lower() == prefer_size['name'].lower():
                        <button id="btn-size-${sz['size_index']}" class="btn btn-primary btn-size" data-mode="0" onclick="changeImageSize(${sz['size_index']}, '${sz['link']}', '${sz.get_extension()}')" disabled>${sz['name']}</button>
                    % else:
                        <button id="btn-size-${sz['size_index']}" class="btn btn-primary btn-size" data-mode="0" onclick="changeImageSize(${sz['size_index']}, '${sz['link']}', '${sz.get_extension()}')">${sz['name']}</button>
                    % endif
                % endfor
            </div>
            ## % if img['extension'] in ['webm', 'mp4']:
            ##     <div class="control-group-round">
            ##         <button id="btn-mode-0" class="btn btn-primary btn-mode" onclick="setVideoMode(0)" disabled>WebM</button>
            ##         <button id="btn-mode-1" class="btn btn-primary btn-mode" onclick="setVideoMode(1)">MP4</button>
            ##     </div>
            ## % endif
        </div>
        <hr class="my-1">
        <div id="img-display-container" class="px-1" data-ext="${prefer_size.get_extension()}">
            % if img['extension'] in ['webm', 'mp4']:
                <video class="img-display" id="video-display" controls autoplay loop muted>
                    <source id="img-display" src="${prefer_size.get_mp4_link()}" type="video/mp4">
                    <source id="img-display-alt" src="${prefer_size['link']}" type="${img['mime_type']}">
                    HTML Video tag not supported (PLEASE UPGRADE YOUR SHITTY BROWSER !!!)
                </video>
            % else:
                <img id="img-display" class="img-display" src="${prefer_size['link']}">
            % endif
        </div>
        <div class="px-1">
            <div class="card my-1 bg-dark">
                <div class="card-header bg-d5-pink">
                    <h3><i class="fas fa-tag"></i> Tags</h3>
                </div>
                <div class="card-content bg-dark p-1">
                    <div class="control-group gap-1">
                        % for tag in img['tags']:
                            <a class="booru-tag ${tag['tag']['color']}" href="/booru/search?q=${tag['tag']['name']}">${tag['tag']['name']}</a>
                        % endfor
                    </div>
                </div>
            </div>
            <div class="card my-1 bg-dark">
                <div class="card-header bg-d5-pink">
                    <h3>Description</h3>
                </div>
                ## Must not breakline for easier parsing
                <div id="text-description" class="card-content bg-dark markup">${img['description']}</div>
            </div>
        </div>
    </div>
</div>

