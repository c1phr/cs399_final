function GenerateUserReport(user){
    $.get("/report/user/" + user)
        .done(function(data){
            var parsed_data = $.parseJSON(data);
            console.log(parsed_data);

            //$.each(data, function(key, val){
            //    $('body').append(val);
            //})


        })
}