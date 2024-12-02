import React, { useState } from 'react'
import { Box, Paper, Typography, Button, styled } from '@mui/material'
import OptionsSideBar from '../components/OptionsSideBar'
import WordInfo from '../components/WordInfo'
import VideoPlayer from '@renderer/components/VideoPlayer/VideoPlayer'
import { LinkType } from '@renderer/types/enums'
import { Quiz as QuizType, Transcript } from '../../../types/types'
import { QuizContentEvent } from '../../../types/events'
import { QuestionComponent } from '@renderer/components/QuestionComponent'

const MainLayout: React.FC = () => {
  const [isLoading, setIsLoading] = useState(false)
  const [isError, setIsError] = useState('')
  // define the quiz state object
  const [quiz, setQuiz] = useState<QuizType>({ questions: [] })

  const handleGenerateQuiz = async (): Promise<void> => {
    setIsLoading(true)
    try {
      const videoId = localStorage.getItem('videoId')
      const transcriptionData = localStorage.getItem(`transcription_${videoId}`)
      if (transcriptionData) {
        const transcriptionJson = JSON.parse(transcriptionData)
        const transcript: Transcript = new Transcript(
          transcriptionJson.text,
          transcriptionJson.segments
        )
        const newQuiz: QuizContentEvent = await window.api.generateQuiz(transcript)
        console.log(newQuiz)
        setQuiz(newQuiz)
        setTimeout(() => {
          window.scrollTo({ top: 0, behavior: 'smooth' })
        }, 100)
      }
    } catch (e) {
      if (e instanceof Error) setIsError(e.message)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="flex ">
      {/* Sidebar (Left) */}
      <div className="flex-3">
        <OptionsSideBar />
      </div>

      <div className="flex flex-col items-center justify-center flex-1 gap-2 p-5">
        <div>
          <VideoPlayer
            linkType={LinkType.YOUTUBE}
            videoStreamlink={localStorage.getItem('videoId') || ''}
          ></VideoPlayer>
        </div>
        {quiz.questions.length != 0 ? (
          <div>
            <p className="text-3xl text-orange-500">Quizzes</p>
            <div>
              {quiz.questions.map((question, key) => {
                return <QuestionComponent question={question} key={key} />
              })}
            </div>
          </div>
        ) : (
          <div className="">
            <button
              className={`px-5 py-3 bg-orange-400 rounded-md ${isLoading ? 'disabled:bg-gray-300' : ''}`}
              disabled={isLoading}
              onClick={handleGenerateQuiz}
            >
              {!isLoading ? (
                'Generate Quiz'
              ) : (
                <span className="loading loading-dots loading-md"></span>
              )}
            </button>
          </div>
        )}
      </div>
      {/* Conditionally render the button or quiz */}
      {/* {!showQuiz && (
        <SubmitButton
          variant="contained"
          sx={{
            marginTop: '20px',
            backgroundColor: '#000000',
            color: 'white',
            fontSize: '20px',
            padding: '10px 30px',
            borderRadius: '8px',
            fontWeight: 'bold',
            textTransform: 'none',
            '&:hover': {
              backgroundColor: '#00000'
            }
          }}
          onClick={handleGenerateQuiz}
        >
          Generate Quiz
        </SubmitButton>
      )}
      {showQuiz && <Quiz quiz={quiz} />} */}

      {/* Sidebar (Right) */}
      {/* <Box sx={{ width: '20%', height: '100vh', overflow: 'hidden' }}>
        <Paper elevation={3} sx={ContainerStyle}>
          <WordInfo definition="Placeholder" synonyms={['Example']} opposites={['Contrary']} />
        </Paper>
      </Box> */}

      <div className="flex-2">
        <WordInfo
        />
      </div>
    </div>
  )
}

export default MainLayout
