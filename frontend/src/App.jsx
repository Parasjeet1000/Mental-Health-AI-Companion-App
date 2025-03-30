import React, { useState } from "react";
import axios from "axios";

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [showBreathingButton, setShowBreathingButton] = useState(false);
  const [showBreathingAnim, setShowBreathingAnim] = useState(false);
  const [moodColor, setMoodColor] = useState("sky-50"); // default



  const sendMessage = async () => {
    if (!input.trim()) return;

    const newMessages = [...messages, { sender: "user", text: input }];
    setMessages(newMessages);
    setInput("");

    try {
      const res = await axios.post("http://localhost:5000/chat", {
        message: input,
      });

      const aiReply = res.data.response;

      // Add AI response to chat
      setMessages([
        ...newMessages,
        { sender: "agent", text: aiReply },
      ]);

      // Check if response includes [BREATHING] tag
      if (aiReply.toLowerCase().includes("[breathing]")) {
        setShowBreathingButton(true);
      } else {
        setShowBreathingButton(false);
      }
      const match = res.data.response.match(/\[SET_LIGHT:(\w+)\]/i);
if (match) {
  const color = match[1].toLowerCase();

  const colorMap = {
    blue: "rgb(0, 0, 255)",
    calm: "rgb(135, 206, 235)",
    warm: "rgb(255, 165, 0)",
    red: "rgb(255, 0, 0)",
    green: "rgb(0, 255, 0)",
    pink: "rgb(255, 105, 180)",
    gold: "rgb(255, 223, 0)",
    sunny: "rgb(255, 240, 140)",
    mint: "rgb(166, 248, 230)",
  };

  if (colorMap[color]) {
    setMoodColor(colorMap[color]);
  }
}


    } catch (error) {
      setMessages([
        ...newMessages,
        { sender: "agent", text: "Oops! Something went wrong." },
      ]);
    }
  };

  const handleBreathingClick = async () => {
    try {
      setShowBreathingAnim(true);
      await axios.post("http://localhost:5000/breathing");
      
      setTimeout(() => setShowBreathingAnim(false), 800);
      setShowBreathingButton(false);
    } catch (err) {
      alert("Failed to start breathing mode.");
    }
  };

  return (
    <div
  style={{ backgroundColor: moodColor }}
  className="min-h-screen flex flex-col items-center p-4 transition-colors duration-700"
>
      <h1 className="text-2xl font-bold mb-4">Mental Health Companion 💬</h1>

      <div className="w-full max-w-xl bg-white p-4 rounded shadow space-y-2 overflow-y-auto h-96">
        {messages.map((msg, i) => (
          <div
            key={i}
            className={`p-2 rounded ${
              msg.sender === "user"
                ? "bg-blue-100 text-right"
                : "bg-green-100 text-left"
            }`}
          >
            {msg.text}
          </div>
        ))}
      </div>

      <div className="mt-4 flex w-full max-w-xl">
        <input
          className="flex-grow border rounded-l px-3 py-2"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && sendMessage()}
        />
        <button
          className="bg-blue-500 text-white px-4 py-2 rounded-r"
          onClick={sendMessage}
        >
          Send
        </button>
      </div>

      {showBreathingButton && (
        <button
          className="mt-4 bg-green-500 text-white px-4 py-2 rounded"
          onClick={handleBreathingClick}
        >
          Start Breathing Exercise
        </button>
      )}
      {showBreathingAnim && (
  <div className="mt-6">
    <div className="w-24 h-24 mx-auto rounded-full bg-blue-300 animate-breath" />
    <p className="text-center mt-2 text-sm text-gray-500">Breathe with the circle...</p>
  </div>
)}

    </div>
  );
}

export default App;
