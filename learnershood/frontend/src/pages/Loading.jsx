import { useEffect, useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { RefreshCw } from "lucide-react";
import { saveStory } from "../utils/storage";
import { motion } from "framer-motion";

const stages = [
  { id: 0, title: "Generating Transcript" },
  { id: 1, title: "Generating Audio" },
  { id: 2, title: "Generating Visual" },
  { id: 3, title: "Generating Quiz" },
];

function Loading() {
  const [currentStage, setCurrentStage] = useState(0);
  const [error, setError] = useState(null);
  const [transcript, setTranscript] = useState(null);
  const [title, setTitle] = useState(null);
  const [audio, setAudio] = useState(null);
  const [images, setImages] = useState([]);
  const [quiz, setQuiz] = useState([]);

  const navigate = useNavigate();

  const location = useLocation();
  const queryParams = new URLSearchParams(location.search);
  const query = queryParams.get("query");

  const processStage = async (stageIndex) => {
    const formInput = [
      {
        url: `${import.meta.env.VITE_BACKEND_ENDPOINT}/api/generate-transcript`,
        options: { topic: query },
      },
      {
        url: `${import.meta.env.VITE_BACKEND_ENDPOINT}/api/generate-audio`,
        options: { transcript },
      },
      {
        url: `${import.meta.env.VITE_BACKEND_ENDPOINT}/api/generate-image`,
        options: { transcript, title },
      },
      {
        url: `${import.meta.env.VITE_BACKEND_ENDPOINT}/api/generate-quiz`,
        options: { transcript, title },
      },
      {
        url: `${import.meta.env.VITE_BACKEND_ENDPOINT}/api/story/create`,
        options: {
          title,
          transcript,
          audio,
          images,
          quiz,
        },
      },
    ];

    try {
      const response = await fetch(formInput[stageIndex].url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ ...formInput[stageIndex].options }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      if (!data.data) {
        throw new Error(`Returned an empty value.`);
      }

      let storyId;

      // Update state based on the specific stage
      switch (stageIndex) {
        case 0:
          setTranscript(data.data.transcript);
          setTitle(data.data.title);

          console.log({
            title: data.data.title,
            transcript: data.data.transcript,
          })
          break;
        case 1:
          setAudio(data.data);

          console.log({
            audio: data.data,
          })
          break;
        case 2:
          setImages(data.data);

          console.log({
            images: data.data,
          })
          break;
        case 3:
          setQuiz(data.data);
          
          console.log({
            quiz: data.data,
          })
          break;
        case 4:
          storyId = data.data;
          
          console.log({
            storyId: data.data,
          })
          break;
        default:
          break;
      }

      if (stageIndex === stages.length) {
        // Save generated story to local storage
        const story = { 
          _id: storyId, 
          title,
          images, 
          createdAt: Date.now()
        };
        saveStory(story);

        navigate(`/story/${storyId}`);
      } else {
        setCurrentStage(stageIndex + 1);
      }
    } catch (err) {
      console.error("Error during stage processing:", err);
      setError(stageIndex);
    }
  };

  console.log({error}) 

  useEffect(() => {
    if (error === null && currentStage <= stages.length) {
      processStage(currentStage);
    }
  }, [currentStage, error]);

  const handleRetry = () => {
    if (error !== null) {
      processStage(error);
      setError(null);
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="min-h-screen flex items-center justify-center"
    >
      <div className="max-w-md w-full mx-4">
        <div className="text-center mb-8">
          <h2 className="text-2xl font-bold text-indigo-600 mb-2">
            Creating your story
          </h2>
          <p className="text-gray-600">Please wait while we work our magic</p>
        </div>

        <div className="space-y-4">
          {stages.map((stage, index) => (
            <motion.div
              key={stage.id}
              initial={{ opacity: 0.5 }}
              animate={{
                opacity: index <= currentStage ? 1 : 0.5,
                scale: index === currentStage ? 1.05 : 1,
              }}
              className="bg-white rounded-lg p-4 shadow-md"
            >
              <div className="flex items-center justify-between">
                <span className="text-gray-800">{stage.title}</span>
                {error === index ? (
                  <button
                    onClick={handleRetry}
                    className="flex items-center space-x-2 text-red-600 hover:text-red-700"
                  >
                    <RefreshCw className="w-5 h-5" />
                    <span>Retry</span>
                  </button>
                ) : index < currentStage ? (
                  <motion.div
                    initial={{ scale: 0 }}
                    animate={{ scale: 1 }}
                    className="w-6 h-6 bg-green-500 rounded-full flex items-center justify-center"
                  >
                    <svg
                      className="w-4 h-4 text-white"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M5 13l4 4L19 7"
                      />
                    </svg>
                  </motion.div>
                ) : index === currentStage && error === null ? (
                  <motion.div
                    animate={{
                      scale: [1, 1.2, 1],
                      rotate: [0, 360],
                    }}
                    transition={{
                      duration: 2,
                      repeat: Infinity,
                      ease: "linear",
                    }}
                    className="w-6 h-6 border-4 border-indigo-600 border-t-transparent rounded-full"
                  />
                ) : null}
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </motion.div>
  );
}

export default Loading;
