// $(function() {

// });

function refreshCyoaData() {
    socket.emit('cyoa_refresh', {});
    $('#btn-refresh').html('<i class="fas fa-ellipsis-h"></i>');
    $('#btn-refresh').attr('class', 'btn btn-disabled mr-1')
    $('#btn-refresh').prop('onclick', false);
}