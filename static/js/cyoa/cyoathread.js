$(document).ready(function() {
    // $('.nav-progress').hide();

    if ($('.nav-progress').length > 0) {
        $('.nav-progress').show();
        $('.nav-progress > .value').addClass('loading');

        showQMMark();

        $(window).scroll(function() {
            updateThreadProgress();
        });
    
        $(window).resize(function() {
            showQMMark();
            updateThreadProgress();
        });
    
        $(document).resize(function() {
            showQMMark();
            updateThreadProgress();
        });
    }
});

$(window).on("load", function() {
    if ($('.nav-progress').length > 0) {
        $('.nav-progress > .value').removeClass('loading');

        updateThreadProgress();
        showQMMark();
    }
});

function updateThreadProgress() {
    var winScroll = document.body.scrollTop || document.documentElement.scrollTop;
    var height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
    var scrolled = (winScroll / height) * 100;
    $('#nav-progress-value').css('width', scrolled + "%");
}

function showQMMark() {
    let height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
    let width = $('#mark-container').width();
    let left = $('#mark-container').offset().left;
    let markWidth = 6;
    let offset = 48;

    $('#mark-container').html('');

    $('.op').each(function() {
        let postId = $(this).data('id');

        let markpos = $(this).offset().top + left + offset;
        let barpos = (markpos / height) * width;
        if (barpos > (width - markWidth)) barpos = width - markWidth;
        $('#mark-container').append(`<div id="mark-${postId}" class="qm-mark" style="left:${barpos}px" onclick="scrollToEl('#p${postId}', 500, ${-offset})"></div>`);
    });

    $('.op-maybe').each(function() {
        let postId = $(this).data('id');

        let markpos = $(this).offset().top + left + offset;
        let barpos = (markpos / height) * width;
        if (barpos > (width - markWidth)) barpos = width - markWidth;
        $('#mark-container').append(`<div id="mark-${postId}" class="qm-mark maybe" style="left:${barpos}px" onclick="scrollToEl('#p${postId}', 500, ${-offset})"></div>`);
    });
    
    $('.lewd-1').each(function() {
        let postId = $(this).data('id');

        $(`#mark-${postId}`).addClass('lewd-1');
    });

    $('.lewd-2').each(function() {
        let postId = $(this).data('id');
        if ($(`#mark-${postId}`).length > 0) {
            $(`#mark-${postId}`).addClass('lewd-2');
        } else {
            let markpos = $(this).offset().top + left + offset;
            let barpos = (markpos / height) * width;
            if (barpos > (width - markWidth)) barpos = width - markWidth;

            $('#mark-container').append(`<div id="mark-${postId}" class="post-mark" style="left:${barpos}px" onclick="scrollToEl('#p${postId}', 500, ${-offset})"></div>`);
        }
    });
}

function changeAltImg(postId, altId) {
    let ls = $(`.img-container[data-id="${postId}"]`).children();
    for (let e of ls) {
        $(e).hide();
    }
    $(`.img-container[data-id="${postId}"] > img[data-altid="${altId}"]`).show();
}

function toggleExpandImage(postId, image = null) {
    let img = $(`.card-image[data-id="${postId}"]`);
    if (img.hasClass('expand')) {
        img.removeClass('expand');
        scrollToEl($(image), 0, -150);
    } else {
        img.addClass('expand');
    }
}

function restartGif(img, link) {
    if (link == '') return;
    img.src = '';
    img.src = link;
}

function showPostReply(button, postId) {
    let post = $(`#p${postId}`);
    if (post.length == 0) {
        $(button).prop('disabled', true);
        $(button).addClass('invalid');
        $(button).next().removeAttr('href');
        $(button).next().removeClass('btn-warning');
        $(button).next().removeClass('btn-primary');
        $(button).next().addClass('btn-disabled');
        return;
    }
    if ($(button).data('show') != 1) {
        $(button).data('show', 1);
        $(button).addClass('shown');
        $(`#p${postId}`).clone().insertAfter($(button).parent());
    } else {
        $(button).parent().next().remove();
        $(button).data('show', 0);
        $(button).removeClass('shown');
    }
    
}

function reparseThread(id) {
    socket.emit('cyoa_thread_reparse', {id:id});
    $('#btn-reparse').prop('disabled', true);
}