

$(function() {
    var savedValue = localStorage.getItem('textareaValue');
    if (savedValue) {
        $("#txtarea").val(savedValue);
    }

    var title = localStorage.getItem("title");
    if (title) {
        $("#title").val(title);
    }

    $("#title").on("input", function() {
        localStorage.setItem("title", $(this).val());
        if (this.scrollHeight > this.clientHeight) {
            $(this).css({
                "height": this.scrollHeight + "px",
            });
        } else {
            $(this).css({
                "height": "auto",
            });
        }
    });

    var ds = localStorage.getItem("ds");

    if (ds) {
        $("#ds").val(ds);
    }
    
    $("#ds").on("input", function() {
        localStorage.setItem("ds", $(this).val());
        if (this.scrollHeight > this.clientHeight) {
            $(this).css({
                "height": this.scrollHeight + "px",
            });
        } else {
            $(this).css({
                "height": "auto",
            });
        }
    });

    var notes = localStorage.getItem("notes");
    if (notes) {
        $("#notes").val(notes);
    }

    $("#notes").on("input", function() {
        localStorage.setItem("notes", $(this).val());
        if (this.scrollHeight > this.clientHeight) {
            $(this).css({
                "height": this.scrollHeight + "px",
            });
        } else {
            $(this).css({
                "height": "auto",
            });
        }
    });

    var txt = localStorage.getItem("txt");
    if (txt) {
        $("#txt").val(txt);
    }

    $("#txt").on("input", function() {
        localStorage.setItem("txt", $(this).val());
        if (this.scrollHeight > this.clientHeight) {
            $(this).css({
                "height": this.scrollHeight + "px",
            });
        } else {
            $(this).css({
                "height": "auto",
            });
        }
    });

    var txtarea = localStorage.getItem("txtarea");
    if (txtarea) {
        $("#txtarea").val(txtarea);
    }

    $("#txtarea").on("input", function() {
        localStorage.setItem("txtarea", $(this).val());
        if (this.scrollHeight > this.clientHeight) {
            $(this).css({
                "height": this.scrollHeight + "px",
            });
        } else {
            $(this).css({
                "height": "auto",
            });
        }
    });




    $("header .save").on("click", function(){
        /*code to send to api goes here*/
        localStorage.clear();
    });
});