

function refreshCyoaData() {
    socket.emit('cyoa_refresh', {});
    $('#btn-refresh').html('<i class="fas fa-ellipsis-h"></i>');
    $('#btn-refresh').attr('class', 'btn btn-disabled mr-1')
    $('#btn-refresh').prop('onclick', false);
}

function refreshThreadData(cyoaId, force = false) {
    socket.emit('cyoa_thread_refresh', {id: cyoaId, force: force});
    // $('#btn-refresh').html('<i class="fas fa-ellipsis-h"></i>');
    $('#btn-refresh').prop('disabled', true);
    $('#btn-refresh-all').prop('disabled', true);
    $('#btn-download-img').prop('disabled', true);
}

function showPageDialog(page, pagecount, formid='form-filter') {
    $('#btn-goto-page').prop('disabled', true);
    let pageHtml = '';
    for (let i=1;i<=pagecount;i++) {
        pageHtml += `<option value="${i}"${i == page ? ' selected':''}>Page ${i}</option>`
    }
    let dialog = new Dialog(
        '<h3>Goto page</h3>', 
        `<select id="select-goto-page" class="form-control w-100">${pageHtml}</select>`,
        [
            {
                html: '<button id="btn-dialog-ok" class="btn btn-primary">OK</button>',
                selector: '#btn-dialog-ok',
                onclick: function(dialog, button) {
                    $('#btn-goto-page').prop('disabled', false);
                    $('input[name=page]').val($('#select-goto-page').val());
                    $(`#${formid}`).submit();
                }
            },
            {
                html: '<button id="btn-dialog-cancel" class="btn btn-secondary">Cancel</button>',
                selector: '#btn-dialog-cancel',
                onclick: function(dialog, button) {
                    $('#btn-goto-page').prop('disabled', false);
                }
            }
        ]);
    dialog.show();
}

function changePerpage(formid = 'form-filter', id='select-perpage') {
    $('input[name=perpage]').val($(`#${id}`).val());
    $('input[name=page]').val('1');
    $(`#${formid}`).submit();
}

function gotoPage(num, formid = 'form-filter') {
    $('input[name=page]').val(num);
    $(`#${formid}`).submit();
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
        scrollToEl(image, 0, -48);
    } else {
        img.addClass('expand');
    }
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