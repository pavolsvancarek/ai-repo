from flask import Flask, request, jsonify
from openai import OpenAI
import os
from dotenv import load_dotenv
from whisper_api import transcribe

load_dotenv()
app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/ask", methods=["POST"])
def ask():
    try:
        text = request.json.get("text", "")
        print("Používateľ napísal:", text)

        chat = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Always reply strictly in English. Do not switch to other languages, no matter what the user writes. The user may use any language. Be concise but clear. Explain well if asked. Don't be polite, be honest. Don't agree if you disagree."},
                {"role": "user", "content": text}
            ],
            temperature=0.3
        )


        reply = chat.choices[0].message.content.strip()
        print("GPT odpovedá:", reply)
        return jsonify({"reply": reply})

    except Exception as e:
        print("CHYBA pri GPT:", str(e))
        return jsonify({"reply": "Chyba na serveri"}), 500


@app.route("/whisper", methods=["POST"])
def whisper():
    try:
        print("PRIJATÉ FILES:", request.files)
        print("HEADERS:", request.headers)
        print("FORM:", request.form)

        if "audio" not in request.files:
            return jsonify({"error": "Žiadny audio súbor"}), 400

        file = request.files["audio"]
        filepath = "temp.wav"
        file.save(filepath)

        print("Dostal som .wav súbor:", filepath)
        text = transcribe(filepath)
        print("Whisper prepis:", text)
        print("Veľkosť súboru:", os.path.getsize(filepath), "bytov")

        return jsonify({"text": text})
    except Exception as e:
        print("CHYBA pri prepise:", str(e))
        return jsonify({"text": ""}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
