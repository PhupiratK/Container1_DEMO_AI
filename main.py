from flask import Flask, request, jsonify
import base64
from PIL import Image
import io
import tensorflow as tf

app = Flask(__name__)

# Initialize the model outside the route
model = None

def load_model():
    try:
        # Load the image classification model
        global model
        model = tf.keras.models.load_model('model_fruit.h5')
        return True
    except Exception as e:
        print(f"Failed to load the model: {str(e)}")
        return False

# Load the model when the application starts
if load_model():
    print("Model loaded successfully.")
else:
    print("Model failed to load.")

# Function for classifying images from base64
def classify_image_from_base64(base64_image):
    try:
        # Ensure the model is loaded
        if model is None:
            return "Model not loaded."

        # Convert base64 to an image
        image = Image.open(io.BytesIO(base64.b64decode(base64_image)))
        
        # Resize the image to match the model's input size (check the model's requirements)
        image = image.resize((1000, 1000))
        
        # Convert the image to a numpy array
        image = tf.keras.preprocessing.image.img_to_array(image)
        
        # Normalize the image
        image = tf.keras.applications.mobilenet_v2.preprocess_input(image)
        
        # Use the model to predict (classify) the image
        predictions = model.predict(image[tf.newaxis, ...])
        
        # Get the class name with the highest probability
        class_index = tf.argmax(predictions, axis=-1)
        class_label = tf.keras.applications.imagenet_utils.decode_predictions(predictions)
        
        return class_label[0][0][1]  # Return the class name
    except Exception as e:
        return str(e)

@app.route('/classify', methods=['POST'])
def classify_image():
    try:
        # Receive base64 image data from the request
        data = request.get_json()
        base64_image = data.get('image')

        if not base64_image:
            return jsonify({'error': 'Missing or invalid image data'}), 400

        # Call the image classification function
        result = classify_image_from_base64(base64_image)
        return jsonify({'result': result})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
