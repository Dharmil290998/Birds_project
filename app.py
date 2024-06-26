from flask import Flask, request, render_template
import tensorflow as tf
from PIL import Image
import numpy as np
import io
import os
import tempfile

# Load your trained model (ensure the path is correct)
model = tf.keras.models.load_model('C:/eco_eye_demo/venv/model.h5')

# Specify your custom template folder path
app = Flask(__name__, template_folder='C:/eco_eye_demo/venv/template')  # Ensure this path is correct

@app.route('/')
def home():
    # Flask will look for 'index.html' in the specified templates folder
    return render_template('index.html')

def preprocess_image(image_path):
    img = tf.keras.preprocessing.image.load_img(image_path, target_size=(224, 224))
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)  # Create a batch
    img_array = tf.keras.applications.efficientnet.preprocess_input(img_array)
    return img_array

# def preprocess_image(file_storage):
#     # Convert the FileStorage to a BytesIO and open it with PIL
#     img = Image.open(io.BytesIO(file_storage.read())).convert('RGB')
#     img = img.resize((224, 224))  # Resize the image to match your model's expected input
#     img_array = np.array(img) / 255.0  # Convert to array and normalize
#     img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
#     img_array = tf.keras.applications.efficientnet.preprocess_input(img_array)
#     return img_array

def predict_image(model, processed_image):
    predictions = model.predict(processed_image)
    predicted_class = np.argmax(predictions, axis=1)
    return predicted_class

labels_dict = {0: 'AFRICAN EMERALD CUCKOO',
 1: 'AFRICAN PIED HORNBILL',
 2: 'ALBATROSS',
 3: 'AMERICAN BITTERN',
 4: 'GOLDEN CHEEKED WARBLER',
 5: 'GRAY KINGBIRD',
 6: 'LONG-EARED OWL',
 7: 'MYNA',
 8: 'RAZORBILL',
 9: 'RED TAILED HAWK'}

def get_class_label(class_index):
    # Assuming you have a dictionary that maps class indices to labels
    # labels = {0: 'Class1', 1: 'Class2', ...}  # Fill in your actual labels
    return labels_dict[class_index]

# @app.route('/predict', methods=['POST'])
# def predict():
#     if 'image' not in request.files:
#         return 'No file part', 400
#     file = request.files['image']
#     if file.filename == '':
#         return 'No selected file', 400
#     if file:
#         # # Convert the file to an RGB image
#         # image = Image.open(file).convert('RGB')
        
#         # # Resize the image to the expected input size of your model
#         # image = image.resize((224, 224))  # Adjust the size (224, 224) as per your model's requirement
        
#         # # Convert the image to a numpy array and normalize it if required by your model
#         # image_array = np.expand_dims(np.array(image) / 255.0, axis=0)
        
#         # # Predict the class of the image
#         # prediction = model.predict(image_array)
#         # # predicted_class = np.argmax(prediction, axis=1)  # Assuming your model predicts classes as integers
        
#         # # Convert predicted_class to string or map to actual class names if you have a class mapping
#         # # For example: predicted_class_name = class_names[predicted_class[0]] if you have a class_names list or dict
#         # # predicted_class_name = str(predicted_class[0])  # Simple conversion to string; adapt as needed
        
#         # # Render the template with the prediction result

#         # processed_image = preprocess_image(file)
#         predicted_class_index = predict_image(model, file)
#         class_label = get_class_label(predicted_class_index.item())

#         return render_template('index.html', prediction=class_label)
#                             #    =predicted_class_name)

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return 'No file part', 400
    file = request.files['image']
    if file.filename == '':
        return 'No selected file', 400
    if file:
        # Preprocess the uploaded image
        # processed_image = preprocess_image(file)

        # Save the file to a temporary file
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            file.save(tmp_file.name)
            # Now you can use the saved file's path to preprocess the image
            processed_image = preprocess_image(tmp_file.name)
        
        # Remember to delete the temporary file after processing
        os.unlink(tmp_file.name)
        
        # Predict the class of the processed image
        predicted_class_index = predict_image(model, processed_image)
        
        # Convert the class index to a readable class label
        class_label = get_class_label(predicted_class_index.item())
        
        # Render the template with the prediction result
        return render_template('index.html', prediction=class_label)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
