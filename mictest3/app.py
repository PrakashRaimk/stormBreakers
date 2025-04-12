from flask import Flask, render_template, request, send_from_directory
import speech_recognition as sr
from io import BytesIO
import os

app = Flask(__name__)
RESPONSE_DIR = "responses"

@app.route('/')
def index():
    return render_template('mic.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'audio' not in request.files:
        return 'No audio file received', 400

    audio_file = request.files['audio']
    audio_data = BytesIO(audio_file.read())

    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(audio_data) as source:
            audio = recognizer.record(source)
            text = recognizer.recognize_google(audio)
            return {
                "text": text,
                "audio_url": "/response-audio/response.wav"
            }
    except Exception as e:
        return {"error": str(e)}

@app.route('/response-audio/<filename>')
def response_audio(filename):
    return send_from_directory(RESPONSE_DIR, filename)

if __name__ == '__main__':
    app.run(debug=True)
