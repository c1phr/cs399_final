    function editMode(element) {
        $this = $(element);
        $this.toggle();
        $this.siblings('.edit-requirement').toggle();
        $this.siblings(".panel-body").children('.non-edit').toggle();
        $this.siblings(".panel-body").children('.edit-requirement').toggle();
        $this.siblings('.panel-body').children('input.edit-requirement').val($this.siblings('.panel-heading').children('h3').text());
        $this.siblings('.panel-body').children('textarea.edit-requirement').val($this.siblings('.panel-body').children('p').text());
    }

    function updateRequirement(element) {

        $this = $(element);
        $.ajax({
            method: "PUT",
            url: "/requirements/" + $this.attr('data-url-target'),
            data: {
                title: $this.siblings('input.edit-requirement').val(),
                description: $this.siblings('textarea.edit-requirement').text(),
                parent: $this.attr('data-parent'),
                id: $this.attr('data-id'),
                method: "update"
            }
        })
            .success(function (msg) {
            $this.siblings('.panel-body').children('input.edit-requirement').val($this.siblings('.panel-heading').children('h3').text());
            $this.siblings('.non-edit').toggle();
            $this.siblings('.edit-requirement').toggle();
            $this.parent().siblings('.panel-heading').children('h3').text($this.siblings('input.edit-requirement').val());
            $this.siblings('p').text($this.siblings('textarea.edit-requirement').val());
            $this.parent().siblings('.non-edit').toggle();
            $this.parent().siblings('.edit-requirement').toggle();

                $this.toggle();
        })

    }

    function addRequirement(element) {

        $this = $(element);
        $.ajax({
            method: "PUT",
            url: "/requirements/" + $this.attr('data-url-target'),
            data: {
                title: $this.siblings('input').val(),
                description: $this.siblings('textarea').text(),
                parent: $this.siblings('select').val(),
                project: $this.attr('data-id'),
                method: "Add"
            }
        })
            .success(function (msg) {
            $('#addRequirement').modal('hide')
        })

    }


    function removeRequirement(element) {
        $this = $(element);
        $.ajax({
            method: "PUT",
            url: "/requirements/" + $this.attr('data-url-target'),
            data: {
                id: $this.attr('data-id'),
                method: "delete"
            }
        })
            .success(function (msg) {
            $this.parent().remove();
        })
    }

    function changeText(element) {
        var $this = $(element);
        $this.text($this.val())
    }