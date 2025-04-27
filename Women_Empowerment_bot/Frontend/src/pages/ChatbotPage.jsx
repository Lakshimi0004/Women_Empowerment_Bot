import { useParams, useNavigate } from 'react-router-dom';
import Chatbot from '../components/Chatbot';

function ChatbotPage() {
  const { type } = useParams();
  const navigate = useNavigate();

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-br from-purple-100 via-blue-100 to-pink-100 p-4">
      <button
        onClick={() => navigate('/')}
        className="self-start mb-6 px-4 py-2 bg-purple-500 text-white rounded hover:bg-purple-600"
      >
        ⬅️ Back
      </button>
      <h1 className="text-3xl font-bold mb-4 text-gray-800">
        {type === 'normal' ? '🗨️ Empowerment Chatbot' : '💼 Career Support Chatbot'}
      </h1>
      <Chatbot type={type} />
    </div>
  );
}

export default ChatbotPage;
