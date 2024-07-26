document.getElementById('uploadForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the default form submission

    const imageInput = document.getElementById('imageInput');
    const loading = document.getElementById('loading');
    const result = document.getElementById('result');
    const tryAgainButton = document.getElementById('tryAgainButton');

    if (imageInput.files.length === 0) {
        alert('Please upload an image.');
        return;
    }

    const formData = new FormData();
    formData.append('file', imageInput.files[0]);

    loading.style.display = 'block';
    result.textContent = '';
    result.classList.remove('ai-generated', 'not-ai-generated');
    tryAgainButton.style.display = 'none';

    fetch('/', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        loading.style.display = 'none';
        if (data.error) {
            result.textContent = data.error;
            result.classList.add('error');
        } else {
            result.textContent = data.prediction;
            result.classList.add(data.prediction === 'Fake' ? 'ai-generated' : 'not-ai-generated');
            document.getElementById('imagePreview').src = `static/${data.image_path}`;
            tryAgainButton.style.display = 'block';
        }
    })
    .catch(error => {
        loading.style.display = 'none';
        result.textContent = 'An error occurred. Please try again.';
        result.classList.add('error');
        tryAgainButton.style.display = 'block';
    });
});

document.getElementById('imageInput').addEventListener('change', function(event) {
    const imagePreview = document.getElementById('imagePreview');
    const file = event.target.files[0];
    const reader = new FileReader();

    reader.onload = function(e) {
        imagePreview.src = e.target.result;
        imagePreview.style.display = 'block';
    }

    if (file) {
        reader.readAsDataURL(file);
    } else {
        imagePreview.style.display = 'none';
    }
});
