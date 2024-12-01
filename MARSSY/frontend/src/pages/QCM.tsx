import { useState } from 'react';
import { MathJax, MathJaxContext } from 'better-react-mathjax';
import axios from 'axios';
import { useAppContext } from "./AppContext";
import { useNavigate } from "react-router-dom"; // Assuming react-router-dom is being used for navigation
import {config} from "../types/LatexConfig";

const QCMApp = () => {
    const { formData, qcmData, setCustomizedCourse, setCustomQcmData, setReport } = useAppContext(); // Assuming `setCustomizedCourse` is part of AppContext
    const [loading, setLoading] = useState<boolean>(false);
    const navigate = useNavigate();

    if (!qcmData || qcmData.length === 0) {
        return <p>No QCM data available. Go back and generate questions first.</p>;
    }

    const [selectedAnswers, setSelectedAnswers] = useState(
        qcmData.map(section => ({
            sous_cours_name: section.sous_cours_name,
            answers: new Array(section.content.length).fill(null),
        }))
    );

    const [submitted, setSubmitted] = useState(false);
    const [submitLabel, setSubmitLabel] = useState("Envoyer les réponses");

    const handleAnswerSelect = (sectionIndex: number, questionIndex: number, optionIndex: number) => {
        const newSelectedAnswers = [...selectedAnswers];
        newSelectedAnswers[sectionIndex].answers[questionIndex] = optionIndex;
        setSelectedAnswers(newSelectedAnswers);
    };

    const handleSubmit = async () => {
        setSubmitted(true);
        setLoading(true);
        try {
            const response = await axios.post(`${import.meta.env.VITE_BACKEND_URL}/submit`, {
                answers: selectedAnswers,
                qcm: qcmData,
                meta: formData,
            });

            // Set the customized course data in the app context
            setCustomizedCourse(response.data["cours"]);
            setCustomQcmData(response.data["custom_qcm"]);
            setReport(response.data["report"]);
            setSubmitLabel("Obtenez votre rapport d'évaluation");
        } catch (error) {
            console.error('Error submitting answers:', error);
        } finally {
            setLoading(false);
        }
    };

    const handleRedirect = () => {
        navigate("/report"); // Redirect to the new page
    };

    return (
        <MathJaxContext config={config}>
            <div
      className="min-h-screen bg-gradient-to-br from-blue-100 to-white flex justify-center items-center"
    >
            <div className="max-w-3xl mx-auto my-6 p-6 bg-white shadow-md rounded-lg">
                <h1 className="text-3xl font-bold mb-6 text-center">QCM Général</h1>

                {qcmData.map((section, sectionIndex) => (
                    <div key={sectionIndex} className="mb-8">
                        <h1 className="text-xl font-bold mb-4">{section.sous_cours_name}</h1>

                        {section.content.map((item, questionIndex) => {
                            const userAnswer = selectedAnswers[sectionIndex].answers[questionIndex];
                            const correctAnswer = item.options.findIndex(
                                option => option.startsWith(item.correct_answer)
                            );

                            return (
                                <div key={questionIndex} className="mb-6">
                                    <MathJax>
                                        <p className="font-semibold mb-3">{`${questionIndex + 1}. ${item.question}`}</p>
                                    </MathJax>

                                    <div className="space-y-2">
                                        {item.options.map((option, optionIndex) => (
                                            <label
                                                key={optionIndex}
                                                className={`block p-3 border rounded cursor-pointer transition-colors 
                        ${
                            submitted
                                ? optionIndex === correctAnswer
                                    ? 'bg-green-100 border-green-500'
                                    : optionIndex === userAnswer && userAnswer !== correctAnswer
                                    ? 'bg-red-100 border-red-500'
                                    : ''
                                : selectedAnswers[sectionIndex].answers[questionIndex] === optionIndex
                                ? 'bg-blue-100 border-blue-500'
                                : 'hover:bg-gray-100'
                        }`}
                                            >
                                                <input
                                                    type="radio"
                                                    name={`question-${sectionIndex}-${questionIndex}`}
                                                    className="mr-3"
                                                    checked={userAnswer === optionIndex}
                                                    onChange={() =>
                                                        handleAnswerSelect(sectionIndex, questionIndex, optionIndex)
                                                    }
                                                />
                                                <MathJax>{option}</MathJax>
                                            </label>
                                        ))}
                                    </div>
                                </div>
                            );
                        })}
                    </div>
                ))}

<button
  onClick={submitted ? handleRedirect : handleSubmit}
  disabled={(!submitted &&
    selectedAnswers.some(section =>
      section.answers.some(answer => answer === null)
    )) || loading}
  className={`w-full py-3 rounded text-white font-bold transition-colors flex justify-center items-center
    ${(!submitted &&
      selectedAnswers.some(section =>
        section.answers.some(answer => answer === null)
      )) || loading
        ? 'bg-gray-400 cursor-not-allowed'
        : 'bg-blue-600 hover:bg-blue-700 active:bg-blue-800'}`}
>
  {loading ? (
    <div className="flex items-center justify-center">
      <svg
        className="animate-spin h-5 w-5 text-white"
        xmlns="http://www.w3.org/2000/svg"
        fill="none"
        viewBox="0 0 24 24"
      >
        <circle
          className="opacity-25"
          cx="12"
          cy="12"
          r="10"
          stroke="currentColor"
          strokeWidth="4"
        ></circle>
        <path
          className="opacity-75"
          fill="currentColor"
          d="M4 12a8 8 0 018-8v8H4z"
        ></path>
      </svg>
      <span className="ml-2">Chargement en cours (cela prendra une minute)...</span>
    </div>
  ) : (
    submitLabel
  )}
</button>
            </div></div>
        </MathJaxContext>
    );
};

export default QCMApp;
