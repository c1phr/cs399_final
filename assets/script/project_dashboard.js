$('.addUser').click(function(){
    $.post("/ManageTeam",{project_id: $('#member-name').attr('data-project-id'), username: $('#member-name').val(), method: "put"});
})
$('.removeUser').click(function(){
    $.post("/ManageTeam",{project_id: $(this).closest('tr').attr('data-project-id'), username: $(this).closest('tr').attr('data-user'), method: "delete"}).done(function(msg){console.log(msg)});
})

$(function(){
    $.getJSON("/js/languages.min.json", function(languages){
            $(".language-bar").each(function(key, val){
                var language = $(this).data("language").toString();
                var percent = Math.round($(this).data("percent"));
                $(this).css("background-color", languages[language].color);
                $(this).attr("data-original-title", language + " " + percent + "%");
            });
        });
    $('[data-toggle="tooltip"]').tooltip();
});