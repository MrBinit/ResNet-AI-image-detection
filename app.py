from flask import Flask, request, jsonify
import tensorflow as tf
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.applications.resnet50 import preprocess_input

app = Flask(__name__)

# Load the trained model
model = tf.keras.models.load_model('/Users/mrbinit/Library/Mobile Documents/com~apple~CloudDocs/Downloads')

def preprocess_image(image_path, target_size=(224, 224)):
    image = load_img(image_path, target_size=target_size)
    image = img_to_array(image)
    image = preprocess_input(image)
    image = np.expand_dims(image, axis=0)
    return image

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return "Please upload an image file", 400
    file = request.files['file']
    if file.filename == '':
        return "No file selected", 400
    file_path = './' + file.filename
    file.save(file_path)

    image = preprocess_image(file_path)
    prediction = model.predict(image)

    # Assuming binary classification (AI-generated vs. real)
    is_ai_generated = prediction[0][0] > 0.5

    return jsonify({
        'is_ai_generated': bool(is_ai_generated),
        'confidence': float(prediction[0][0])
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
