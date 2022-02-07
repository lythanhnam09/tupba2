<%def name="booru_search_image(img, link)">
    <div class="galery-image card bg-l10-dark">
        <div class="card-header bg-d20-pink pos-relative text-center">
            <span class="d-iblock "><i class="fas fa-arrow-up fg-l10-success"></i> ${img['score']} <i class="fas fa-arrow-down fg-l10-danger"></i></span>
            <span class="d-iblock fg-warning">${img['fave']} <i class="fas fa-star fg-warning"></i></span>
            <span class="d-iblock fg-light fg-l25-darkblue">${img['comment_count']} <i class="fas fa-comment"></i></span>
        </div>
        <a href="${link}">
            <div class="overlay-bar">
                % if img['extension'] == 'webm':
                    <div class="webm-bar">
                        <i class="fas fa-play mr-1"></i> WebM
                    </div>
                % endif
                % if img['spoiler_tag'] != '':
                    <div class="spoiler-bar" onclick="return toggleSpoiler(${img['id']}, '${img.get_image('thumb')['link']}')">
                        <i class="fas fa-eye-slash mr-1"></i>${img['spoiler_tag']}
                    </div>
                % endif
            </div>
            <div id="img-thumb-${img['id']}" data-spoilered="${0 if img['spoiler_tag'] == '' else 1}" class="img-container image-square">
                % if img['spoiler_tag'] != '':
                    <img class="w-100" src="/static/img/no-image.png" alt="">
                % else:
                    <img class="w-100" src="${img.get_image('thumb', True)['link']}" alt="">
                % endif
            </div>
        </a>
    </div>
</%def>

<%def name="booru_album_image(img, link)">
    <div class="galery-image card bg-l10-dark">
        <div class="card-header bg-d20-pink pos-relative row flex-space-between">
            <div>
                <span class="d-iblock "><i class="fas fa-arrow-up fg-l10-success"></i> ${img['score']} <i class="fas fa-arrow-down fg-l10-danger"></i></span>
                <span class="d-iblock fg-warning">${img['fave']} <i class="fas fa-star fg-warning"></i></span>
                <span class="d-iblock fg-light fg-l25-darkblue">${img['comment_count']} <i class="fas fa-comment"></i></span>
            </div>
            <div>
                <i class="fas fa-times fg-l10-danger"></i>
            </div>
        </div>
        <a href="${link}">
            <div class="overlay-bar">
                % if img['extension'] == 'webm':
                    <div class="webm-bar">
                        <i class="fas fa-play mr-1"></i> WebM
                    </div>
                % endif
            </div>
            <div id="img-thumb-${img['id']}" data-spoilered="${0 if img['spoiler_tag'] == '' else 1}" class="img-container image-square">
                <img class="w-100" src="${img.get_image('thumb', True)['link']}" alt="">
            </div>
        </a>
    </div>
</%def>