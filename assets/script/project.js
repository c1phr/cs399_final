    $('.project_submit').click(function () {
        var $this = $(this);
        $.post('/project', {
            id: parseInt($(this).attr('data-project-id')),
            name: $(this).attr('data-project-name'),
            desc: $(this).attr('data-project-desc')
        })
            .success(function () {
            $this.attr('disabled', true);
            console.log("disabled");
            $('.project-success').fadeIn(1500).fadeOut(4000);
        })
    })
