

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


    function flashMessage(message) {
        var messageElement = $("<div>");
        messageElement.text(message);
        messageElement.addClass("to-fade");
        messageElement.css({
            "color": "black",
            "display": "block",
            "background-color": "white",
            "margin": "10px",
            "padding": "10px 20px",
            "width": "calc(100% - 40px)",
            "text-align": "center",
            "border-radius": "5px"});
        messageElement.insertAfter("header");
    
        $(".to-fade").fadeOut(6000);
        };
    


    $("header .save").on("click", function(){
        if (!$("#title").val()) $("#title").val("Untitled Recipe");
        var submitted_title = $("#title").val();

        if (!$("#ds").val()) $("#ds").val("No description");
        var submitted_ds = $("#ds").val();

        if (!$("#notes").val()) $("#notes").val("No notes");
        var submitted_notes = $("#notes").val();

        if (!$("#txt").val()) $("#txt").val("No ingredients");
        var submitted_txt = $("#txt").val();

        if (!$("#txtarea").val()) $("#txtarea").val("No instructions");
        var submitted_txtarea = $("#txtarea").val();

        var user_id;

        $.ajax({
            url: "http://0.0.0:5001/status",
            type: "GET",
            Headers: {
                "Access-Control-Allow-Origin": "0.0.0.0:5001",
            }
        }).done(function(json) {
            if (json.status === "logged") {
                user_id = json.id;
            }
        });

        if (!user_id) {
            flashMessage("You must be logged in to save a recipe.");
            return;
        }

        var recipe = {
            title: submitted_title,
            ds: submitted_ds,
            notes: submitted_notes,
            txt: submitted_txt,
            txtarea: submitted_txtarea
        };

        console.log(recipe);
        
        
        localStorage.clear();
    });
});