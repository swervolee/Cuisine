
$(function() {
    $("#txtarea, .instruction textarea").on("input", function() {
        if (this.scrollHeight > this.clientHeight) {
            $(this).css({
                "height": this.scrollHeight + "px",
            });
        } else {
            $(this).css({
                "height": $(this).scrollHeight + "px",
            });
        }

        // Load any saved value from localStorage
        var savedValue = localStorage.getItem('textareaValue');
        if (savedValue) {
            $("#txtarea, .instruction textarea").val(savedValue);
        }
    });

    // Save the value to localStorage whenever it changes
    $("#txtarea, .instruction textarea").on("input", function() {
        localStorage.setItem('textareaValue', $(this).val());

        if (this.scrollHeight > this.clientHeight) {
            $(this).css({
                "height": this.scrollHeight + "px",
            });
        } else {
            $(this).css({
                "height": $(this).scrollHeight + "px",
            });
        }
    });
});
