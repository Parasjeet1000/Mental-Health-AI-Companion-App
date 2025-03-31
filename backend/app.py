from flask import Flask, request, jsonify
import requests
from flask_cors import CORS
import socket
import json
import re
from breathing_light import breathing_loop

app = Flask(__name__)
CORS(app)

GROQ_API_KEY = ""
# === Govee LAN Light Setup ===
GOVEE_IP = "10.0.0.68"  # Your light bar's LAN IP
#GOVEE_IP = "172.20.10.3"

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

# === SYSTEM PROMPT
SYSTEM_PROMPT = """
You are a kind and supportive mental health companion.
Speak gently, ask reflective questions, and encourage self-care
and suggest small, helpful actions like journaling, taking a break, talking to someone, or reflecting on emotions.

You can suggest deep breathing only when it's truly necessary — not in every response.

---

When a user expresses:
- Anxiety or overwhelm → respond with empathy and end the message with [SET_LIGHT:blue] or [SET_LIGHT:calm]
- Burnout or fatigue → [SET_LIGHT:warm]
- Sadness or heartbreak → [SET_LIGHT:pink]
- Anger or stress → [SET_LIGHT:red]
- Mindfulness or groundedness → [SET_LIGHT:green]
- Positivity or joy → [SET_LIGHT:gold], [SET_LIGHT:sunny], or [SET_LIGHT:mint]

You must follow these rules exactly:

1. Only include ONE [SET_LIGHT:color] tag per message, at the END of the message.
2. The color must be exactly one of: blue, calm, warm, red, pink, green, gold, sunny, mint.
3. Never include more than one light tag.
4. Never place the [SET_LIGHT:color] tag anywhere but the very end.
5. Never invent or suggest a color outside the approved list.

---

If the user is experiencing **intense emotional distress**, you MAY include a [BREATHING] tag — but ONLY in these specific situations:

- Panic or spiraling thoughts  
- Racing heart or shortness of breath  
- Feeling physically overwhelmed or out of control  
- Sudden breakdowns or emotional overload  
- User directly asks for a calming exercise or help with breathing

If the user sounds mildly stressed, annoyed, sad, angry, or just venting — **do NOT include [BREATHING]**.

Also:  
Do not casually suggest breathing exercises in every reply. Only bring up deep breathing if the user truly needs it or asks for it.

If a [BREATHING] tag is included, it should appear at the very end — directly after the [SET_LIGHT:color] tag.

Example format (if both are used):
[SET_LIGHT:blue] [BREATHING]




"""


@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get("message")

    prompt = f"[INST] {SYSTEM_PROMPT}\nUser: {user_message}\nAssistant: [/INST]"

    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama-3.3-70b-versatile",  # You can also try "llama2-70b-chat"
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_message}
                ],
                "temperature": 0.7
            }
        )

        if response.status_code == 200:
            reply = response.json()["choices"][0]["message"]["content"].strip()
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
            print("❌ Groq API error:", response.status_code, response.text)
            return jsonify({"response": "Sorry, the model is currently unavailable."})
    except Exception as e:
        print("❌ Groq API error:", e)
        return jsonify({"response": "Something went wrong with the Groq model."})


@app.route('/breathing', methods=['POST'])
def start_breathing():
    from breathing_light import breathing_loop
    breathing_loop(GOVEE_IP, cycles=3)
    return jsonify({"status": "Breathing sequence started"})


if __name__ == '__main__':
    app.run(debug=True)
