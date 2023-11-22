$(document).ready(function() {
    $('[data-toggle="tooltip"]').tooltip();

    $(".binary-choice-button").click(function() {
        // Get the parent container and the associated input ID
        var container = $(this).parent(".binary-choice");
        var inputId = container.data("input-id");
        var inputValue = "";

        // If this button is already selected, deselect it
        if ($(this).hasClass("selected")) {
            $(this).removeClass("selected");
        } else {
            // If another button was selected, deselect it
            container.find(".binary-choice-button").removeClass("selected");
            // Select this button
            $(this).addClass("selected");
            inputValue = $(this).attr("id");
        }

        // Store the selected value in the hidden input field
        $("#" + inputId).val(inputValue);
    });

    $(".binary-choice-button").hover(
        function() {
            $(this).addClass("hover");
        },
        function() {
            $(this).removeClass("hover");
        }
    );
});