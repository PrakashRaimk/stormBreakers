from flask import Flask, render_template, request
import speech_recognition as sr
from io import BytesIO

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('mic.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'audio' not in request.files:
        return 'No audio file', 400

    audio_file = request.files['audio']
    audio_data = BytesIO(audio_file.read())

    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(audio_data) as source:
            audio = recognizer.record(source)
            text = recognizer.recognize_google(audio)
            return f"Transcription: {text}"
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
