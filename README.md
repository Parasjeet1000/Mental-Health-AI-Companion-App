# 💬Mental Health AI Companion

A real-time, agentic AI system that responds empathetically to user emotions using a local large language model (LLM), and enhances emotional support through dynamic lighting and breathing guidance.

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

- 🧠 LLM: [`mistral`](https://ollama.com/library/mistral) via [Ollama](https://ollama.com)
- 💡 Hardware: [Govee Light Bar](https://www.govee.com/)
- 🔧 Backend: Python (Flask)
- 🌐 Frontend: React + Tailwind CSS
- 🎨 Real-time light control: UDP → Govee LAN API

---

## 🚀 Getting Started

### 1. Install [Ollama](https://ollama.com/download) (Windows/macOS/Linux)

then run the fowllowing commands
ollama pull mistral
ollama run mistral


