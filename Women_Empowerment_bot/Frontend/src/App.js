import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import SelectChatbot from './pages/SelectChatbot';
import ChatbotPage from './pages/ChatbotPage';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<SelectChatbot />} />
        <Route path="/chatbot/:type" element={<ChatbotPage />} />
        <Route path="/chatbot1/:type" element={<ChatbotPage />} />
      </Routes>
    </Router>
  );
}

export default App;
