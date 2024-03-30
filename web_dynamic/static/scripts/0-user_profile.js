#!/usr/bin/node

$(".logout-text").on("click", function() {
    $ajax({
        url: "0.0.0.0:5001/logout",
        data: {
            "status": "logout"
        },
        type: "POST",
        datatype: "json"
    })
})