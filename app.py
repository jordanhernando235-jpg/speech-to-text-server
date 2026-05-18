from flask import Flask, request, jsonify
from googletrans import Translator

app = Flask(__name__)

translator = Translator()

@app.route("/translate", methods=["POST"])
def translate_text():

    data = request.json

    text = data.get("text")
    target = data.get("target")

    translated = translator.translate(
        text,
        dest=target
    )

    return jsonify({
        "translated_text": translated.text
    })

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000
    )