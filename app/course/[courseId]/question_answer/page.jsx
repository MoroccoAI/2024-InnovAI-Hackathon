"use client";

import axios from "axios";
import { useParams } from "next/navigation";
import React, { useEffect, useState } from "react";
import StepProgress from "../_components/StepProgress";
import QAItem from "./_components/QAItem";
import EndScreen from "../_components/EndScreen";

function QAPage() {
    const { courseId } = useParams();
    const [qaData, setQAData] = useState({ content: { questions: [] } }); // Default structure
    const [stepCount, setStepCount] = useState(0);

    useEffect(() => {
        fetchQAs();
    }, [courseId]);

    const fetchQAs = async () => {
        console.log(courseId); // Debug courseId
        try {
            const result = await axios.post("/api/study-type", {
                courseId: courseId,
                studyType: "Question/Answer",
            });

            console.log("QA Data:", result.data); // Debug response
            setQAData(result.data);
        } catch (error) {
            console.error("Error fetching Q&A data:", error);
            setQAData({ content: { questions: [] } }); // Fallback in case of error
        }
    };

    return (
        <div>
            <h2 className="font-bold text-2xl text-center mb-4">Q&A</h2>

            <StepProgress
                data={qaData?.content?.questions}
                stepCount={stepCount}
                setStepCount={(value) => setStepCount(value)}
            />

            <div>
                {qaData?.content?.questions?.length > 0 ? (
                    qaData.content.questions[stepCount] && (
                        <QAItem questionData={qaData.content.questions[stepCount]} />
                    )
                ) : (
                    <p>Loading questions or no data available.</p>
                )}
            </div>

            <EndScreen data={qaData?.content?.questions} stepCount={stepCount} />
        </div>
    );
}

export default QAPage;
