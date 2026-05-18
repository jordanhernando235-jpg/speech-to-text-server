from flask import Flask, request, jsonify
from flask_cors import CORS
from faster_whisper import WhisperModel
from deep_translator import GoogleTranslator

import os
import uuid
import traceback
import subprocess

app = Flask(__name__)

CORS(app)

# ALLOW LARGE FILES
app.config["MAX_CONTENT_LENGTH"] = 500 * 1024 * 1024  # 500MB

UPLOAD_FOLDER = "uploads"

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)

print("Loading Whisper model...")

# WHISPER MODEL
model = WhisperModel(
    "base",
    device="cpu",
    compute_type="int8"
)

@app.route("/")
def home():

    return "Server is running"

@app.route("/transcribe", methods=["POST"])
def transcribe():

    temp_input = None
    temp_wav = None

    try:

        # CHECK FILE
        if "file" not in request.files:

            return jsonify({
                "success": False,
                "error": "No file uploaded"
            }), 400

        file = request.files["file"]

        if file.filename == "":

            return jsonify({
                "success": False,
                "error": "Empty filename"
            }), 400

        print("Uploaded file:", file.filename)

        # UNIQUE ID
        uid = str(uuid.uuid4())

        # GET FILE EXTENSION
        extension = os.path.splitext(
            file.filename
        )[1].lower()

        # ALLOWED AUDIO TYPES
        allowed = [
            ".mp3",
            ".wav",
            ".m4a",
            ".ogg"
        ]

        if extension not in allowed:

            return jsonify({
                "success": False,
                "error": "Unsupported audio format"
            }), 400

        # INPUT FILE
        temp_input = os.path.join(
            UPLOAD_FOLDER,
            f"{uid}{extension}"
        )

        # OUTPUT WAV
        temp_wav = os.path.join(
            UPLOAD_FOLDER,
            f"{uid}.wav"
        )

        # SAVE FILE
        file.save(temp_input)

        print("Saved file")

        # CONVERT TO WAV
        print("Converting audio...")

        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-i",
                temp_input,
                "-ar",
                "16000",
                "-ac",
                "1",
                temp_wav
            ],
            check=True
        )

        print("Conversion complete")

        # TRANSCRIBE
        print("Starting transcription...")

        segments, info = model.transcribe(
            temp_wav,
            beam_size=1
        )

        text_parts = []

        for segment in segments:

            text_parts.append(
                segment.text
            )

        text = " ".join(
            text_parts
        ).strip()

        print("Detected language:", info.language)

        print("Text:", text)

        # TRANSLATE TO INDONESIAN
        translated = GoogleTranslator(
            source="auto",
            target="id"
        ).translate(text)

        return jsonify({
            "success": True,
            "language": info.language,
            "text": text,
            "translated": translated
        })

    except Exception as e:

        print(traceback.format_exc())

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

    finally:

        # CLEANUP FILES
        try:

            if temp_input and os.path.exists(temp_input):

                os.remove(temp_input)

            if temp_wav and os.path.exists(temp_wav):

                os.remove(temp_wav)

        except Exception as cleanup_error:

            print(
                "Cleanup error:",
                cleanup_error
            )

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )