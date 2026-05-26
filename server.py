from flask import Flask, request, jsonify
from flask_cors import CORS
from faster_whisper import WhisperModel
from deep_translator import GoogleTranslator
import uuid
import os

app = Flask(__name__)
CORS(app)

print("Loading Whisper model...")
model = WhisperModel("base", device="cpu", compute_type="int8")

@app.route("/")
def home():
    return "Speech-to-Text Server Running OK"

@app.route("/transcribe", methods=["POST"])
def transcribe():

    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]

    path = f"temp_{uuid.uuid4()}.mp3"
    file.save(path)

    try:
        # 🎙️ Speech to text
        segments, _ = model.transcribe(path)

        text = " ".join([s.text for s in segments])

        # 🌍 Translate English -> Indonesian
        translated = GoogleTranslator(
            source='auto',
            target='id'
        ).translate(text)

        return jsonify({
            "text": text,
            "translated": translated
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if os.path.exists(path):
            os.remove(path)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)