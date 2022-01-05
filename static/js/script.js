var connected = false;
var socket;

var onSocketStatLoad = null;

$(function() {
    $('.card-foldable>.card-header').append('<i class="fas fa-chevron-up foldbutton"></i>');
    $('.card-foldable>.card-header').click(function() {
        if (! $(this).data('folded') || $(this).data('folded') == 0) {
            $(this).parent().children('.card-content').slideUp();
            $(this).children('.foldbutton').removeClass('fa-chevron-up');
            $(this).children('.foldbutton').addClass('fa-chevron-down');
            $(this).data('folded', '1');
        } else {
            $(this).parent().children('.card-content').slideDown();
            $(this).children('.foldbutton').removeClass('fa-chevron-down');
            $(this).children('.foldbutton').addClass('fa-chevron-up');
            $(this).data('folded', '0');
        } 
    });
    let mw = $('.image-square').width();
    $('.image-square').css('height', mw + 'px');

    connectSocket();

    $('.top-previous').each(function() {
        let je = $(this);
        let prev = je.prev();
        je.css('top', prev.offset().top + prev.height() - $(window).scrollTop() + 'px');
    });

    $(window).resize(function() {
        $('.top-previous').each(function() {
            let je = $(this);
            let prev = je.prev();
            je.css('top', prev.offset().top + prev.height() - $(window).scrollTop() + 'px');
        });
    });
});

function setSocketStat(stat, color) {
    $('#socket-stat').html(`Socket: ${stat}`);
    $('#socket').attr('class', `${color} p-1`);
}

function connectSocket() {
    socket = io.connect('http://' + document.domain + ':' + location.port);
    socket.on('connect', function() {
        setSocketStat('Connected', 'fg-success');
        connected = true;
        socket.emit('task_stat', {});
    });

    socket.on('connect_error', err => setSocketStat('Connection Error', 'fg-danger'));
    socket.on('connect_failed', err => setSocketStat('Connection Failed', 'fg-danger'));
    socket.on('disconnect', err => setSocketStat('Disconnected', 'fg-danger'));

    socket.on('task_data', function(data) {
        console.log(`Task data:`);
        console.log(data);
        updateTask(data);
        if (onSocketStatLoad != null) onSocketStatLoad(data);
    });

    socket.on('refresh_page', function(data) {
        console.log(`Refresh page: ${data.context}`);
        if (data.context == null) location.reload();
        else {
            if (data.context == location.pathname) location.reload();
        }
    });

    socket.on('throw_error', function(data) {
        console.log(data.message);
    });
}

function updateTask(data) {
    if (data.count == 0) {
        $('#task-count').html('No task');
        $('#task-list').html('');
    } else {
        $('#task-count').html(`${data.count} tasks`);

        let thtml = '';
        let cnt = 0;
        for (let task of data.tasks) {
            let per = (task.progress / task.count * 100).toFixed(2);
            let prog = cnt == 0 ? `${per}% (${task.progress}/${task.count})`:`Awaiting (${task.count})`;
            // if (`#task-${task.id}`) {

            // }
            thtml += `
            <div id="task-${task.id}" class="task-item card bg-l10-darkblue mb-1">
                <div class="card-content">
                    <div class="task-stat">
                        <div class="task-tag tag-${task.category.toLowerCase()}">${task.category}</div>
                        <div class="task-progress">${prog}</div>
                    </div>
                    
                    <div class="task-name">${task.name}</div>
                    <div class="progress-bar">
                        <div class="value bg-warning" style="width:${per}%"></div>
                    </div>
                </div>
            </div>
            `;
            cnt++;
        }
        $('#task-list').html(thtml);
    }
}

function getData(link) {
    return $.ajax({
        url: link,
        type: 'GET',
        dataType:'json',
        crossDomain: true,
        xhrFields: {
            withCredentials: true
        },
        success: function(res) {
            //console.log(res);
        },
        error: function(e) {
            console.log(e);
        }
    });
}

function getBaseUrl() {
    let url = window.location.href;
    let start = url.indexOf('/') + 2;
    let end = url.indexOf('/', start) == -1 ? url.length-1:url.indexOf('/', start)
    return url.substring(start, end);
}

function toggleSidebar() {
    $('#sidebar').toggleClass('show');
}

function toggleExpandable(id, buttonid, leftAlign = true) {
    var exp = $(`#${id}`);
    var button = $(`#${buttonid}`);
    if (leftAlign) exp.css('left', button.position().left);
    exp.css('top', button.innerHeight());
    //exp.toggleClass('show');
    exp.slideToggle(300);
}

