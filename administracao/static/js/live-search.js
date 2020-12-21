$('.live-search-list a').each(function(){
   $(this).attr('data-search-term', $(this).text().toLowerCase());
});

$('.live-search-box').on('keyup', function(){
    let searchTerm = $(this).val().toLowerCase();

    $('.live-search-list a').each(function(){
        if ($(this).filter('[data-search-term *= ' + searchTerm + ']').length > 0 || searchTerm.length < 1) {
            $(this).show();
        } else {
            $(this).hide();
        }
    });
});