import React, { useState, useRef, useEffect } from "react";
import axios from "axios";

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [showBreathingButton, setShowBreathingButton] = useState(false);
  const [showBreathingAnim, setShowBreathingAnim] = useState(false);
  const [moodColor, setMoodColor] = useState("sky-50");
  const [isTyping, setIsTyping] = useState(false);
  const timestamp = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  const notificationSoundSend = new Audio("../assets/send.mp3");
  const notificationSoundRecieve = new Audio("../assets/recieve.mp3");
  

  const chatRef = useRef(null);

  const scrollToBottom = () => {
    if (chatRef.current) {
      chatRef.current.scrollTop = chatRef.current.scrollHeight;
    }
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isTyping]);

  const sendMessage = async () => {
    if (!input.trim()) return;
    notificationSoundSend.play();
    const newMessages = [...messages, { sender: "user", text: input, time: timestamp }];
    setMessages(newMessages);
    setInput("");
    setIsTyping(true);

    try {
      const res = await axios.post("http://localhost:5000/chat", {
        message: input,
      });

      const aiReply = res.data.response;

      setTimeout(() => {
        notificationSoundRecieve.play();
        const agentTime = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        setMessages((prev) => [...prev, { sender: "agent", text: aiReply, time: agentTime }]);
        setIsTyping(false);

        if (aiReply.toLowerCase().includes("[breathing]")) {
          setShowBreathingButton(true);
        } else {
          setShowBreathingButton(false);
        }

        const match = aiReply.match(/\[SET_LIGHT:(\w+)\]/i);
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
      }, 1000);
    } catch (error) {
      setMessages([
        ...newMessages,
        { sender: "agent", text: "Oops! Something went wrong." },
      ]);
      setIsTyping(false);
    }
  };

  const handleBreathingClick = async () => {
    try {
      setShowBreathingAnim(true);
      await axios.post("http://localhost:5000/breathing");
  
      setTimeout(() => {setShowBreathingAnim(false);}, 900);
      setShowBreathingButton(false);
    } catch (err) {
      alert("Failed to start breathing mode.");
    }
  };

  return (
    <div
      style={{ backgroundColor: moodColor }}
      className="min-h-screen flex flex-col items-center p-6 transition-colors duration-700 font-sans"
    >
      <h1 className="text-3xl font-bold mb-2">Mental Health Companion 💬</h1>
      <p className="text-gray-600 mb-6 text-center max-w-xl text-sm">
        Talk to your companion about how you're feeling. If you're overwhelmed, it'll offer breathing support and change your environment lighting to help your mood.
      </p>

      <div
        ref={chatRef}
        className="w-full max-w-xl bg-white p-4 rounded-2xl shadow-md space-y-2 overflow-y-auto h-[32rem] transition-all"
      >
        {messages.map((msg, i) => (
          <div
            key={i}
            style={{
              backgroundColor: msg.sender == "user" ? "#007AFF" : "#E5E5EA",
              color: msg.sender == "user" ? "white" : "black",
            }}
            className={`px-4 py-2 rounded-2xl max-w-xs shadow mb-2 ${msg.sender === "user"
                ? "ml-auto text-right"
                : "mr-auto text-left"
              } `}
          >
            <div className="whitespace-pre-wrap">{msg.text}</div>
            <div
              className={`text-xs mt-1 ${msg.sender === "user" ? "text-gray-200" : "text-gray-500"
                }`}
            >
              {msg.time}
            </div>
          </div>
        ))}

        {isTyping && (
          <div className="text-sm text-gray-500 italic">Agent is typing...</div>
        )}
      </div>

      <div className="mt-4 flex w-full max-w-xl">
        <input
          className="flex-grow border rounded-l px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && sendMessage()}
          placeholder="How are you feeling?"
        />
        <button
          className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-r transition"
          onClick={sendMessage}
        >
          Send
        </button>
      </div>

      {showBreathingButton && (
        <button
          className="mt-4 bg-green-500 hover:bg-green-600 text-white px-5 py-2 rounded-xl transition"
          onClick={handleBreathingClick}
        >
          Start Breathing Exercise
        </button>
      )}

      {showBreathingAnim && (
        <div className="mt-6 flex flex-col items-center">
          <div className="w-28 h-28 rounded-full bg-blue-300 animate-pulse-slow" />
          <p className="text-center mt-2 text-sm text-gray-600">
            Breathe with the circle...
          </p>
        </div>
      )}
    </div>
  );
}

export default App;
