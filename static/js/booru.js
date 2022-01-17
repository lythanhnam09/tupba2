var timer = null;

$(function() {
    parseMarkup('#text-description');
    // $('#filter-select').change(function() {
    //     let id = $('#filter-select').val();
    //     $.post( "/booru/api/config/filter", {'filter_id':id}).done(function( data ) {
    //         console.log('OK');
    //         location.reload();
    //     }).fail(function() {
    //         console.log("Error");
    //     });
    // });

    $('#q').keyup(function() {
        if ($('#tag-suggest').data('folded') == '1') return;
        if (timer != null) {
            clearTimeout(timer);
        }
        timer = setTimeout(async function() {
            let text = $('#q').val();
            let name = getSearchTag(text).name;

            timer = null;

            data = await socketEmitGet('search_tag', {name: name}, true);
            let suggestHtml = '';
            for (let tag of data) {
                suggestHtml += `<span class="booru-tag ${tag.cols.color}" onclick="fillResult('${tag.cols.name}')">${tag.cols.name}</span> `;
            }
            $('#tag-suggestion').html(suggestHtml);
            
        }, 500);
    });

    // $('.mdropdown').click(function() {
    //     let id = $(this).data('id');
    //     let show = $(this).data('show');
    //     if (show == 0) {
    //         $(this).data('show', 1);
    //         $(`#dropdown-${id}`).slideDown();
    //     } else {
    //         $(this).data('show', 0);
    //         $(`#dropdown-${id}`).slideUp();
    //     }
    // });
});

function getSearchTag(text) {
    let start = text.lastIndexOf(',') + 1;
    let end = text.length
    if (start == -1) {
        start = 0;
    }
    let res = text.substring(start, end).trim();
    let type = '';
    if (res.length > 0 && ['-', '`', '+'].includes(res[0])) {
        type = res[0];
        res = res.substring(1, res.length);
    }
    return {name:res, type:type};
}

function fillResult(tag) {
    let text = $('#q').val();
    let current = getSearchTag(text);
    let start = text.lastIndexOf(',') + 1;
    let res = text.substring(0, start);
    res += ` ${current.type}${tag}`;
    $('#q').val(res.trim());
}

var currentPage = -1;
var nextPage = -1;
var prevPage = -1;
var pageCount = 0;
var imgId = 0;

function loadComment(id, page) {
    imgId = id;
    $('#comment-button > button').html('Loading comment...');
    $('#comment-button > button').prop('disabled', true);
    
    $('#first-comment').prop('disabled', true);
    $('#last-comment').prop('disabled', true);
    $('#next-comment').prop('disabled', true);
    $('#prev-comment').prop('disabled', true);

    $('#comment-page-num').html(`Loading page ${page}...`);

    $.getJSON(`https://derpibooru.org/api/v1/json/search/comments?q=image_id:${id}&page=${page}&filter_id=56027`).done(function(data) {
        // console.log(data);

        pageCount = Math.ceil(data.total / 25);
        currentPage = page;
        $('#first-comment').prop('disabled', false);
        $('#last-comment').prop('disabled', false);
        $('#next-comment').prop('disabled', false);
        $('#prev-comment').prop('disabled', false);
        if (pageCount <= 1) {
            $('#first-comment').prop('disabled', true);
            $('#last-comment').prop('disabled', true);
            $('#next-comment').prop('disabled', true);
            $('#prev-comment').prop('disabled', true);
            if (pageCount == 0) {
                $('#comment-button').show();
                $('#comment-button > button').html('No comment');
                $('#comment-button > button').prop('disabled', false);
                return;
            }
        } else {
            if (currentPage - 1 < 1) {
                prevPage = -1;
                $('#prev-comment').prop('disabled', true);
            } else {
                prevPage = currentPage - 1;
            }
            if (currentPage + 1 > pageCount) {
                nextPage = -1;
                $('#next-comment').prop('disabled', true);
            } else {
                nextPage = currentPage + 1;
            }
            $('#prev-comment').attr('onclick', `loadComment(${imgId}, ${prevPage})`);
            $('#next-comment').attr('onclick', `loadComment(${imgId}, ${nextPage})`);
            $('#first-comment').attr('onclick', `loadComment(${imgId}, ${1})`);
            $('#last-comment').attr('onclick', `loadComment(${imgId}, ${pageCount})`);
        }

        $('#comment-page-num').html(`Page ${currentPage} of ${pageCount}`);

        $('#comment-button').hide();

        commentHtml = '';
        for (comment of data.comments) {
            commentHtml += `
            <div class="card mb-1">
                <div class="row">
                    <div class="col-2 p-2 col flex-center">
                        <div class="img-container w-75">
                            <img src="${comment.avatar}" alt="avatar">
                        </div>
                        <div class="">
                            <h3 class="fg-body-primary">${comment.author}</h3>
                            <h5>${comment.created_at}</h5>
                        </div>
                    </div>
                    <div class="col-10 p-2">
                        ${comment.body}
                    </div>
                </div>
            </div>
            `;
        }
        commentHtml += `
            <div class="my-2">
                <button class="btn btn-primary" onclick="scrollToComment()"><i class="fas fa-chevron-up"></i> Scroll to top comment</button>
            </div>
        `;
        $('#comment-container').html(commentHtml);
        $('#comment-container').show();
        $('#comment-page').show();

    }).fail(function(e) {
        console.log('Error');
        $('#comment-button').show();
        $('#comment-button > button').html('Error (Try again)');
        $('#comment-button > button').prop('disabled', false);
    });
}

