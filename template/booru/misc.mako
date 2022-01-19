<%def name="booru_image(img, link)">
    <div class="galery-image card bg-l10-dark">
        <div class="card-header bg-d20-pink text-center pos-relative">
            <span class="d-iblock "><i class="fas fa-arrow-up fg-l10-success"></i> ${img['score']} <i class="fas fa-arrow-down fg-l10-danger"></i></span>
            <span class="d-iblock fg-warning">${img['fave']} <i class="fas fa-star fg-warning"></i></span>
            <span class="d-iblock fg-light fg-l25-darkblue">${img['comment_count']} <i class="fas fa-comment"></i></span>
        </div>
        <a href="${link}">
            % if img['extension'] == 'webm':
                <div class="webm-bar">
                    <i class="fas fa-play mr-1"></i> WebM
                </div>
            % endif
            <div class="img-container image-square">
                <img class="w-100" src="${img.get_image('thumb')['link']}" alt="">
            </div>
        </a>
    </div>
</%def>