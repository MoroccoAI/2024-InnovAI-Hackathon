import { db } from "@/configs/db";
import { CHAPTER_NOTES_TABLE, STUDY_TYPE_CONTENT_TABLE } from "@/configs/schema";
import { and, eq } from "drizzle-orm";
import { NextResponse } from "next/server";

// Handler function for the POST request
export async function POST(req) {
    try {
        // Parse the incoming request payload
        const { courseId, studyType } = await req.json();

        // Validate the incoming data
        if (!courseId || !studyType) {
            return NextResponse.json({ error: "Missing courseId or studyType" }, { status: 400 });
        }

        // Fetch data based on the `studyType`
        if (studyType === 'ALL') {
            return await getAllStudyMaterials(courseId);
        } else if (studyType === 'notes') {
            return await getNotes(courseId);
        } else {
            return await getSpecificStudyMaterial(courseId, studyType);
        }
    } catch (error) {
        console.error("Error handling POST request:", error);
        return NextResponse.json({ error: "Internal Server Error" }, { status: 500 });
    }
}

// Function to fetch all study materials (notes, flashcards, quizzes, QA)
async function getAllStudyMaterials(courseId) {
    const notes = await db.select().from(CHAPTER_NOTES_TABLE)
        .where(eq(CHAPTER_NOTES_TABLE.courseId, courseId));

    const contentList = await db.select().from(STUDY_TYPE_CONTENT_TABLE)
        .where(eq(STUDY_TYPE_CONTENT_TABLE.courseId, courseId));

    const result = {
        notes,
        flashcard: contentList.filter(item => item.type === 'Flashcard'),
        quiz: contentList.filter(item => item.type === 'Quiz'),
        qa: contentList.filter(item => item.type === 'Question/Answer'),
    };

    return NextResponse.json(result);
}

// Function to fetch notes
async function getNotes(courseId) {
    const notes = await db.select().from(CHAPTER_NOTES_TABLE)
        .where(eq(CHAPTER_NOTES_TABLE.courseId, courseId));

    return NextResponse.json(notes);
}

// Function to fetch specific study material by type
async function getSpecificStudyMaterial(courseId, studyType) {
    const result = await db.select().from(STUDY_TYPE_CONTENT_TABLE)
        .where(
            and(
                eq(STUDY_TYPE_CONTENT_TABLE.courseId, courseId),
                eq(STUDY_TYPE_CONTENT_TABLE.type, studyType)
            )
        );

    return NextResponse.json(result[0] ?? []);
}