function scrollToComment() {
    $([document.documentElement, document.body]).animate({
        scrollTop: $("#comment-page").offset().top - 50
    }, 750);
}

function deleteImage(id, reload = true) {
    $.get(`/booru/api/delete/${id}`).done((data) => {
        console.log(data);
        if (reload) location.reload();
    }).fail((e) => {
        console.log('Error');
    });
}

function showPageDialog(page, pagecount, formid='form-filter') {
    $('#btn-goto-page').prop('disabled', true);
    let selectHtml = '';
    let start = page - 10;
    let end = page + 10;
    if (start < 1) start = 1;
    if (end > pagecount) end = pagecount;
    for (let i=start;i<=end;i++) {
        selectHtml += `<option value="${i}"${i == page ? ' selected':''}>Page ${i}</option>`;
    }
    // <label>Page (max ${pagecount}): </label><input class="form-control" type="number" id="inp-goto-page" max="${pagecount}" min="1" value="${page}">
    let dialog = new Dialog(
        '<h3>Goto page</h3>', 
        `<select id="select-goto-page" class="form-control w-100">${selectHtml}</select>`,
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

function setVideoMode(mode) {
    $('.btn-mode').prop('disabled', false);
    $('#btn-mode-' + mode).prop('disabled', true);
    $('.btn-size').data('mode', mode);
    let link = $('#img-display').attr('src');
    if (mode == 1) {
        link = link.replaceAll('.webm', '.mp4');
    }
    $('#img-display').attr('src', link);
    let vid = document.querySelector('#video-display');
    vid.load();
    vid.play();
}

function changeImageSize(index, link = null, extension = 'png') {
    let btn = $('#btn-size-' + index);
    $('.btn-size').prop('disabled', false);
    btn.prop('disabled', true);
    if (link != null) {
        if (! ['webm', 'mp4'].includes(extension)) {
            let lastText = btn.text();
            btn.text(`Loading ${lastText}`);
            let img = new Image();
            img.src = link;
            img.onload = function() {
                btn.text(lastText);
            }
        }
        if (btn.data('mode') == 1) {
            link = link.replaceAll('.webm', '.mp4');
        }
        $('#img-display').attr('src', link);
    } else {
        link = $('#img-display').attr('src');
    }

    if (['webm', 'mp4'].includes(extension)) {
        if (btn.data('mode') == 1) {
            link = link.replaceAll('.webm', '.mp4');
        }
        $('#img-display').attr('src', link);
        let vid = document.querySelector('#video-display');
        vid.load();
        vid.play();
    }
    
}

function parseMarkup(selector) {
    let e = $(selector);
    if (e.length <= 0) return;
    let txt = e.text();
    txt = txt.replaceAll(/\[(.*)\]\((.*)\)/gm, '<a href="$2">$1</a>'); // Link
    txt = txt.replaceAll(/>>(\d+)[stp]?/gm, '<a href="/booru/view/$1">&gt;&gt;$1</a>'); // Booru Link
    txt = txt.replaceAll(/\*\*(.*?)\*\*/gm, '<b>$1</b>'); // Bold
    txt = txt.replaceAll(/~~(.*?)~~/gm, '<span class="spoiler">$1</span>'); // Spoiler
    txt = txt.replaceAll(/__(.*?)__/gm, '<u>$1</u>'); // Underline
    txt = txt.replaceAll(/[\*_](.*?)[\*_]/gm, '<i>$1</i>'); // Italic
    txt = txt.replaceAll(/\^(.*?)\^/gm, '<sup>$1</sup>'); // Super script
    txt = txt.replaceAll(/\%(.*?)\%/gm, '<sub>$1</sub>'); // Sub script
    txt = txt.replaceAll(/^> (.*)/gm, '<span class="quote">$1</span>'); // Quote
    txt = txt.replaceAll('\n', '<br>');
    e.html(txt);
}