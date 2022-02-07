
function showAlbumDailog(title, edit = false, id = 0, name = '') {
    let dialog = new Dialog(
        `<h2>${title}</h2>`, 
        `<div class="control-group vflex-center gap-1 mb-1">
            <label for="">Name: </label>
            <input id="inp-album-name" type="text" class="form-control dark flex-grow" value="${name}">
        </div>`,
        [
            {
                html: '<button id="btn-dialog-ok" class="btn btn-primary">Save</button>',
                selector: '#btn-dialog-ok',
                onclick: function(dialog, button) {
                    let name = $('#inp-album-name').val().trim();
                    if (name != '') {
                        if (edit) {
                            socket.emit('edit_album', {id:id, name: name});
                        } else {
                            socket.emit('add_album', {name: name});
                        }
                        $('#btn-dialog-ok').prop('disabled', true);
                        $('#btn-dialog-ok').html('Please wait');
                    }
                }
            },
            {
                html: '<button id="btn-dialog-cancel" class="btn btn-secondary">Cancel</button>',
                selector: '#btn-dialog-cancel',
                onclick: function(dialog, button) {
                    dialog.hide();
                }
            }
        ], 'bg-dark', true, false);
    dialog.show();
}

function swapFilterOrder(id1, id2) {
    socket.emit('swap_filter', {id1: id1, id2: id2});
}

function deleteAlbum(id, name) {
    if (confirm(`Delete album "${name}" ?`)) {
        socket.emit('delete_album', {id: id});
    }
}

function saveFilter() {
    let ls = []
    $('.ck-filter').each((index, e) => {
        if ($(e).prop('checked')) {
            let id = $(e).data('id');
            ls.push(parseInt(id));
        }
    });
    socket.emit('save_filter', {filters: ls});
}