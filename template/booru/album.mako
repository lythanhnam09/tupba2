<%inherit file="../base.mako"/>
<%block name="title">
    Booru Browser - Albums
</%block>
<%block name="extracss">
    <link rel="stylesheet" href="/static/css/booru.css">
</%block>
<%block name="extrajs">
    <script src="/static/js/booru/booru.js"></script>
    <script src="/static/js/booru/album.js"></script>
</%block>

<%def name="form_option(form, name, value, text)">
    <option value="${value}" ${form.option_selected(name, value)}>${text}</option>
</%def>

<div class="bg-d10-dark">
    <div class="container-lg bg-d5-dark py-2">
        <h1 class="text-center">Albums</h1>
        <hr class="my-1">
        <div class="control-group gap-1 px-1">
            <button class="btn btn-primary" onclick="showAlbumDailog('Create new album')"><i class="fas fa-plus"></i> New album</button>
        </div>
        <hr class="my-1">

        <div class="px-1">
            <div class="list-container p-1">
                % for album in ls_album:
                    <div class="galery-image card bg-l10-dark">
                        <a href="/booru/albums/${album['id']}">
                            <div id="img-thumb-${album['id']}" data-spoilered="0" class="img-container image-square">
                                % if album['thumbnail'] == None:
                                    <img class="w-100" src="/static/img/no-image.png" alt="">
                                % else:
                                    <img class="w-100" src="${album['thumbnail'].get_image('thumb', True)['link']}" alt="">
                                % endif
                            </div>
                        </a>
                        <div class="card-header bg-d10-pink">
                            <div class="text-bold">${album['name']}</div>
                            <div class="d-flex flex-space-between vflex-center">
                                <div>
                                    <i class="fas fa-image"></i> ${album['image_count']}
                                </div>
                                <div>
                                    <button class="btn-transparent fg-white px-1" onclick="showAlbumDailog('Edit album name', true, ${album['id']}, name = '${album['name']}')"><i class="fas fa-pen"></i></button>
                                    % if album['name'] != 'Favorited':
                                        <button class="btn-transparent btn-danger fg-white px-1" onclick="deleteAlbum(${album['id']}, '${album['name']}')"><i class="fas fa-times"></i></button>
                                    % endif
                                </div>
                            </div>
                        </div>
                    </div>
                % endfor
            </div>
        </div>
    </div>
</div>

