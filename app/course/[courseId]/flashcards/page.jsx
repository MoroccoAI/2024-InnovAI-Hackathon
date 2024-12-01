"use client"
import axios from 'axios';
import { useParams } from 'next/navigation'
import React, { useEffect, useState } from 'react'

import {
    Carousel,
    CarouselContent,
    CarouselItem,
    CarouselNext,
    CarouselPrevious,
  } from "@/components/ui/carousel"
import StepProgress from '../_components/StepProgress';
import FlashcardItem from './_components/FlashcardItem';
  
function Flashcards() {

    const {courseId}=useParams();
    const [flashCards,setFlashCards]=useState([]);
    const [isFlipped,setIsFlipped]=useState();
    const [api,setApi]=useState();
    // const [stepCount,setStepCount]=useState(0)

    useEffect(()=>{
        GetFlashCards();
    },[])

    useEffect(()=>{
        if(!api)
        {
            return ;
        }
        api.on('select',()=>{
            setIsFlipped(false);
        })
    },[api])

    const GetFlashCards=async()=>{
        const result=await axios.post('/api/study-type',{
            courseId:courseId,
            studyType:'Flashcard'

        });

        setFlashCards(result?.data);
       
    }

    const handleClick=(index)=>{
        setIsFlipped(!isFlipped)
    }
    
  return (
    <div>
        <h2 className='font-bold text-2xl'>Flashcards</h2>
        <p>Flashcards: The Ultimate Tool to Lock in Concepts!</p>

        <div className=' mt-10'>
        {/* <StepProgress data={flashCards?.content} 
        setStepCount={(v)=>setStepCount(v)} 
        stepCount={stepCount} /> */}

        <Carousel setApi={setApi}>
        <CarouselContent>
            {flashCards?.content&&flashCards.content?.map((flashcard,index)=>(
                <CarouselItem key={index} className="flex items-center justify-center">
                <FlashcardItem handleClick={handleClick} 
                isFlipped={isFlipped}
                flashcard={flashcard}/>
                </CarouselItem>
            ))}

        </CarouselContent>
  <CarouselPrevious />
  <CarouselNext />
</Carousel>

        </div>

  
    </div>
  )
}

export default Flashcards