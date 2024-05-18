

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


    function flashMessage(message, position=null) {
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
        if (position) {
            messageElement.insertAfter(position);
        } else {
            messageElement.insertAfter("header");
        }
    
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

        
        $.ajax({
            url: "https://web-02.monadoll.tech/status",
            type: "GET",
            Headers: {
                "Access-Control-Allow-Origin": "http://0.0.0.0:5000",
            }
        }).done(function(json) {

            if (json.status === "logged") {
                var user_id = json.id;
                console.log("user creation and user is logged in")
            }


            if (!user_id) {
                flashMessage("You must be logged in to save a recipe.");
                return;
            }

            /*var favorite;
            if ($(".switch checkbox").is(":isChecked")) {
                favorite = true;
            } else {
                favorite = false;
            }*/

            var recipe = {
                "user_id": user_id,
                "title": submitted_title,
                "introduction": submitted_ds,
                "notes": submitted_notes,
                "ingredients": submitted_txt,
                "instructions": submitted_txtarea
            };

            $.ajax({
                url: "https://web-02.monadoll.tech/api/v1/users/" + user_id + "/recipes",
                type: "POST",
                data: JSON.stringify(recipe),
                contentType: "application/json",
                headers: {
                    "Access-Control-Allow-Origin": "52.91.120.169",
                }
            }).done(function(json) {
                flashMessage("Recipe saved successfully!");
            }).fail(function() {
                flashMessage("Failed to save recipe.");
            });

            $.ajax({
                url: "https://web-02.monadoll.tech/api/v1/recipes",
                type: "GET",
                headers: {
                    "Access-Control-Allow-Origin": "https://web-02.monadoll.tech",
                }
                
            }).done(function(json) {
                console.log(json);
            }
            );

            console.log(recipe);
        
        
            localStorage.clear();
        });
    });
    
    $("#comment-form button").on("click", function() {
        event.preventDefault();
        var that = this;
 
        $.ajax({
            url: "https://web-02.monadoll.tech/status",
            type: "GET",
            Headers: {
                "Access-Control-Allow-Origin": "https://web-02.monadoll.tech",
            }
        }).done(function(json) {
            var user_id = null;
            var user = null;
            if (json.status === "logged") {
                user_id = json.id;
            }

            if (user_id) {
                $.ajax({
                    url: "https://web-02.monadoll.tech/api/v1/users/" + user_id,
                    type: "GET",
                    headers: {
                        "Access-Control-Allow-Origin": "http://0.0.0.0"
                    }
                }).done(function(json) {
                    user = JSON.parse(json);
                    console.log(user)
                });
            }
            if (!user_id) {
                flashMessage("You must be logged in to comment.", ".comment-form button");
                return;
            }

            var message = $(that).parent().find("textarea").val();
            var recipe_id = $(that).parent().find("textarea").attr("data-id");

            if (!message) {
                flashMessage("Please enter a comment.", ".comment-form button");
                return;
            }

            var info = {
                "message": message,
                "recipe_id": recipe_id,
            }
            $.ajax({
                url: "https://web-02.monadoll.tech/api/v1/users/" + user_id + "/comments",
                type: "POST",
                data: JSON.stringify(info),
                contentType: "application/json",
                headers: {
                    "Access-Control-Allow-Origin": "http://0.0.0.0",
                }
            }).done(function(json) {
                console.log("posted");
                flashMessage("Comment added successfully.", ".comment-form button");

                $(".comments-section .comment-list").append(
                    '<div class="comment">' +
                        '<div class="comment-author">' + user.first_name + ' ' + user.last_name + '</div>' +
                        '<div class="comment-text">' + json.text + '</div>' +
                    '</div>'
                );
            });
        });

    });
});