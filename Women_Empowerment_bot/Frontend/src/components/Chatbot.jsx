import { useState, useRef, useEffect } from 'react';
import axios from 'axios';

function Chatbot({ type }) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isBotTyping, setIsBotTyping] = useState(false);
  const [selectedFile, setSelectedFile] = useState(null);
  const recognitionRef = useRef(null);
  const messagesEndRef = useRef(null);

  const endpoint =
    type === 'normal'
      ? 'http://127.0.0.1:8000/chat'
      : 'http://127.0.0.1:8000/search_jobs';

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = { sender: 'user', text: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput('');

    try {
      setIsBotTyping(true);
      const response = 
      type === 'normal'
      ? await axios.post(endpoint, { message: input })
      : await axios.post(endpoint, { query: input })

      // const response = await axios.post(endpoint, { message: input });
      
      const botReplyText = response.data.response || "Sorry, I didn't understand.";

      setTimeout(() => {
        const botReply = { sender: 'bot', text: botReplyText };
        setMessages((prev) => [...prev, botReply]);
        setIsBotTyping(false);
      }, 1000);
    } catch (error) {
      console.error(error);
      const errorReply = { sender: 'bot', text: "Error contacting server. Please try again." };
      setMessages((prev) => [...prev, errorReply]);
      setIsBotTyping(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter') {
      sendMessage();
    }
  };

  const handleVoiceInput = () => {
    if (!('webkitSpeechRecognition' in window)) {
      alert('Voice recognition not supported in this browser.');
      return;
    }

    if (!recognitionRef.current) {
      recognitionRef.current = new window.webkitSpeechRecognition();
      recognitionRef.current.continuous = false;
      recognitionRef.current.interimResults = false;
      recognitionRef.current.lang = 'en-US';

      recognitionRef.current.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        setInput(transcript);
      };

      recognitionRef.current.onerror = (event) => {
        console.error(event.error);
      };
    }
    recognitionRef.current.start();
  };

  // 👇 Auto-scroll to bottom whenever messages change
  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages, isBotTyping]);

  return (
    <div className="w-full md:w-2/3 lg:w-1/2 bg-white p-6 rounded-2xl shadow-lg flex flex-col h-[80vh]">
      <div className="flex-1 overflow-y-auto mb-4 p-4 bg-gray-100 rounded-lg">
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`mb-2 flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div className={`p-3 rounded-lg max-w-xs ${msg.sender === 'user' ? 'bg-purple-300 text-right' : 'bg-gray-300 text-left'}`}>
              {msg.text}
              {/* Display file as a clickable link or preview */}
              {msg.file && (
                <div className="mt-2">
                  {msg.file.endsWith('.pdf') || msg.file.endsWith('.txt') ? (
                    <a href={msg.file} target="_blank" className="text-blue-600">
                      Open File
                    </a>
                  ) : (
                    <img src={msg.file} alt="Uploaded file" className="max-w mt-2 rounded-lg" />
                  )}
                </div>
              )}
            </div>
          </div>
        ))}

        {/* Typing animation */}
        {isBotTyping && (
          <div className="flex justify-start mb-2">
            <div className="p-3 rounded-lg max-w-xs bg-gray-300 text-left animate-pulse">
              Typing...
            </div>
          </div>
        )}

        {/* Dummy div to scroll to */}
        <div ref={messagesEndRef} />
      </div>

      <div className="flex gap-2">
        <input
          type="text"
          placeholder="Type your message..."
          className="flex-1 p-3 border rounded-l-lg"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
        />
        <button
          onClick={sendMessage}
          className="bg-purple-800 text-white px-6 rounded-r-lg hover:bg-purple-600"
        >
          Send
        </button>
      </div>

      <div className="flex gap-4 justify-center mt-4">
        <button
          onClick={handleVoiceInput}
          className="flex items-center gap-2 text-purple-600 border border-purple-600 px-4 py-2 rounded-full hover:bg-purple-50"
        >
          🎙 Voice Input
        </button>
      </div>
    </div>
  );
}

export default Chatbot;
