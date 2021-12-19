var connected = false;
var socket;

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
        updateTask(data);
    });

    socket.on('refresh_page', function(data) {
        location.reload();
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
            thtml += `
            <div class="task-item card bg-l10-darkblue mb-1">
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

function scrollToEl(selector, time = 2000) {
    $([document.documentElement, document.body]).animate({
        scrollTop: $(selector).offset().top
    }, time);
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
        ]) {
        
        this.title = title;
        this.content = content;
        this.buttons = buttons;

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
        for (let btn of this.buttons) {
            let dialog = this;
            $(btn.selector).click(function(el) {
                btn.onclick(dialog, el);
            });
        }
    }

    hide() {
        $('.dialog-container').remove();
    }
}