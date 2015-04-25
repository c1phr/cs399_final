 $('[data-toggle="tooltip"]').tooltip()

$('.addUser').click(function(){
    $.post("/ManageTeam",{project_id: $('#member-name').attr('data-project-id'), username: $('#member-name').val(), method: "put"});
})
$('.removeUser').click(function(){
    $.post("/ManageTeam",{project_id: $(this).closest('tr').attr('data-project-id'), username: $(this).closest('tr').attr('data-user'), method: "delete"}).done(function(msg){console.log(msg)});
})