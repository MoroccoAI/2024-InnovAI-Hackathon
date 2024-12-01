import React from "react";

function QAItem({ questionData }) {
    return questionData ? (
        <div className="mt-10 p-5">
            <h2 className="font-medium text-3xl text-center">{questionData.question}</h2>
            <p className="text-lg text-gray-700 mt-5">{questionData.answer}</p>
        </div>
    ) : null;
}

export default QAItem;
