import { db } from "@/configs/db";
import { inngest } from "./client";
import { CHAPTER_NOTES_TABLE, STUDY_MATERIAL_TABLE, STUDY_TYPE_CONTENT_TABLE, USER_TABLE } from "@/configs/schema";
import { eq } from "drizzle-orm";
import { courseOutlineAIModel, generateNotesAiModel, GenerateQuizAiModel, GenerateStudyTypeContentAiModel } from "@/configs/AiModel";

// Hello World Example
export const helloWorld = inngest.createFunction(
    { id: "hello-world" },
    { event: "test/hello.world" },
    async ({ event, step }) => {
        await step.sleep("wait-a-moment", "1s");
        return { event, body: "Hello, World!" };
    },
);

// Create New User
export const CreateNewUser = inngest.createFunction(
    { id: 'create-user', retries: 1 },
    { event: 'user.create' },
    async ({ event, step }) => {
        const { user } = event.data;

        // Check User and Add to DB if Not Exists
        const result = await step.run('Check User and Create New if Not in DB', async () => {
            const existingUser = await db.select().from(USER_TABLE)
                .where(eq(USER_TABLE.email, user?.primaryEmailAddress?.emailAddress));

            if (existingUser?.length === 0) {
                const userResp = await db.insert(USER_TABLE).values({
                    name: user?.fullName,
                    email: user?.primaryEmailAddress?.emailAddress
                }).returning(USER_TABLE);
                return userResp;
            }

            return existingUser;
        });

        return 'Success';
    }
);

// Generate Notes
export const GenerateNotes = inngest.createFunction(
    { id: 'generate-course', retries: 1 },
    { event: 'notes.generate' },
    async ({ event, step }) => {
        const { course } = event.data;

        // Generate Notes for Each Chapter with AI
        const notesResult = await step.run('Generate Chapter Notes', async () => {
            const Chapters = course?.courseLayout?.chapters;
            let index = 0;

            for (const chapter of Chapters) {
                const PROMPT = `
Generate comprehensive learning material for the course type: ${course?.courseType}.
Provide detailed content for each chapter, including:
1. **Notes for each topic**: Clearly explain key concepts with examples or real-world applications.
2. **Highlighted key points**: Use proper emphasis (e.g., bold or mark important points) to make the content engaging and easier to review.
3. **Code examples or calculations**: Where applicable, include code snippets or problem-solving examples enclosed in <precode> tags.
4. **Interactive and styled content**: Use appropriate styling for headings, lists, and emphasis to create an organized and visually appealing layout.
5. **Supplementary visuals**: Include suggestions for diagrams, tables, or flowcharts where relevant.
6. **Actionable insights**: Summarize each chapter with actionable insights or practical tips for learners.

Provide the response in **HTML format** (excluding HTML, Head, Body, and Title tags), ready for direct rendering. Add Tailwind CSS styles to ensure a visually appealing and responsive presentation.

**Important**:
- The response must be in the same language as the chapter details (${chapter || "default english"}). For example, if the chapter details are in French, generate the content in French; if in Arabic, generate it in Arabic, and so on.
- Adapt the content to the course field and ensure it is suitable for beginners to advanced learners.

The chapter details are as follows: ${JSON.stringify(chapter)}
`;


                const result = await generateNotesAiModel.sendMessage(PROMPT);
                const aiResp = await result.response.text();

                await db.insert(CHAPTER_NOTES_TABLE).values({
                    chapterId: index,
                    courseId: course?.courseId,
                    notes: aiResp
                });

                index += 1;
            }

            return Chapters;
        });

        // Update Status to 'Ready'
        await step.run('Update Course Status to Ready', async () => {
            await db.update(STUDY_MATERIAL_TABLE).set({
                status: 'Ready'
            }).where(eq(STUDY_MATERIAL_TABLE.courseId, course?.courseId));
        });

        return 'Notes Generated Successfully';
    }
);

// Generate Study Type Content
export const GenerateStudyTypeContent = inngest.createFunction(
    { id: 'generate-study-type-content', retries: 1 },
    { event: 'studyType.content' },
    async ({ event, step }) => {
        const { studyType, prompt, courseId, recordId } = event.data;

        // Generate Content using AI
        const AiResult = await step.run('Generate Content using AI', async () => {
            const result = studyType === 'Flashcard'
                ? await GenerateStudyTypeContentAiModel.sendMessage(prompt)
                : await GenerateQuizAiModel.sendMessage(prompt);

            return JSON.parse(await result.response.text());
        });

        // Save the Result to DB
        await step.run('Save Result to DB', async () => {
            await db.update(STUDY_TYPE_CONTENT_TABLE).set({
                content: AiResult,
                status: 'Ready'
            }).where(eq(STUDY_TYPE_CONTENT_TABLE.id, recordId));
        });

        return 'Study Type Content Generated Successfully';
    }
);
