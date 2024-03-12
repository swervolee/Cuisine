#!/usr/bin/node


/* HANDLE CREATION OF ITEMS */

$(document).ready(function() {

    /*Hide items on default*/
    $(".recipe-creation .data").hide();
    $(".recipe-container").hide();
    $(".recipe-ingredients, .recipe-instructions").hide();
    $(".back").hide();
    $(".comments-section").hide();
    $(".comment-form").hide();

    $(".introduction").slideDown(3000);





    /*change opacity of browse recipes and create recipes on hover*/
    $(".introduction h2").on("mouseenter", function() {
	$(this).css("opacity", "0.7")
    }).on("mouseleave", function() {
	$(this).css("opacity", "1");
    });


    /*style the tags display*/
    $(".tag").on("mouseenter", function() {
	$(".tag ul").css("display", "block");
	$(".tag ul li").on("mouseenter", function() {
	    $(this).css("background-color", "green");
	}).on("mouseleave", function() {
	    $(this).css("background-color", "black");
	});
    }).on("mouseleave", function() {
	$(".tag ul").css("display", "none");
    });


    /*Hide the main menu and show recipes  when show recipes
      platform is clicked*/
    $("#recipe-world").on("click", function() {
	$(".introduction").hide();
	$(".recipe-container").toggle();
	$(".back").toggle();
    });


    /*Change opacity of the tab recipe creation on hover*/
    $(".recipe-creation h3").on("mouseenter", function() {
	$(this).css({"opacity": "0.5"});
    }).on("mouseleave", function() {
	$(this).css({"opacity": "1"});
    });

    /*Prevent empty submission and hide form on submit*/
    $("#recipeForm").on("submit", function(event) {
        event.preventDefault();
        console.log("Submit clicked");
        $(".recipe-creation .data").toggle();
    });


    /*Change the opacity of the back button on hover*/
    $(".back").on("mouseenter", function() {
	$(this).css("opacity", "0.9");
    }).on("mouseleave", function() {
	$(this).css("opacity", "1");
    });


    /*Switch visibilities when back button is pressed*/
    $(".back").on("click", function() {
	$(".introduction").toggle();
	$(".recipe-container").toggle();
	$(".back").hide();
    });


    /*Recipe creation fill form*/
    $(".recipe-creation h3").on("click", function() {
	$(".recipe-creation .data").toggle();
	$("header").toggle();
	$(".recipe-container").toggle();
    });


    /*Only show title and description of recipe on default
      Expand the ingredients and instruction on clicking the
      header*/
    $(".recipe-name h2").on("click", function() {
	$(".recipe-ingredients, .recipe-instructions, .comments-section, .comment-form").toggle();
    }).on("mouseenter", function() {
	$(this).css("opacity", "0.8");
    }).on("mouseleave", function() {
	$(this).css("opacity", "1");
    });




    /*Change color of the favourite button*/
    $(".recipe .favourite").on("click", function() {
	$(this).toggleClass("favourite-red");
	$(this).toggleClass("favourite")
    });


    function flashMessage(message) {
	var messageElement = $("<div>");
	messageElement.text(message);
	messageElement.addClass("to-fade");
	messageElement.css({
	    "color": "black",
	    "display": "inline-block",
	    "background-color": "white",
	    "margin": "10px",
	    "padding": "10px 20px",
	    "border-radius": "5px"});
	messageElement.insertAfter(".comment-form button");

	$(".to-fade").fadeOut(3000);
    };


    $(".comment-form").on("submit", function(event) {
	event.preventDefault();
	flashMessage("Posted");
    });


    $(".recipe-creation h3").trigger("click");


    /*Hide the recipe creation form when area outside of it
      is clicked*/
    $(document).on("click", function(event) {
	console.log(event.target);
        if (!$(event.target).closest(".recipe-creation").length && !$(event.target).is(":submit")) {
            if ($(".recipe-creation .data").is(":visible")) {
                $(".recipe-creation .data").hide();
		$("header").toggle();
		$(".recipe-container").toggle();
            }
        }
    });
});
