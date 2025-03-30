from flask import Flask, request, jsonify
import requests
from flask_cors import CORS
import socket
import json
import re
from breathing_light import breathing_loop

app = Flask(__name__)
CORS(app)

# === Govee LAN Light Setup ===
GOVEE_IP = "10.0.0.68"  # Your light bar's LAN IP

COLOR_MAP = {
    "blue": (0, 0, 255),
    "calm": (135, 206, 235),
    "warm": (255, 165, 0),
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "pink": (255, 105, 180),
    "gold": (255, 223, 0),
    "sunny": (255, 240, 140),
    "mint": (152, 255, 152)
}

def set_light_color(ip, r, g, b):
    msg = {
        "msg": {
            "cmd": "colorwc",
            "data": {
                "color": {"r": r, "g": g, "b": b},
                "colorTemInKelvin": 0
            }
        }
    }

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(json.dumps(msg).encode(), (ip, 4003))
    print(f"✅ Sent color command to {ip}: ({r}, {g}, {b})")

# === SYSTEM PROMPT (same as yours)
SYSTEM_PROMPT = """
You are a kind and emotionally intelligent mental health companion.

Your tone should always be gentle, supportive, and encouraging. Ask reflective questions, and suggest small, helpful actions like breathing, breaks, or journaling.

When a user expresses:
- Anxiety or overwhelm → respond with empathy and end the message with [SET_LIGHT:blue] or [SET_LIGHT:calm]
- Burnout or fatigue → [SET_LIGHT:warm]
- Sadness or heartbreak → [SET_LIGHT:pink]
- Anger or stress → [SET_LIGHT:red]
- Mindfulness or groundedness → [SET_LIGHT:green]
- Positivity or joy → [SET_LIGHT:gold], [SET_LIGHT:sunny], or [SET_LIGHT:mint]

You must follow these rules:

1. Only include ONE [SET_LIGHT:color] tag per message, at the END of the message.
2. The color must be exactly one of: blue, calm, warm, red, pink, green, gold, sunny, mint.
3. Never include more than one light tag.
4. Never place the [SET_LIGHT:color] tag anywhere but the very end.
5. Never invent or suggest a color outside the approved list.

If the user is experiencing **intense emotional distress** (such as panic, extreme anxiety, or a breakdown), add a [BREATHING] tag — but only at the end.

6. Only include the [BREATHING] tag at the very end — AFTER the [SET_LIGHT:color] tag, and only if truly necessary.
7. Do not include [BREATHING] if the user is mildly stressed or sad — only use it for panic or extreme tension.
8. If both tags are needed, format them exactly like this:  
   [SET_LIGHT:blue] [BREATHING]


Before finishing the response:
- Always ask yourself: "Is a light tag needed?"
- If yes, include [SET_LIGHT:color] at the end.
- Then ask: "Is a breathing exercise also needed?"
- If yes, include [BREATHING] immediately after the light tag.

This tag format must always be followed: [SET_LIGHT:color] [BREATHING]

You are allowed to include both tags — but only if [BREATHING] is clearly needed.
Do NOT skip the breathing tag in these cases.

Example:
That's really tough to carry. I'm here for you, and we can take it one step at a time together. Have you tried journaling or taking a few deep breaths? [SET_LIGHT:blue] [BREATHING]
"""

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get("message")

    prompt = f"[INST] {SYSTEM_PROMPT}\nUser: {user_message}\nAssistant: [/INST]"

    # === 🔁 Use local Ollama instead of Hugging Face
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "mistral",  # or "phi" or any other local model
                "prompt": prompt,
                "stream": False
            }
        )

        if response.status_code == 200:
            reply = response.json()["response"].strip()
            print(f"\n🤖 LLM Response:\n{reply}")

            # Check for [SET_LIGHT:color] tag
            match = re.search(r"set_light:(\w+)", reply, re.IGNORECASE)
            if match:
                color = match.group(1).lower()
                if color in COLOR_MAP:
                    r, g, b = COLOR_MAP[color]
                else:
                    print(f"⚠️ Unknown color '{color}', using calm as fallback.")
                    r, g, b = COLOR_MAP["calm"]
                set_light_color(GOVEE_IP, r, g, b)

            return jsonify({"response": reply})
        else:
            print("❌ Ollama API error:", response.status_code, response.text)
            return jsonify({"response": "Sorry, the model is currently unavailable."})
    except Exception as e:
        print("❌ Local LLM error:", e)
        return jsonify({"response": "Something went wrong with the local model."})

@app.route('/breathing', methods=['POST'])
def start_breathing():
    breathing_loop(GOVEE_IP)
    return jsonify({"status": "Breathing sequence started"})

if __name__ == '__main__':
    app.run(debug=True)
