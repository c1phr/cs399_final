function editMode(element){
    $this = $(element);
    $parent = $this.closest('.col-xs-4');
    $parent.children('.edit-mode').toggle();
    $parent.children('.non-edit').toggle();
}


function changeText(element) {
    var $this = $(element);
    $this.text($this.val())
}

function updateTask(element){
    $this = $(element);
    $.ajax({
        method: "PUT",
        url: "/tasks/"+$this.attr('data-requirement'),
        data: {
            requirement: $this.attr('data-requirement'),
            title: $this.siblings('input').val(),
            description: $this.siblings('textarea').text(),
            assignee: $this.siblings('#assigneeUpdate').val(),
            open: $this.siblings('#statusUpdate').val(),
            task_key: $this.attr('data-task-key')
        }
    })
        .success(function(data){
            editMode($this);
            $parent = $this.closest('.col-xs-4');
            $parent.find('h3').text($this.siblings('input').val());
            $parent.find('h4').text($this.siblings('textarea').text());
            $parent.find('.user-assigned').text($this.siblings('#assigneeUpdate').children(':selected').text());
        })
}

function addTask(element){
    $this = $(element);
    $.ajax({
        method: "PUT",
        url: "/tasks/"+$this.attr('data-requirement'),
        data: {
            requirement: $this.attr('data-requirement'),
            title: $('#addTaskTitle').val(),
            description: $('#addTaskDesc').val(),
            assignee: $('#assigneeNew').val(),
            open: "Open"
        }
    })
        .success(function(data){
            $('#taskModal').modal('hide');
             $('#addTaskTitle').val("");
            $('#addTaskDesc').val("");
            $('#assigneeNew').val("");
        })
}
