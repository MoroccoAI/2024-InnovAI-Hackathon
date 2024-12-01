import { db } from "@/configs/db";
import { STUDY_TYPE_CONTENT_TABLE } from "@/configs/schema";
import { inngest } from "@/inngest/client";
import { NextResponse } from "next/server";

// Function to get the prompt based on the study type
function getPromptByType(type, chapters) {
    switch (type) {
        case 'Flashcard':
            return `Generate flashcards on the topic: ${chapters} in JSON format with "front" and "back" content. Limit to a maximum of 15 flashcards.`;

        case 'Question/Answer' :
            return `Generate a Question and Answer list on the topic: ${chapters} in JSON format with the following structure:
{
  "questions": [
    {
      "question": "What is machine learning?",
      "answer": "Machine learning (ML) is a branch of artificial intelligence (AI) and computer science which focuses on the use of data and algorithms to imitate the way that humans learn, gradually improving its accuracy."
    },
    ...
  ]
}
Limit the number of qaPairs to a maximum of 10. Ensure each question is clear, and the answers are detailed and accurate.`;

        case 'Quiz':
            return `Generate a quiz on the topic: ${chapters} in JSON format with questions, multiple-choice options, and the correct answer for each. Limit to a maximum of 10 questions.`;

        default:
            throw new Error("Invalid type provided");
    }
}

export async function POST(req) {
    const { chapters, courseId, type } = await req.json();

    try {
        // Get the appropriate prompt using the helper function
        const PROMPT = getPromptByType(type, chapters);
        console.log(PROMPT)

        // Insert record into the database and set status to "Generating..."
        const result = await db.insert(STUDY_TYPE_CONTENT_TABLE).values({
            courseId: courseId,
            type: type,
        }).returning({ id: STUDY_TYPE_CONTENT_TABLE.id });

        // Trigger Inngest function with the generated prompt
        await inngest.send({
            name: 'studyType.content',
            data: {
                studyType: type,
                prompt: PROMPT,
                courseId: courseId,
                recordId: result[0].id,
            },
        });

        // Return the newly created record ID
        return NextResponse.json(result[0].id);
    } catch (error) {
        // Handle invalid type or other errors
        return NextResponse.json({ error: error.message }, { status: 400 });
    }
}
