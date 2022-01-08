let imgLoader = null;
let centerImg = null;
let imgControl = null;
let zoomScroll = null;

let currentIndex = 0;
let currentPage = 0;
let perPage = 0;
let totalCount = 0;
let currentData = null;

async function showImageView(cyoaId, page, pagecount, total, perpage, q, index) {
    if (imgLoader == null) {
        imgLoader = new PagePreLoader(perpage, (page, perpage) => socketEmitGet('cyoa_image_data', {page:page, perpage:perpage, cyoaId:cyoaId, q:q}, true));
    }
    perPage = perpage;
    currentIndex = index;
    totalCount = total;
    currentPage = page;
    $('#image-view').show();
    currentData = await imgLoader.get(page);
    // console.log(data);
    $('#image-view-image').attr('src', currentData.data[index].cols.link);
    resetImageView();
    // $('.image-view-main').on('click', (event) => {
    //     $('#image-view').hide();
    // });
}

function closeImageView() {
    $('#image-view').hide();
}

async function viewNext() {
    if (currentIndex + 1 < totalCount) {
        currentIndex++;
        if (currentIndex >= perPage) {
            currentIndex = 0;
            currentPage++;
            currentData = await imgLoader.get(currentPage);
        }
        $('#image-view-image').attr('src', currentData.data[currentIndex].cols.link);
        resetImageView()
    }
}

async function viewPrevious() {
    if (currentIndex - 1 >= 0) {
        currentIndex--;
        if (currentIndex < 0) {
            currentIndex = perPage - 1;
            currentPage--;
            currentData = await imgLoader.get(currentPage);
        }
        $('#image-view-image').attr('src', currentData.data[currentIndex].cols.link);
        resetImageView()
    }
}

function resetImageView() {
    centerImg.setPos(0, 0);
    centerImg.resetScale();
    centerImg.updateOrgSize();
    zoomScroll.value = 100;
    $('#zoom-per').text(zoomScroll.value.toFixed(0) + '%');
}

$(function() {
    centerImg = new ScalableDrag('#image-view-drag', {
        relative: true
    });

    imgControl = new GestureDetector('#image-control-drag', {
        mouseMove: (e, pos) => {
            let p = $('#image-view-control').position();
            $('#image-view-control').css('left', (p.left + e.delta.x) + 'px');
            $('#image-view-control').css('top', (p.top + e.delta.y) + 'px');
        }
    });

    zoomScroll = new SwipeScrollbar('#image-control-zoom', {
        min: 50,
        max: 400,
        value: 100,
        scale: 0.25,
        mouseMove: (e, pos) => {
            centerImg.setScale(e.value / 100);
            $('#zoom-per').text(e.value.toFixed(0) + '%');
        }
    })
});