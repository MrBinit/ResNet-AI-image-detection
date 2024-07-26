document.getElementById('predictButton').addEventListener('click', function() {
    const imageInput = document.getElementById('imageInput');
    const loading = document.getElementById('loading');
    const result = document.getElementById('result');

    if (imageInput.files.length === 0) {
        alert('Please upload an image.');
        return;
    }

    loading.style.display = 'block';
    result.textContent = '';

    // Simulate a loading and prediction process
    setTimeout(() => {
        loading.style.display = 'none';
        // This is where you would normally handle the prediction logic
        // For demonstration, we'll just randomly decide if the image is AI-generated or not
        const isAIGenerated = Math.random() > 0.5;
        result.textContent = isAIGenerated ? 'The image is AI generated.' : 'The image is not AI generated.';
    }, 2000); // Simulate 2 seconds of loading time
});
