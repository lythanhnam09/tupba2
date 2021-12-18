

function refreshCyoaData() {
    socket.emit('cyoa_refresh', {});
    $('#btn-refresh').html('<i class="fas fa-ellipsis-h"></i>');
    $('#btn-refresh').attr('class', 'btn btn-disabled mr-1')
    $('#btn-refresh').prop('onclick', false);
}

function showPageDialog(page, pagecount) {
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
                    $('#form-filter').submit();
                    dialog.hide();
                }
            },
            {
                html: '<button id="btn-dialog-cancel" class="btn btn-secondary">Cancel</button>',
                selector: '#btn-dialog-cancel',
                onclick: function(dialog, button) {
                    $('#btn-goto-page').prop('disabled', false);
                    dialog.hide();
                }
            }
        ]);
    dialog.show();
}

function changePerpage() {
    $('input[name=perpage]').val($('#select-perpage').val());
    $('input[name=page]').val('1');
    $('#form-filter').submit();
}