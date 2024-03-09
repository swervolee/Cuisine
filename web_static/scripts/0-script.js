#!/usr/bin/node


/** HANDLE CREATION OF ITEMS */

$(document).ready(function() {

    $(".recipe-creation .data").hide();

    $(".recipe-container").hide();

    $(".introduction h2").on("mouseenter", function() {
	$(this).css("opacity", "0.7")
    }).on("mouseleave", function() {
	$(this).css("opacity", "1");
    });

    $("#recipe-world").on("click", function() {
	console.log("fist child clicked");
	$(".introduction").hide();
	$(".recipe-container").toggle();s
    });


    $(".recipe-creation h3").on("mouseenter", function() {
	$(this).css({"opacity": "0.5"});
    }).on("mouseleave", function() {
	$(this).css({"opacity": "1"});
    });


    $("#recipeForm").on("submit", function(event) {
        event.preventDefault();
        console.log("Submit clicked");
        $(".recipe-creation .data").toggle();
    });




    $(".recipe-creation h3, .introduction .creation").on("click", function() {
	$(".recipe-creation .data").toggle();
	$("header").toggle();
	$(".recipe-container").toggle();
    });


    $(".recipe-ingredients, .recipe-instructions").hide();

    $(".recipe-name h2").on("click", function() {
	$(".recipe-ingredients, .recipe-instructions").toggle();
    }).on("mouseenter", function() {
	$(this).css("opacity", "0.9");
    }).on("mouseleave", function() {
	$(this).css("opacity", "1");
    });


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
