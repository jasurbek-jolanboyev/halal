from flask import Flask, request, jsonify, send_from_directory
import openai
import os
from flask_cors import CORS

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

# Renderda kalitni Environment Variables orqali oladi
openai.api_key = os.getenv("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")

SYSTEM_PROMPT = """Sen Credit.AI halol moliyalashtirish bo‘yicha sun'iy intellekt maslahatchisisan. 
Javob faqat o‘zbek tilida, do‘stona va professional tonda bo‘lsin. 
Har javob oxirida “In sha Alloh, rizqingiz barakali bo‘lsin!” deb yoz."""

@app.route("/")
def index():
    return send_from_directory('.', 'index.html')

@app.route("/<path:path>")
def static_files(path):
    return send_from_directory('.', path)

@app.route("/api/chat", methods=["POST"])
def chat():
    try:
        user_message = request.json.get("message", "").strip()
        if not user_message:
            return jsonify({"error": "Xabar bo‘sh"}), 400

        completion = openai.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0.7,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ]
        )
        answer = completion.choices[0].message.content.strip()
        return jsonify({"answer": answer})

    except Exception as e:
        return jsonify({"error": "Server xatosi"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))