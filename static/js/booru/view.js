$(function() {

});

let lsAlbum = [];

class AlbumCheckItem {
    constructor(id, name, count, checked = false, disabled = false) {
        this.name = name;
        this.count = count
        this.checked = checked;
        this.disabled = disabled;
        this.id = id;
    }

    update() {
        let e = $(`#ck-album-${this.id}`)
        if (this.checked) {
            if (this.disabled) {
                e.css('border-left', '5px solid grey');
            } else {
               e.css('border-left', '5px solid green');
            }
        }
        else e.css('border-left', 'none');
        if (this.disabled) {
            e.off('click');
            $(`#ck-album-${this.id} label`).addClass('fg-secondary');
        }
    }

    toHtml() {
        let html = `
        <div class="card my-05 bg-dark" id="ck-album-${this.id}">
            <div class="card-content p-1 bg-dark">
                <div class="control-group vflex-center gap-1">
                    <label class="flex-grow">${this.name}</label>
                    <div>
                        <div class="d-iblock fg-success mr-1"><i class="fas fa-image"></i> ${this.count}</div>
                    </div>
                </div>
            </div>
        </div>
        `;
        
        return html;
    }

    setEvent() {
        let item = this;
        $(`#ck-album-${this.id}`).on('click', function() {
            item.checked = !item.checked;
            item.update();
        });
    }
}

async function showAlbumDialog(id) {
    let albumHtml = '';
    lsAlbum = [];
    ls = await socketEmitGet('add_album_list', {id:id}, true);
    ls.forEach(album => {
        let ai = new AlbumCheckItem(album.cols.id, album.cols.name, album.cols.image_count, album.cols.is_added, album.cols.is_added);
        albumHtml += ai.toHtml();
        lsAlbum.push(ai);
    });
    let dialog = new Dialog(
        `<h2>Select albums to add</h2>`, 
        `${albumHtml}`,
        [
            {
                html: '<button id="btn-dialog-ok" class="btn btn-primary">Save</button>',
                selector: '#btn-dialog-ok',
                onclick: function(dialog, button) {
                    let lsid = [];
                    lsAlbum.forEach(ai => {
                        if (ai.checked && !ai.disabled) lsid.push(ai.id);
                    });
                    if (lsid.length > 0) socket.emit('add_to_albums', {pid:id, lsid:lsid});
                    dialog.hide();
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
    lsAlbum.forEach(ai => {
        ai.setEvent();
        ai.update();
    });
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

function favorite(id) {
    socket.emit('fav_booru_pic', {id: id});
}