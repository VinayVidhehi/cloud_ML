function uploadImage() {
    var formData = new FormData(document.getElementById('uploadForm'));

    // Display loading animation
    document.getElementById('loading').classList.remove('hidden');

    // Make a request to the server to handle image deblurring
    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        // Hide loading animation
        document.getElementById('loading').classList.add('hidden');

        // Display the deblurred image
        document.getElementById('result').classList.remove('hidden');
        document.getElementById('deblurredImage').src = 'data:image/jpeg;base64,' + data.deblurred_image;
    })
    .catch(error => {
        console.error('Error:', error);
        // Handle error if necessary
    });
}
