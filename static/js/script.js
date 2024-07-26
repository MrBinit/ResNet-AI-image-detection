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
    result.classList.remove('ai-generated', 'not-ai-generated');
});
