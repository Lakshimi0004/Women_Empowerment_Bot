import { useNavigate } from 'react-router-dom';

function SelectChatbot() {
  const navigate = useNavigate();

  const handleSelect = (type) => {
    navigate(`/chatbot/${type}`);
  };
  const handleSelect1 = (type) => {
    navigate(`/chatbot1/${type}`);
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-br from-pink-200 via-purple-200 to-yellow-100">
      <h1 className="text-4xl font-bold mb-10 text-gray-800">Choose Your Chatbot</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <div
          onClick={() => handleSelect('normal')}
          className="cursor-pointer bg-white p-8 rounded-2xl shadow-lg hover:scale-105 transform transition duration-300 flex flex-col items-center"
        >
          <h2 className="text-2xl font-semibold mb-4">🗨️ Women Empowerment / Normal Chat</h2>
          <p className="text-gray-600 text-center">Engage in conversations and get support!</p>
        </div>
        <div
          onClick={() => handleSelect1('mentorship')}
          className="cursor-pointer bg-white p-8 rounded-2xl shadow-lg hover:scale-105 transform transition duration-300 flex flex-col items-center"
        >
          <h2 className="text-2xl font-semibold mb-4">🗨️ MentorShip Chat</h2>
          <p className="text-gray-600 text-center">Mentorship conversations and get support!</p>
        </div>
        <div
          onClick={() => handleSelect('career')}
          className="cursor-pointer bg-white p-8 rounded-2xl shadow-lg hover:scale-105 transform transition duration-300 flex flex-col items-center"
        >
          <h2 className="text-2xl font-semibold mb-4">💼 Career Support Chat</h2>
          <p className="text-gray-600 text-center">Jobs related conversations and get guidance!</p>
        </div>
        <div
          onClick={() => handleSelect('event')}
          className="cursor-pointer bg-white p-8 rounded-2xl shadow-lg hover:scale-105 transform transition duration-300 flex flex-col items-center"
        >
          <h2 className="text-2xl font-semibold mb-4">💼 Event Support Chat</h2>
          <p className="text-gray-600 text-center">Event related conversations and get guidance!</p>
        </div>
      </div>
    </div>
  );
}

export default SelectChatbot;
