#!/usr/bin/node

$(document).ready(function() {
    console.log("Script loaded");

    $(".recipe-creation").on("click", function() {
        console.log("Clicked");
        $(this).toggleClass("show");
    });
});
