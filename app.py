from flask import Flask, request, render_template, jsonify
from PIL import Image
from transformers import AutoImageProcessor, AutoModelForImageClassification
import torch
import os

app = Flask(__name__)

# Load model and processor
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
processor = AutoImageProcessor.from_pretrained("Organika/sdxl-detector")
model = AutoModelForImageClassification.from_pretrained("Organika/sdxl-detector")
model.to(device)

def predict(image_path):
    image = Image.open(image_path).convert("RGB")
    inputs = processor(image, return_tensors="pt").pixel_values.to(device)
    outputs = model(inputs).logits
    _, predicted_class = torch.max(outputs, dim=1)
    return "Fake" if predicted_class.item() == 0 else "Real"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        if file:
            filename = file.filename
            file_path = os.path.join('static/uploads', filename)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            file.save(file_path)
            prediction = predict(file_path)
            return jsonify({'prediction': prediction, 'image_path': 'uploads/' + filename})
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