function checkClickOutside(e, container) {
    return !container.is(e.target) && container.has(e.target).length === 0
}

function registerMenuDismiss(e, container, button, f) {
    if (checkClickOutside(e, button) && checkClickOutside(e, container)) f(container);
}

$(document).mouseup(function(e) 
{
    registerMenuDismiss(e, $('#sidebar'), $('#btn-menu'), (con) => con.removeClass('show'));
    registerMenuDismiss(e, $('#exp-left'), $('#btn-exp-left'), (con) => con.slideUp(300));
    registerMenuDismiss(e, $('#exp-right'), $('#btn-exp-right'), (con) => con.slideUp(300));
});

function scrollToEl(selector, time = 2000, offset = 0) {
    if (time == 0) {
        document.documentElement.scrollTop = $(selector).offset().top + offset;
    } else {
        $([document.documentElement, document.body]).animate({
            scrollTop: $(selector).offset().top + offset
        }, time);
    }
}

class Dialog {
    constructor(
        title = 'Dialog title', content = 'Some random message', 
        buttons = [
            {
                html: '<button id="btn-dialog-ok" class="btn btn-primary">OK</button>',
                selector: '#btn-dialog-ok',
                onclick: function() {
                    console.log('Dialog ok');
                }
            }
        ], dismissOutside = true, dismissButton = true) {
        
        this.title = title;
        this.content = content;
        this.buttons = buttons;
        this.dismissOutside = dismissOutside;
        this.dismissButton = dismissButton;
    }

    show() {
        let buttonHtml = '';
        for (let btn of this.buttons) {
            buttonHtml += btn.html;
        }
        $(`
        <div class="dialog-container">
            <div class="dialog">
                <div class="title">
                    ${this.title}
                </div>
                <div class="content">
                    ${this.content}
                </div>
                <div class="dialog-button">
                    ${buttonHtml}
                </div>
            </div>
        </div>
        `).insertBefore('body');
        let dialog = this;
        for (let btn of this.buttons) {
            $(btn.selector).click(function(el) {
                btn.onclick(dialog, el);
                if (dialog.dismissButton) dialog.hide();
            });
        }
        if (this.dismissOutside) {
            $('.dialog').click(function(el) {
                return false;
            });
            $('.dialog-container').click(function(el) {
                dialog.hide();
            });
        }
    }

    hide() {
        $('.dialog-container').remove();
    }
}

class Queue {
    constructor() {
        this.data = [];
    }

    enqueue(data) {
        this.data.push(data);
    }

    dequeue() {
        if (this.data.length <= 0) return null;
        let el = this.data[0];
        this.data.splice(0, 1);
        return el;
    }

    doLimit(limit) {
        if (this.data.length > limit) {
            let count = this.data.length - limit;
            for (let i=0;i<count;i++) this.dequeue();
        }
    }

    get length() {
        return this.data.length;
    }
}

class PagePreLoader {
    constructor(perpage, request, range = 1, cacheSize = 4) {
        // request: function(page, perpage) -> Future<Page>
        this.page = 1;
        this.perpage = perpage;
        this.request = request;
        this.range = range;
        this.pageCount = 1;
        this.cacheSize = cacheSize;
        this.pageData = new Queue();
    }

    checkPageLoaded(page, perpage) {
        for (let pg of this.pageData.data) {
            if (page == pg.page_num && perpage == pg.per_page) return pg;
        }
        return null;
    }

    async doRequest(page, perpage) {
        console.log(`Loading page ${page}...`);
        let result = this.checkPageLoaded(page, perpage);
        if (! result) {
            let data = await this.request(page, perpage);
            this.receiveData(data);
            return data;
        }
        console.log(`Page ${page} already loaded`);
        return result;
    }

    receiveData(data) {
        // console.log(data);
        console.log(`Page ${data.page_num} received`);
        this.pageCount = data.page_count;
        this.pageData.enqueue(data);
        this.pageData.doLimit(this.cacheSize);
        console.log(this.pageData.data);
    }

    async get(page) {
        console.log(` * Requesting page ${page}...`);
        this.page = page;
        let result = await this.doRequest(page, this.perpage);
        for (let i=1;i<=this.range;i++) {
            if (page + i <= this.pageCount) this.doRequest(page + i, this.perpage);
            if (page - i >= 1) this.doRequest(page - i, this.perpage);
        }
        console.log(`Done`);
        return result;
    }
}