import React, { useState } from 'react'
import { Paper, Typography, Box, TextField, Tabs, Tab } from '@mui/material'
import { styled } from '@mui/system'
import {
  Quiz as QuizType,
  Transcript,
  GrammarFeedback,
  FactCheckFeedback
} from '../../../types/types'
import { SubmitButton } from './styled/StyledComponents'
import { FactCheckRequestEvent, GrammarEvalRequestEvent } from '../../../types/events'

interface QuizProps {
  quiz: QuizType
}

const Quiz: React.FC<QuizProps> = ({ quiz }) => {
  const videoId = localStorage.getItem('videoId')
  const json = JSON.parse(localStorage.getItem(`transcription_${videoId}`)!)
  const transcript = new Transcript(json.text, json.segments)

  const [answers, setAnswers] = useState<string[]>(Array(quiz.questions.length).fill(''))
  const [inputValues, setInputValues] = useState<string[]>(Array(quiz.questions.length).fill(''))
  const [selectedTab, setSelectedTab] = useState<number[]>(Array(quiz.questions.length).fill(0))

  const [grammarFeedback, setGrammarFeedback] = useState<GrammarFeedback[]>(
    Array(quiz.questions.length).fill(null)
  )
  const [factCheckFeedback, setFactCheckFeedback] = useState<FactCheckFeedback[]>(
    Array(quiz.questions.length).fill(null)
  )

  const handleInputChange = (index: number, event: React.ChangeEvent<HTMLInputElement>) => {
    const updatedInputValues = [...inputValues]
    updatedInputValues[index] = event.target.value
    setInputValues(updatedInputValues)
  }

  const handleSubmit = async (index: number): Promise<void> => {
    const updatedAnswers = [...answers]
    updatedAnswers[index] = inputValues[index]
    setAnswers(updatedAnswers)

    const grammarFeedbackResponse = await window.api.evalGrammar(
      new GrammarEvalRequestEvent(inputValues[index])
    )
    setGrammarFeedback((prev) => {
      const updated = [...prev]
      updated[index] = grammarFeedbackResponse
      return updated
    })

    // Assuming you have a similar API for fact-check feedback
    const factCheckFeedbackResponse: FactCheckFeedback = await window.api.evalFactCheck(
      new FactCheckRequestEvent(transcript, quiz.questions[index].prompt, inputValues[index])
    )

    console.log(factCheckFeedbackResponse)
    setFactCheckFeedback((prev) => {
      const updated = [...prev]
      updated[index] = factCheckFeedbackResponse
      return updated
    })
  }

  const handleTabChange = (index: number, event: React.SyntheticEvent, newValue: number) => {
    const updatedSelectedTab = [...selectedTab]
    updatedSelectedTab[index] = newValue
    setSelectedTab(updatedSelectedTab)
  }

  return (
    <StyledPaper elevation={3}>
      <StyledTitle>Quiz</StyledTitle>

      {quiz.questions.map((question, index) => (
        <StyledBox key={index}>
          <StyledQuestion>{question.prompt}</StyledQuestion>
          <Box display="flex" alignItems="center">
            <TextField
              fullWidth
              variant="outlined"
              value={inputValues[index]}
              onChange={(event) => handleInputChange(index, event)}
              style={{ marginRight: '10px' }}
            />
            <SubmitButton onClick={() => handleSubmit(index)}>Submit</SubmitButton>
          </Box>
          <Tabs
            value={selectedTab[index]}
            onChange={(event, newValue) => handleTabChange(index, event, newValue)}
            indicatorColor="primary"
            textColor="primary"
          >
            <Tab label="Grammar Feedback" />
            <Tab label="Factuality Feedback" />
          </Tabs>
          {selectedTab[index] === 0 && grammarFeedback[index] && (
            <Box>
              <Typography variant="body2">Grammar Feedback:</Typography>
              <Typography variant="body2">{grammarFeedback[index].corrected_text}</Typography>
            </Box>
          )}
          {selectedTab[index] === 1 && factCheckFeedback[index] && (
            <Box>
              <Typography variant="body2">Factuality Feedback:</Typography>
              <Typography variant="body2">
                {factCheckFeedback[index].feedback.map((f) => f.explanation).join(', ')}
              </Typography>
            </Box>
          )}
        </StyledBox>
      ))}
    </StyledPaper>
  )
}

export default Quiz

// Styled components
const StyledPaper = styled(Paper)({
  width: '100%',
  maxWidth: '580px',
  padding: '20px',
  backgroundColor: '#fff',
  marginTop: '30px',
  borderRadius: '12px'
})

const StyledTitle = styled(Typography)({
  fontFamily: '"Cambria", serif',
  color: '#000',
  fontSize: '22px',
  fontWeight: 'bold',
  marginBottom: '20px',
  textAlign: 'center'
})

const StyledBox = styled(Box)({
  width: '100%',
  marginBottom: '30px'
})

const StyledQuestion = styled(Typography)({
  fontFamily: '"Cambria", serif',
  color: '#000',
  fontSize: '18px',
  marginBottom: '10px'
})
