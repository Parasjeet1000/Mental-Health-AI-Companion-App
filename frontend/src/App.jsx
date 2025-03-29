import React, { useState } from "react";
import axios from "axios";

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  const sendMessage = async () => {
    if (!input.trim()) return;

    const newMessages = [...messages, { sender: "user", text: input }];
    setMessages(newMessages);
    setInput("");

    try {
      const res = await axios.post("http://localhost:5000/chat", {
        message: input,
      });

      setMessages([
        ...newMessages,
        { sender: "agent", text: res.data.response },
      ]);
    } catch (error) {
      setMessages([
        ...newMessages,
        { sender: "agent", text: "Oops! Something went wrong." },
      ]);
    }
  };

  return (
    <div className="min-h-screen bg-sky-50 flex flex-col items-center p-4">
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
    </div>
  );
}

export default App;
