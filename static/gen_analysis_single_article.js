async function sendMessage() {

    const modelSingle = document.getElementById('model_single').value;

    // Display a loading message to assure front end user that data is being collected
    const responseElement = document.getElementById('response');
    responseElement.innerText = `Processing with model ${modelSingle}... 
    this usually takes up to 30 seconds with GPT3,
    and up to a minute with GPT4.`;


    const articleHeadline = document.getElementById('article_headline').value;
    const articleText = document.getElementById('article_text').value;
    const brandList = document.getElementById('brand_list').value;

    const response = await fetch('http://localhost:5000/single', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ modelSingle, articleHeadline, articleText, brandList }),
    });
    const responseData = await response.json();
    console.log(responseData);
    console.log(typeof responseData);

    // Clear the loading message
    responseElement.innerText = '';

    // Loop over all brands
    for (const brand in responseData) {
        // Create a table
        const table = document.createElement('table');
        table.className = 'brandTable'; 
        const caption = document.createElement('caption');
        caption.textContent = brand;
        table.appendChild(caption);
        
        // The order of keys
        const orderedKeys = ['Mention_YN', 'Corporate_Consumer', 'Sentiment', 'Sentiment_explanation', 'Prominence', 'Topics', 'Positive_Brand_Values', 'Negative_Brand_Values', 'Spokespeople', 'Story'];
        
        // Loop over orderedKeys instead of directly looping over the attributes of responseData[brand]
        for (const key of orderedKeys) {
            // Check if the key exists in responseData[brand]
            if (key in responseData[brand]) {
                const tr = document.createElement('tr');
                const th = document.createElement('th');
                const td = document.createElement('td');

                th.textContent = key;

                // Check if the value is an array
                if (Array.isArray(responseData[brand][key])) {
                    td.textContent = responseData[brand][key].join(', ');
                } else if (key === 'Sentiment') {
                    // Add tooltip for sentiment explanation
                    td.textContent = responseData[brand][key];
                    if (responseData[brand]['Sentiment_explanation']) {
                        td.title = responseData[brand]['Sentiment_explanation'];
                    }
                } else {
                    td.textContent = responseData[brand][key];
                }

                tr.appendChild(th);
                tr.appendChild(td);
                table.appendChild(tr);
            }
        }

        document.getElementById('response').appendChild(table);
    }
}