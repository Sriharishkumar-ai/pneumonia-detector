from flask import Flask, request, render_template
import tensorflow as tf
import numpy as np
import cv2

app = Flask(__name__)

# Load trained model
model = tf.keras.models.load_model("medical_ai_model.h5")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return render_template('index.html', prediction="No image uploaded.")

    file = request.files['image']
    image = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_GRAYSCALE)
    image = cv2.resize(image, (256, 256)) / 255.0
    image = image.reshape(1, 256, 256, 1)

    pred = model.predict(image)[0][0]
    result = "Pneumonia Detected" if pred > 0.5 else "Normal"
    confidence = f"{(pred if pred > 0.5 else 1 - pred) * 100:.2f}%"

    return render_template('index.html', prediction=result, confidence=confidence)

if __name__ == '__main__':
    app.run(debug=True)
