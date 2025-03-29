from flask import Flask, request, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

HF_API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"
HEADERS = {"Authorization": "Bearer APIKEYHERE"}

SYSTEM_PROMPT = """
You are a kind and supportive mental health companion.
Speak gently, ask reflective questions, and encourage self-care.
"""

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get("message")

    prompt = f"[INST] {SYSTEM_PROMPT}\nUser: {user_message}\nAssistant: [/INST]"

    response = requests.post(
        HF_API_URL,
        headers=HEADERS,
        json={"inputs": prompt}
    )

    if response.status_code == 200:
        reply = response.json()[0]['generated_text'].split("Assistant:")[-1].strip()
        return jsonify({"response": reply})
    else:
        return jsonify({"response": "Sorry, the model is currently unavailable."})

if __name__ == '__main__':
    app.run(debug=True)
