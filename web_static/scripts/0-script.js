
/** HANDLE CREATION OF ITEMS */

$(document).ready(function() {
    console.log("Script loaded");

    $(".recipe-creation .data").hide();


    $("#recipeForm").on("submit", function(event) {
        event.preventDefault();
        console.log("Submit clicked");
        $(".recipe-creation .data").toggle();
    });

    $(".recipe-creation h3").on("click", function() {
	$(".recipe-creation .data").toggle();
    });

    $(document).on("click", function(event) {
	console.log(event.target);
        if (!$(event.target).closest(".recipe-creation").length && !$(event.target).is(":submit")) {
            if ($(".recipe-creation .data").is(":visible")) {
                $(".recipe-creation .data").hide();
            }
        }
    });
});
