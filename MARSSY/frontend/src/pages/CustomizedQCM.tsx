import { useState } from 'react';
import { MathJax, MathJaxContext } from 'better-react-mathjax';
import { useAppContext } from "./AppContext";
import { useNavigate } from "react-router-dom"; // Assuming react-router-dom is being used for navigation
import {config} from "../types/LatexConfig";

const CustomQCMApp = () => {
    const { customQcmData } = useAppContext(); // Assuming `setCustomizedCourse` is part of AppContext
    const navigate = useNavigate();

    if (!customQcmData || customQcmData.length === 0) {
        return <p>No QCM data available. Go back and generate questions first.</p>;
    }

    const [selectedAnswers, setSelectedAnswers] = useState(
        customQcmData.map(section => ({
            sous_cours_name: section.sous_cours_name,
            answers: new Array(section.content.length).fill(null),
        }))
    );

    const [submitted, setSubmitted] = useState(false);
    const [submitLabel, setSubmitLabel] = useState("Faire corriger");

    const handleAnswerSelect = (sectionIndex: number, questionIndex: number, optionIndex: number) => {
        const newSelectedAnswers = [...selectedAnswers];
        newSelectedAnswers[sectionIndex].answers[questionIndex] = optionIndex;
        setSelectedAnswers(newSelectedAnswers);
    };

    const handleSubmit = async () => {
        setSubmitted(true);
        setSubmitLabel("Terminer");
    };

    const handleRedirect = () => {
        navigate("/"); // Redirect to the new page
    };


    return (
        <MathJaxContext config={config}>
            <div
      className="min-h-screen bg-gradient-to-br from-blue-100 to-white flex justify-center items-center"
    >
            <div className="max-w-3xl mx-auto my-6 p-6 bg-white shadow-md rounded-lg">
                <h1 className="text-3xl font-bold mb-6 text-center">QCM Personnalisé</h1>

                {customQcmData.map((section, sectionIndex) => (
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
    ))}
  className={`w-full py-3 rounded text-white font-bold transition-colors flex justify-center items-center
    ${(!submitted &&
      selectedAnswers.some(section =>
        section.answers.some(answer => answer === null)
      ))
        ? 'bg-gray-400 cursor-not-allowed'
        : 'bg-blue-600 hover:bg-blue-700 active:bg-blue-800'}`}
>
  {submitLabel}
</button>
            </div></div>
        </MathJaxContext>
    );
};

export default CustomQCMApp;
