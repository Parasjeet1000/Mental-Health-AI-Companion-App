# 💬Mental Health AI Companion

A real-time, agentic AI system that responds empathetically to user emotions using a local large language model (LLM), and enhances emotional support through dynamic lighting and breathing guidance. The application is able to chnage the light of compatible Govee lighting models based on the users current mood and provides breathing guidance through the lights.

Note: This application was tested with Govee Glide Lively RGBIC Wall Lights (H610A)
---

## Features

- 🧠 Emotionally intelligent AI chat using **Mistral-7B** (via [Ollama](https://ollama.com))
- 🎨 Mood-based light color changes via **Govee LAN API**
- 💨 AI-triggered breathing exercises with visual and ambient feedback
- 🌈 UI dynamically adapts to emotional tone and lighting
- 🔌 Runs fully **offline** (no Hugging Face/OpenAI tokens needed)

---

## 📸 Demo Highlights

- "I'm anxious" → Light turns **blue**, UI background shifts
- "I feel angry" → Light turns **red**
- "I'm panicking" → AI suggests deep breathing, starts **breathing animation**
- Joyful moments → **mint/gold/sunny** lighting with supportive feedback

---

## 🛠️ Tech Stack

- 🧠 LLM: [`llama3-8b-8192`](https://console.groq.com/) via Groq API
- 💡 Hardware: [Govee Glide Lively RGBIC Wall Lights (H610A)](https://www.govee.com/)
- 🔧 Backend: Python (Flask)
- 🌐 Frontend: React + Tailwind CSS
- 🎨 Real-time light control: UDP → Govee LAN API

---

## 🚀 Getting Started

### 1. 🗝️ Set Up Your Groq API Key

- Sign up at [https://console.groq.com](https://console.groq.com)
- Generate an API key and place it on the line " GROQ_API_KEY = "" " in app.py in the backend folder:

### 2. Run Backend (Flask + Python)

run the following commands:
```bash
cd backend
pip install -r requirements.txt
python app.py
```
### 2. Run Frontend (React)

run the following commands:
```bash
cd frontend
npm install
npm run dev
```



