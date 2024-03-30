var user = {};

$.ajax({
    url: "http://0.0.0.0:5001/status",
    type: "GET",
    dataType: "json" // corrected datatype to dataType
}).done(function (json) {
    if (json.status === "logged") {
        console.log("User is logged in and id is " + json.id);
        
        $.ajax({
            url: "http://0.0.0.0:5000/api/v1/users/" + json.id, // corrected URL
            dataType: "json",
            type: "GET"
        }).done(function (userJson) {
            user = userJson;
            console.log("User details:", user);
        }).fail(function (xhr, status, error) {
            console.error("Failed to retrieve user details:", error);
        });
    } else {
        console.log("User is not logged in");
    }
}).fail(function (xhr, status, error) {
    console.error("Failed to check user status:", error);
});