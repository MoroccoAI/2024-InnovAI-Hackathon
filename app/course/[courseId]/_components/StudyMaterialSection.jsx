import React, { useEffect, useState } from 'react'
import MaterialCardItem from './MaterialCardItem'
import { db } from '@/configs/db'
import axios from 'axios'
import Link from 'next/link';

function StudyMaterialSection({courseId,course}) {

    const [studyTypeContent,setStudyTypeContent]=useState();
    const MaterialList=[
        {
            name:'Notes/Chapters',
            desc:'Read notes to prepare it',
            icon:'/notes.png',
            path:'/notes',
            type:'notes'
        },
        {
            name:'Flashcard',
            desc:'Flashcard to remember the concepts',
            icon:'/flashcard.png',
            path:'/flashcards',
            type:'flashcard'

        },
        {
            name:'Quiz',
            desc:'Great way to test your knowledge',
            icon:'/quiz.png',
            path:'/quiz',
            type:'quiz'
        },
        {
            name:'Question/Answer',
            desc:'Help to pratice your learning',
            icon:'/qa.png',
            path:'/question_answer',
            type:'qa'
        }
    ]

    useEffect(()=>{
        GetStudyMaterial();
    },[])

    const GetStudyMaterial=async()=>{
        const result=await axios.post('/api/study-type',{
            courseId:courseId,
            studyType:'ALL'
        })

        console.log(result?.data);
        setStudyTypeContent(result.data)
    }


  return (
    <div className='mt-5'>
        <h2 className='font-medium text-xl'>Study Plans </h2>

        <div className='grid grid-cols-2 md:grid-cols-4 gap-5 mt-3'>
            {MaterialList.map((item,index)=>(
                
                <MaterialCardItem item={item} key={index}
                    studyTypeContent={studyTypeContent}
                    course={course}
                    refreshData={GetStudyMaterial}
                />
             
            ))}
        </div>
    </div>
  )
}

export default StudyMaterialSection