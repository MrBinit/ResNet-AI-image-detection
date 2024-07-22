# import os
# from flask import Flask, request, jsonify, render_template
# import tensorflow as tf
# from tensorflow.keras.preprocessing import image
# from tensorflow.keras.applications.resnet50 import preprocess_input

# app = Flask(__name__)

# # Path to the SavedModel directory
# model_path = '/Users/mrbinit/Desktop/saved_model_RESNET'

# # Load the SavedModel using keras.layers.TFSMLayer
# model = tf.keras.Sequential([
#     tf.keras.layers.TFSMLayer(model_path, call_endpoint='serving_default')
# ])

# # Function to preprocess the uploaded image
# def preprocess_image(file_path, image_size=(224, 224)):
#     img = tf.io.read_file(file_path)
#     img = tf.image.decode_jpeg(img, channels=3)  # Ensure 3 channels (RGB)
#     img = tf.image.resize(img, image_size)
#     img = preprocess_input(img)
#     img = tf.expand_dims(img, axis=0)  # Add batch dimension
#     return img

# # Route to handle index page and image prediction
# @app.route('/', methods=['GET', 'POST'])
# def index():
#     if request.method == 'GET':
#         return render_template('index.html', prediction=None)

#     if request.method == 'POST':
#         if 'image' not in request.files:
#             return jsonify({'error': 'No image uploaded'})

#         # Save the uploaded image to a temporary file
#         img = request.files['image']
#         img_path = 'temp.jpg'
#         img.save(img_path)

#         # Preprocess the uploaded image
#         processed_img = preprocess_image(img_path)

#         # Make prediction using the loaded model
#         prediction = model(processed_img)  # Assuming the model outputs probabilities for each class
#         probability_real = prediction[0][0].numpy()
#         probability_fake = prediction[0][1].numpy()

#         # Remove the temporary uploaded image
#         os.remove(img_path)

#         # Return prediction result to the template
#         return render_template('index.html', prediction={
#             'probability_real': float(probability_real),
#             'probability_fake': float(probability_fake)
#         })

# if __name__ == '__main__':
#     app.run(debug=True)


import os
from flask import Flask, request, jsonify, render_template
import tensorflow as tf
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import numpy as np

app = Flask(__name__)

# Path to the SavedModel directory
model_path = '/Users/mrbinit/Desktop/saved_model_RESNET'

# Load the SavedModel using keras.layers.TFSMLayer
model = tf.keras.Sequential([
    tf.keras.layers.TFSMLayer(model_path, call_endpoint='serving_default')
])



# Function to preprocess the uploaded image
def preprocess_image(file_path, target_size=(224, 224)):
    img = load_img(file_path, target_size=target_size)
    img = img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img = tf.keras.applications.resnet50.preprocess_input(img)
    return img

# Route to handle index page and image prediction
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html', prediction=None)

    if request.method == 'POST':
        if 'image' not in request.files:
            return jsonify({'error': 'No image uploaded'})

        # Save the uploaded image to a temporary file
        img = request.files['image']
        img_path = 'temp.jpg'
        img.save(img_path)

        # Preprocess the uploaded image
        processed_img = preprocess_image(img_path)

        # Make prediction using the loaded model
        prediction = model.predict(processed_img)

        # Assuming the model outputs a probability for AI-generated
        is_ai_generated = prediction[0][0] > 0.5

        # Remove the temporary uploaded image
        os.remove(img_path)

        # Return prediction result to the template
        return render_template('index.html', prediction={
            'is_ai_generated': is_ai_generated
        })

if __name__ == '__main__':
    app.run(debug=True)


