from flask import Flask, render_template, request, jsonify
import cv2
import numpy as np
import pytesseract
import pyttsx3
import base64
import time

# Set the path to the Tesseract executable (change this according to your installation)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

app = Flask(__name__)

def perform_ocr(image_data):
    # Decode the image data from base64 and convert it to NumPy array
    _, encoded_image = image_data.split(',', 1)
    decoded_image = base64.b64decode(encoded_image)
    image = cv2.imdecode(np.frombuffer(decoded_image, np.uint8), cv2.IMREAD_COLOR)

    recognized_text = pytesseract.image_to_string(image, lang='eng')
    return recognized_text

@app.route('/')
def index():
    return render_template('camera_input.html')

@app.route('/perform_ocr', methods=['POST'])
def ocr():
    try:
        image_data = request.json.get('image_data')
        if image_data is None:
            return jsonify({'error': 'No image data provided.'}), 400

        recognized_text = perform_ocr(image_data)
        
        # Introduce a delay of, for example, 2 seconds before responding
        time.sleep(2)
        
        # Speak out the recognized text
        # engine = pyttsx3.init()
        # engine.say(recognized_text)
        # engine.runAndWait()
             
        return jsonify({'output': recognized_text.strip()}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__": #checks whether the script is being run as the main program
    app.run(debug=True) #line starts the Flask development web server
