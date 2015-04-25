    function editMode(element) {
        $this = $(element);
        $this.parent().children('.non-edit').toggle();
        $this.parent().children('.edit-requirement').toggle();
        $this.siblings('input.edit-requirement').val($this.siblings('h3').text());
        $this.siblings('textarea.edit-requirement').val($this.siblings('h4').text())
    }

    function updateRequirement(element) {

        $this = $(element);
        $.ajax({
            method: "PUT",
            url: "/requirements/"+$this.attr('data-url-target'),
            data: {
                title: $this.siblings('input.edit-requirement').val(),
                description: $this.siblings('textarea.edit-requirement').text(),
                parent: $this.attr('data-parent'),
                id: $this.attr('data-id'),
                method: "update"
            }
        })
            .success(function (msg) {
            $this.siblings('h3').text($this.siblings('input.edit-requirement').val());
            $this.siblings('h4').text($this.siblings('textarea.edit-requirement').text());
            editMode($this);
        })

    }

    function addRequirement(element) {

        $this = $(element);
        $.ajax({
            method: "PUT",
            url: "/requirements/"+$this.attr('data-url-target'),
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


function removeRequirement(element){
$this = $(element);
 $.ajax({
            method: "PUT",
            url: "/requirements/"+$this.attr('data-url-target'),
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