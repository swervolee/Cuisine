#!/usr/bin/node

$(document).ready(function () {
    window.onload = function() {
        setTimeout(function() {
            window.location.href = "http://localhost:5001/login";
        }, 5000); // 5000 milliseconds = 5 seconds
    }
}