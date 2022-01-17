<%inherit file="../base.mako"/>
<%block name="title">
    Booru Browser - View image ${img['id']}
</%block>
<%block name="extracss">
    <link rel="stylesheet" href="/static/css/booru.css">
</%block>
<%block name="extrajs">
    <script src="/static/js/booru.js"></script>
    <script>changeImageSize(5);</script>
</%block>

<%def name="form_option(form, name, value, text)">
    <option value="${value}" ${form.option_selected(name, value)}>${text}</option>
</%def>

<% ls_perpage = [5, 10, 15, 20, 25] %>

<div class="bg-d10-dark">
    <div class="container-lg bg-d5-dark py-2">
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
        </div>
        <hr class="my-1">
        <div class="control-group gap-1 px-1">
            <div class="control-group-round">
                % for sz in img['sizes']:
                    <% if sz['name'].find('Thumb') != -1: continue %>
                    <button id="btn-size-${sz['size_index']}" class="btn btn-primary btn-size" data-mode="0" onclick="changeImageSize(${sz['size_index']}, '${sz['link']}', '${img['extension']}')">${sz['name']}</button>
                % endfor
            </div>
            % if img['extension'] in ['webm', 'mp4']:
                <div class="control-group-round">
                    <button id="btn-mode-0" class="btn btn-primary btn-mode" onclick="setVideoMode(0)" disabled>WebM</button>
                    <button id="btn-mode-1" class="btn btn-primary btn-mode" onclick="setVideoMode(1)">MP4</button>
                </div>
            % endif
        </div>
        <hr class="my-1">
        <div class="px-1">
            % if img['extension'] in ['webm', 'mp4']:
                <video class="img-display" id="video-display" controls autoplay loop muted>
                    <source id="img-display" src="${img.get_image('medium')['link']}" type="${img['mime_type']}">
                    HTML Video tag not supported (PLEASE UPGRADE YOUR SHITTY BROWSER !!!)
                </video>
            % else:
                <img id="img-display" class="img-display" src="${img.get_image('medium')['link']}">
            % endif
        </div>
        <div class="px-1">
            <div class="card my-1">
                <div class="card-header bg-d5-pink">
                    <h2><i class="fas fa-tag"></i> Tags</h2>
                </div>
                <div class="card-content bg-dark p-1">
                    <div class="control-group gap-1">
                        % for tag in img['tags']:
                            <a class="booru-tag ${tag['tag']['color']}" href="/booru/search?q=${tag['tag']['name']}">${tag['tag']['name']}</a>
                        % endfor
                    </div>
                </div>
            </div>
            <div class="card my-1">
                <div class="card-header bg-d5-pink">
                    <h2>Description</h2>
                </div>
                ## Must not breakline for easier parsing
                <div id="text-description" class="card-content bg-dark">${img['description']}</div>
            </div>
        </div>
    </div>
</div>

