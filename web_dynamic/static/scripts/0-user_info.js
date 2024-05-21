
// Remove unnecessary variable declaration
// var user = {};
$(document).ready(function() {
    $.ajax({
        url: "0.0.0.0:5001/status",
        type: "GET",
        Headers: {
            "Access-Control-Allow-Origin": "52.91.120.169"
        }
    }).done(function(json) {
        if (json.status === "logged") {
            console.log("User is logged in and id is " + json.id);

            $.ajax({
                url: "https://web-02.monadoll.tech/api/v1/users/" + json.id,
                dataType: "json",
                type: "GET",
                Headers: {
                    "Access-Control-Allow-Origin": "52.91.120.169"
                }
            }).done(function(userJson) {
                var user = userJson; // Declare user variable here
                console.log("User details:", user);
            }).fail(function(xhr, status, error) {
                console.error("Failed to retrieve user details:", error);
            });
        } else {
            console.log("User is not logged in");
        }
    }).fail(function(xhr, status, error) {
        console.error("Failed to check user status:", error);
    });

    $.ajax({
        url: "https://web-02.monadoll.tech/status",
        type: "GET",
    }).done(function(json) {
        if (json.status === "logged") {
            console.log("User is logged in and id is " + json.id);

            $.ajax({
                url: "https://web-02.monadoll.tech/api/v1/users/" + json.id,
                dataType: "json",
                type: "GET"
            }).done(function(userJson) {
                user = userJson;
                console.log("User details:", user);
            }).fail(function(xhr, status, error) {
                console.error("Failed to retrieve user details:", error);
            });
        } else {
            console.log("User is not logged in");
        }
    }).fail(function(xhr, status, error) {
        console.error("Failed to check user status:", error);
    });
});