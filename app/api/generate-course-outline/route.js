import { courseOutlineAIModel } from "@/configs/AiModel";
import { db } from "@/configs/db";
import { STUDY_MATERIAL_TABLE } from "@/configs/schema";
import { inngest } from "@/inngest/client";
import { NextResponse } from "next/server";

export async function POST(req) {

    const {courseId,topic,courseType,difficultyLevel,createdBy}=await req.json();

    const PROMPT = `
Generate a comprehensive study material outline for the topic: "${topic}". 
Ensure the material is suitable for a difficulty level of "${difficultyLevel}". 

The output should include the following:
1. **Course Title**: Provide a concise, engaging, and descriptive title for the course.
2. **Course Summary**: Write a brief summary of the course, highlighting its objectives, target audience, and key takeaways.
3. **List of Chapters** (Maximum of 3): 
   - Include a creative and descriptive title for each chapter.
   - Provide a brief summary of each chapter (2-3 sentences).
   - Suggest an appropriate emoji icon to represent each chapter.
4. **Topics List**: Include a list of topics covered in each chapter to give a clear structure to the material.

**Important**:
- The output must be generated in the same language as the topic. For example, if the topic is in French, generate the content in French; if in Arabic, generate it in Arabic, and so on. Adjust the tone and phrasing to suit the language context appropriately.

Ensure the output is returned in **valid JSON format**, structured as follows:
{
  "title": "Course Title",
  "summary": "Course Summary",
  "chapters": [
    {
      "title": "Chapter 1 Title",
      "summary": "Chapter 1 Summary",
      "emoji": "📘",
      "topics": ["Topic 1", "Topic 2", "Topic 3"]
    },
    {
      "title": "Chapter 2 Title",
      "summary": "Chapter 2 Summary",
      "emoji": "📙",
      "topics": ["Topic 1", "Topic 2", "Topic 3"]
    },
    {
      "title": "Chapter 3 Title",
      "summary": "Chapter 3 Summary",
      "emoji": "📗",
      "topics": ["Topic 1", "Topic 2", "Topic 3"]
    }
  ]
}

Focus on creating a user-friendly and engaging output that makes the material easy to understand and visually appealing.
`;

    // Generate Course Layout using AI
    const aiResp=await courseOutlineAIModel.sendMessage(PROMPT);
    const aiResult= JSON.parse(aiResp.response.text());

    // Save the result along with User Input
    const dbResult=await db.insert(STUDY_MATERIAL_TABLE).values({
        courseId:courseId,
        courseType:courseType,
        createdBy:createdBy,
        topic:topic,
        courseLayout:aiResult
    }).returning({resp:STUDY_MATERIAL_TABLE})

    //Trigger the Inngest function to generate chapter notes

    inngest.send({
        name:'notes.generate',
        data:{
            course:dbResult[0].resp
        }
    });
    // console.log(result);
    
    return NextResponse.json({result:dbResult[0]})
    
}