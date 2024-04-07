
$(function() {
    $("#txtarea").on("input", function () {
        if (this.scrollHeight > this.clientHeight) {
            $(this).css({
                "height": this.scrollHeight + "px",
            });
        } else {
            $(this).css({
                "height": "auto",
            });
        }
    });
});
