    $('.closeOpenIssue').click(function(){
        $this = $(this);
        $.post("/CloseIssue", {project: "{{project}}", issue_id:$this.attr('data-issue'), issue_title: $this.attr('data-title'), issue_body: $this.attr('data-body'), issue_assignee: $this.attr('data-assignee'), issue_milestone: $this.attr('data-milestone')}).done(function(msg) {
         console.log(msg);
        });


})