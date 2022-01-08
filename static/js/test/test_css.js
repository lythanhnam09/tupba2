function changeCol() {
    var sz = $('#select-col').val();
    var md = $('#select-size').val();
    var num = $('#input-colnum').val();
    var cls = `col${md}${sz}-${num} changed px-1 my-1`;
    console.log('Set cards class to: ' + cls);
    $('.changed').attr('class', cls);
}

function setNavColor(color) {
    $('#navbar').attr('class', `nav ${color} pos-sticky-top shadow`);
    return false;
}

$(function() {
    changeCol();
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

    $('#getajax').click(async function() {
        setStat('stat1', false);
        setStat('stat2', false);
        setStat('stat3', false);
        setStat('stat4', false);
        $('#test1').val('');
        $('#test2').val('');
        $('#test3').val('');
        
        // try {
            const t1 = await getData('http://localhost:8080/api/test1');
            setStat('stat1', true);
            $('#test1').val(t1.message);
            const t2 = await getData('http://localhost:8080/api/test2');
            setStat('stat2', true);
            $('#test2').val(t2.message);
            const t3 = await getData('http://localhost:8080/api/test3');
            setStat('stat3', true);
            $('#test3').val(t3.message);

            setStat('stat4', true);
        // } catch (error) {
        //     console.log(error);
        // }
    });
});

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
            console.log(res);
        },
        error: function(e) {
            console.log(e);
        }
    });
}

function setStat(id, done = false) {
    $('#' + id).html(done ? 'Done':'Waiting...');
    $('#' + id).attr('class', done ? 'fg-body-success':'fg-body-warning');
}