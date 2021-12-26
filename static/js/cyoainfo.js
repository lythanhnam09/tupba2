$(document).ready(function() {
    $('.nav-progress').hide();
});

function refreshThreadData(cyoaId, force = false) {
    socket.emit('cyoa_thread_refresh', {id: cyoaId, force: force});
    // $('#btn-refresh').html('<i class="fas fa-ellipsis-h"></i>');
    // $('#btn-refresh').prop('disabled', true);
    // $('#btn-refresh-all').prop('disabled', true);
    // $('#btn-download-img').prop('disabled', true);
    $('.reload-disable').each(function() {
        $(this).prop('disabled', true);
        if ($(this).prop('tagName') == 'A') {
            $(this).addClass('btn-disabled');
            $(this).removeAttr('href');
        }
    });
}