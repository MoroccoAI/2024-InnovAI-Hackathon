import { Textarea } from '@/components/ui/textarea'
import React from 'react'
import {
    Select,
    Input,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
  } from "@/components/ui/select"
import SelectOption from "@/app/create/_components/SelectOption";

  
function TopicInput({setTopic,setDifficultyLevel}) {
  return (
      <div className='mt-10 w-full flex flex-col'>


          <br/>
          <h2>Enter topic or paster the content for which you want to generate study material plan</h2>

          <Textarea placeholder='Start writing here'
                    className="mt-2 w-full" onChange={(event) => setTopic(event.target.value)}/>


          <h2 className='mt-5 mb-3'>Select the difficulty Level</h2>
          <Select onValueChange={(value) => setDifficultyLevel(value)}>
              <SelectTrigger className="w-full">
                  <SelectValue placeholder="Difficulty Level"/>
              </SelectTrigger>
              <SelectContent>
                  <SelectItem value="Easy">Easy</SelectItem>
                  <SelectItem value="Moderate">Intermediate</SelectItem>
                  <SelectItem value="Hard">Hard</SelectItem>
              </SelectContent>
          </Select>

      </div>
  )
}

export default TopicInput