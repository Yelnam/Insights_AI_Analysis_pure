$(document).ready(function () {
    $("#upload-form-ppt").on("submit", function(e){
        e.preventDefault();
        console.log('Form submission detected.');
        alert('Data has been submitted and PowerPoint report is being generated. While it may be much quicker, please allow up to a minute per slide. You will be notified when your analysis is complete.');
        $.ajax({
            url: $(this).attr("action"),
            method: $(this).attr("method"),
            data: new FormData(this),
            contentType: false,
            cache: false,
            processData: false,
            success: function (response) {
                console.log('Success function activated.');
                console.log(response);
                window.location.href = "/download_ppt/" + response.filename;
                alert('PPT report is complete and will be delivered to your browser downloads. Please run a full QC on report before delivery to client.');
            },
            error: function(jqXHR, textStatus, errorThrown) {
                console.log("AJAX error: " + textStatus + ' : ' + errorThrown);
                alert('An error occurred while processing your request. Please try again.');
            }
        });
    });
});
