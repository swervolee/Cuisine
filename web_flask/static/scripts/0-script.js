#!/usr/bin/node


$(window).on('load', () => {
    $('.loader').fadeOut(2000);
    
})

$(document).ready(function() {


    
        
    /*Hide items on default*/
    $(".recipe-creation .data").hide();
    /*$(".recipe-container").hide();*/
    $(".recipe-ingredients, .recipe-instructions").hide();
    $(".back").hide();
    $(".comments-section").hide();
    $(".comment-form").hide();

    $(".introduction").slideDown(3000);

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

    $(".recipe-name h2").on("click", function(event) {
	event.stopPropagation(); // Stop event propagation to prevent hiding when clicked on this element
	var $recipe = $(this).closest(".recipe");
	var $otherRecipes = $(".recipe").not($recipe); // Select all other recipes
	var $toggleItems = $recipe.find(".recipe-ingredients, .recipe-instructions, .comments-section, .comment-form");

	/* Get the current scroll position */
	var scrollTop = $(window).scrollTop();

	/* Toggle the current recipe items*/
	$toggleItems.toggle();


	/* Hide items of other recipes*/
	$otherRecipes.find(".recipe-ingredients, .recipe-instructions, .comments-section, .comment-form").hide();

	/* Adjust the scroll position of the window to the currently clicked item*/
	$(window).scrollTop($recipe.offset().top);

	/* Click event to hide items when clicking outside of the recipe*/
	$(document).one("click", function(event) {
            if (!$(event.target).closest(".recipe").length) {
		$toggleItems.hide();
            }
	});
	/* Prevent the event from bubbling up to the document */
	return false;
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
