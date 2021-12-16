var timer = null;

$(function() {
    $('#filter-select').change(function() {
        let id = $('#filter-select').val();
        $.post( "/booru/api/config/filter", {'filter_id':id}).done(function( data ) {
            console.log('OK');
            location.reload();
        }).fail(function() {
            console.log("Error");
        });
    });

    $('#q').keyup(function() {
        if ($('#tag-suggest').data('folded') == '1') return;
        if (timer != null) {
            clearTimeout(timer);
        }
        timer = setTimeout(function() {
            let text = $('#q').val();
            let name = getSearchTag(text).name;
            //console.log();
            $.getJSON(`http://${getBaseUrl()}/booru/api/tag/search?name=${name}`).done(function(data) {
                console.log(data);
                let suggestHtml = '';
                for (let tag of data) {
                    suggestHtml += `<span class="booru-tag tag-${tag.cols.color}" onclick="fillResult('${tag.cols.name}')">${tag.cols.name}</span> `;
                }
                $('#tag-result').html(suggestHtml);
            }).fail(function() {
                console.log("Error getting search data");
            });
            timer = null;
        }, 500);
    });

    $('.mdropdown').click(function() {
        let id = $(this).data('id');
        let show = $(this).data('show');
        if (show == 0) {
            $(this).data('show', 1);
            $(`#dropdown-${id}`).slideDown();
        } else {
            $(this).data('show', 0);
            $(`#dropdown-${id}`).slideUp();
        }
    });
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