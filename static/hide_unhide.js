// Get the form sections
const excelInputSection = document.getElementById('excel-input-section');
const rssInputSection = document.getElementById('rss-input-section');

// Set up event listeners for the data source buttons
document.getElementById('Excel').addEventListener('click', function () {
    excelInputSection.style.display = 'block';
    rssInputSection.style.display = 'none';
});

document.getElementById('RSS').addEventListener('click', function () {
    excelInputSection.style.display = 'none';
    rssInputSection.style.display = 'block';
});