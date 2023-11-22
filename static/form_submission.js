$(document).ready(function(){
    $("#upload-form").on('submit', function(e){
        e.preventDefault();
        console.log('Form submission detected.');
        alert('Data has been submitted for analysis. \n\nPlease allow up to a minute per article, you will be notified when your analysis is complete.');
        $.ajax({
            url: '/form', // handled dynamically in equivalent PPT AJAX call
            method: 'POST', // handled dynamically in equivalent PPT AJAX call. changed from type. both valid, method recommended
            data: new FormData(this),
            contentType: false,
            cache: false,
            processData:false,
            success: function(response){
                console.log('Success function activated.');
                console.log(response);
                window.location.href = "/download?filename=" + response.filename;  // use filename from JSON response
                alert(`Analysis complete! Remember to run a full SC check on the data!\n\nPlease check browser downloads for your completed analysis.\n\n${response.articles_analysed} articles analysed in ${response.elapsed_time} seconds.\n\nTotal cost: ${response.total_cents} cents\nCost breakdown: ${response.prompt_cents}c prompt, ${response.completion_cents}c completion.`);
            },
            error: function(jqXHR, textStatus, errorThrown) {
                console.log("AJAX error: " + textStatus + ' : ' + errorThrown);
                alert('An error occurred while processing your request. Please try again.');
            }
        });
    });
});
