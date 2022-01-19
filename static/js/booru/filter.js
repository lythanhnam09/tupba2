
function showFilterDailog(title, edit = false, id = 0, name = '', text = '') {
    let dialog = new Dialog(
        `<h2>${title}</h2>`, 
        `<div class="control-group vflex-center gap-1 mb-1">
            <label for="">Name: </label>
            <input id="inp-filter-name" type="text" class="form-control dark flex-grow" value="${name}">
        </div>
        <label for="">Filter query: </label>
        <textarea id="inp-filter-text" class="form-control dark w-100">${text}</textarea>`,
        [
            {
                html: '<button id="btn-dialog-ok" class="btn btn-primary">Save</button>',
                selector: '#btn-dialog-ok',
                onclick: function(dialog, button) {
                    let name = $('#inp-filter-name').val().trim();
                    let txt = $('#inp-filter-text').val().trim();
                    if (name != '' && txt != '') {
                        if (edit) {
                            socket.emit('edit_filter', {id:id, name: name, text: txt});
                        } else {
                            socket.emit('new_filter', {name: name, text: txt});
                        }
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

function deleteFilter(id, name) {
    if (confirm(`Delete filter "${name}" ?`)) {
        socket.emit('delete_filter', {id: id});
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