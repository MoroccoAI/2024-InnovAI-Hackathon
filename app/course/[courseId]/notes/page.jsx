"use client"
import { Button } from '@/components/ui/button';
import axios from 'axios'
import { useParams, useRouter } from 'next/navigation'
import React, { useEffect, useState } from 'react'
import StepProgress from '../_components/StepProgress';
import EndScreen from '../_components/EndScreen';

function ViewNotes() {

    const {courseId}=useParams();
    const [notes,setNotes]=useState();
    const [stepCount,setStepCount]=useState(0)
    const route=useRouter();
    useEffect(()=>{
        GetNotes();
    },[])

    const GetNotes=async()=>{
        const result=await axios.post('/api/study-type',{
            courseId:courseId,
            studyType:'notes'
        });

        console.log(result?.data);
        setNotes(result?.data);
    }

  return notes&&(
    <div>
        <div className='flex gap-5 items-center'>
           {stepCount!=0&& <Button variant="outline" size="sm" onClick={()=>setStepCount(stepCount-1)}>Previous</Button>}
            {notes?.map((item,index)=>(
                <div key={index} className={`w-full h-2 rounded-full
                ${index<stepCount?'bg-primary':'bg-gray-200'}`}>
                    </div>
            ))}
            <Button variant="outline" size="sm" onClick={()=>setStepCount(stepCount+1)}>Next</Button>

        </div>


        <div className='mt-10 noteClass'>
            <div dangerouslySetInnerHTML={{__html:(notes[stepCount]?.notes)?.replace('```html',' ')}} />
            
             {notes?.length==stepCount&&<div className='flex items-center gap-10 flex-col justify-center'>

                <h2>End of Notes</h2>
                <Button onClick={()=>route.back()}>Go to Course Page</Button>
            </div>}
       
        </div>

    </div>
  )
}

export default ViewNotes