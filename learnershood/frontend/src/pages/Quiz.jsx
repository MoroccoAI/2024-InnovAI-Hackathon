import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { CheckCircle, XCircle, ArrowRight } from 'lucide-react';
import { getRandomQuizzes } from '../utils/quiz';

function Quiz() {
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [selectedAnswer, setSelectedAnswer] = useState(null);
  const [showResult, setShowResult] = useState(false);
  const [score, setScore] = useState(0);
  const [quizzes, setQuizzes] = useState([]);
  const navigate = useNavigate();
  const { id } = useParams();

  const initializeData = async () => {
    try {
      const url = `${import.meta.env.VITE_BACKEND_ENDPOINT}/api/story/get/${id}`;

      const response = await fetch(url, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      
      if (data.error) {
        throw new Error(data.error);
      }

      setQuizzes(getRandomQuizzes(data.data.quiz, 5));

      return data.data.quiz;
    } catch (error) {
      console.error('API Error:', error);
    }
  }

  useEffect(() => {
    initializeData()
  }, []);

  const handleAnswer = (index) => {
    setSelectedAnswer(index);
  };

  const handleConfirm = () => {
    if (selectedAnswer === null) return;
    
    setShowResult(true);
    if (selectedAnswer === quizzes[currentQuestion].correctAnswer) {
      setScore(score + 1);
    }
  };

  const handleNext = () => {
    if (currentQuestion < quizzes.length - 1) {
      setCurrentQuestion(currentQuestion + 1);
      setSelectedAnswer(null);
      setShowResult(false);
    } else {
      navigate(`/story/${id}`);
    }
  };

  if (quizzes.length === 0) return null;

  const question = quizzes[currentQuestion];

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="min-h-screen bg-gradient-to-br from-indigo-50 to-purple-50 pb-safe"
    >
      <div className="max-w-lg mx-auto px-4 py-6">
        <div className="bg-white rounded-2xl shadow-lg p-6">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-xl font-bold text-indigo-600">
              Question {currentQuestion + 1}/{quizzes.length}
            </h2>
            <span className="text-lg font-semibold text-gray-600">
              Score: {score}
            </span>
          </div>

          <motion.div
            key={question.id}
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            className="mb-6"
          >
            <h3 className="text-lg text-gray-800 mb-4">{question.question}</h3>
            <div className="space-y-3">
              {question.options.map((option, index) => (
                <button
                  key={index}
                  onClick={() => !showResult && handleAnswer(index)}
                  disabled={showResult}
                  className={`w-full p-4 rounded-xl text-left transition-all ${
                    showResult
                      ? index === question.correctAnswer
                        ? 'bg-green-100 border-green-500'
                        : index === selectedAnswer
                        ? 'bg-red-100 border-red-500'
                        : 'bg-gray-50 border-gray-200'
                      : index === selectedAnswer
                      ? 'bg-indigo-100 border-indigo-500'
                      : 'bg-gray-50 hover:bg-gray-100 border-gray-200'
                  } border-2 active:scale-98`}
                >
                  <div className="flex items-center justify-between">
                    <span>{option}</span>
                    {showResult && index === question.correctAnswer && (
                      <CheckCircle className="w-5 h-5 text-green-500" />
                    )}
                    {showResult && index === selectedAnswer && index !== question.correctAnswer && (
                      <XCircle className="w-5 h-5 text-red-500" />
                    )}
                  </div>
                </button>
              ))}
            </div>
          </motion.div>

          <div className="flex justify-end space-x-3">
            {!showResult && (
              <button
                onClick={handleConfirm}
                disabled={selectedAnswer === null}
                className={`flex items-center space-x-2 px-6 py-3 rounded-full transition-colors ${
                  selectedAnswer === null
                    ? 'bg-gray-200 text-gray-500 cursor-not-allowed'
                    : 'bg-indigo-600 text-white hover:bg-indigo-700 active:scale-95'
                }`}
              >
                <span>Confirm Answer</span>
              </button>
            )}
            {showResult && (
              <motion.button
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                onClick={handleNext}
                className="flex items-center space-x-2 bg-indigo-600 text-white px-6 py-3 rounded-full hover:bg-indigo-700 transition-colors active:scale-95"
              >
                <span>
                  {currentQuestion === quizzes.length - 1
                    ? 'Finish'
                    : 'Next Question'}
                </span>
                <ArrowRight className="w-5 h-5" />
              </motion.button>
            )}
          </div>
        </div>
      </div>
    </motion.div>
  );
}

export default Quiz;