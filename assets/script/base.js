    $(document).ready(function(){
        //$('body').css("background", "white");
        $('#breadcrumbs').css({marginLeft: $('#sidebar').width() + 10});
        $('.topContainer').css({paddingLeft: $('aside').width()})

        $.get('/login');
        $(window).resize(function(){
            $('#breadcrumbs').css({marginLeft: $('#sidebar').width() + 10});
            $('.topContainer').css({paddingLeft: $('aside').width()})

        })
    })