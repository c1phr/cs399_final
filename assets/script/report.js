function filter_members(element){
    $this = $(element);
    if($this.val() == ""){
        $('tbody > tr').show();
    }
    else{
        $('tbody > tr').each(function(){
            if($(this).attr("data-filter-user") != $this.val()){
                $(this).hide();
            }
            else{
                $(this).show();
            }
        })
    }

}

function search_all(element){
    $this = $(element).val().toLowerCase();
    $('tbody > tr').each(function(){
        var search_val = $(this).attr("data-filter-all").toLowerCase();
        if(search_val.indexOf($this) >= 0){
            $(this).show();
        }
        else{
            $(this).hide();
        }
    })
}