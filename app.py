from flask import Flask, request, jsonify
from flask_cors import CORS
from helper import classify_plant
import os
from PIL import Image
import numpy as np  # numpy kütüphanesini ekledik

app = Flask(__name__)
CORS(app)

@app.route('/predict', methods=['POST'])
def predict():
    file = request.files['image']
    class_name, confidence = classify_plant(file)
    
    if class_name and confidence:
        # Orijinal resmi kaydet ve URL'ini oluştur
        img = Image.open(file)
        save_path = os.path.join('static', 'original_image.png')
        img.save(save_path)
        image_url = f'http://192.168.1.163:5000/static/original_image.png'
        
        # TensorFlow'dan gelen EagerTensor'u numpy dizisine dönüştür
        confidence = float(confidence)  # TensorFlow'dan gelen tensorı float olarak dönüştür
        
        return jsonify({'prediction': class_name, 'confidence': confidence, 'image_url': image_url})
    else:
        return jsonify({'error': 'Sınıflandırma hatası'}), 500

if __name__ == '__main__':
    if not os.path.exists('static'):
        os.makedirs('static')
    app.run(host='0.0.0.0', port=5000)
