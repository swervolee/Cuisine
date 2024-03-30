#!/usr/bin/node

$(document).ready(function() {
    $(".introduction h2").on("mouseenter", function (){
	$(this).css("background-color", "white");
    }).on("mouseleave", function () {
	$(this).css("background-color", "black");
    });
});
