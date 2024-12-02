import React, { useEffect, useState } from 'react'
import { Box, Typography, TextField, Button, Card, CardContent, Grid, Tooltip, Grid2 } from '@mui/material'
import { styled } from '@mui/system'
import { useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'

// Brand colors and theme
const theme = {
  colors: {
    primary: '#f97316',
    secondary: '#0284c7',
    text: '#0f172a',
    lightText: '#475569',
    background: '#ffffff',
    accent: '#0ea5e9'
  }
}

const Root = styled(Box)({
  minHeight: '100vh',
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'center',
  justifyContent: 'center',
  background: `linear-gradient(135deg, ${theme.colors.primary}15 0%, ${theme.colors.secondary}15 100%)`,
  padding: '2rem 1rem',
  position: 'relative',
  overflow: 'hidden',
  '&::before': {
    content: '""',
    position: 'absolute',
    width: '100%',
    height: '100%',
    top: 0,
    left: 0,
    background: `radial-gradient(circle at 50% 0%, ${theme.colors.primary}20 0%, transparent 50%)`,
    zIndex: 0
  }
})

const ContentWrapper = styled(Box)({
  maxWidth: '1400px',
  width: '100%',
  display: 'grid',
  gridTemplateColumns: '1fr',
  gap: '2rem',
  position: 'relative',
  zIndex: 1
})

const HeroSection = styled(Box)({
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'center',
  textAlign: 'center',
  marginBottom: '2rem'
})

const Title = styled(motion.h1)({
  fontSize: 'clamp(2.5rem, 8vw, 4rem)',
  fontWeight: 900,
  background: `linear-gradient(135deg, ${theme.colors.primary}, ${theme.colors.secondary})`,
  WebkitBackgroundClip: 'text',
  WebkitTextFillColor: 'transparent',
  marginBottom: '1rem',
  fontFamily: "'Outfit', sans-serif",
  lineHeight: 1.1
})

const Subtitle = styled(Typography)({
  fontSize: 'clamp(1rem, 2vw, 1.25rem)',
  color: theme.colors.lightText,
  maxWidth: '600px',
  margin: '0 auto 3rem',
  lineHeight: 1.6,
  fontFamily: "'Outfit', sans-serif"
})

const InputSection = styled(Box)({
  width: '100%',
  maxWidth: '600px',
  background: 'rgba(255, 255, 255, 0.8)',
  backdropFilter: 'blur(20px)',
  borderRadius: '16px',
  padding: '1.5rem',
  boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)',
  margin: '2rem auto'
})

const InputFieldWrapper = styled(Box)({
  display: 'flex',
  gap: '1rem',
  alignItems: 'center',
  background: 'white',
  padding: '0.5rem',
  borderRadius: '12px',
  boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)',
  border: '2px solid transparent',
  transition: 'all 0.2s ease',
  '&:focus-within': {
    border: `2px solid ${theme.colors.accent}`,
    boxShadow: `0 0 0 3px ${theme.colors.accent}25`
  }
})

const InputField = styled(TextField)({
  flex: 1,
  '& .MuiOutlinedInput-root': {
    border: 'none',
    '& fieldset': {
      border: 'none'
    }
  },
  '& .MuiInputBase-input': {
    padding: '1rem',
    fontSize: '1rem',
    fontFamily: "'Outfit', sans-serif"
  }
})

const SubmitButton = styled(Button)({
  background: `linear-gradient(to right, ${theme.colors.primary}, ${theme.colors.secondary})`,
  color: 'white',
  padding: '1rem 2rem',
  borderRadius: '10px',
  fontFamily: "'Outfit', sans-serif",
  fontWeight: 600,
  textTransform: 'none',
  fontSize: '1rem',
  transition: 'all 0.2s ease',
  '&:hover': {
    transform: 'translateY(-2px)',
    boxShadow: '0 10px 15px -3px rgb(37 99 235 / 0.3)'
  }
})

const FeatureGrid = styled(Grid2)({
  display: 'grid',
  gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
  gap: '4rem 1.5rem',
  width: '100%',
  padding: '1rem 1rem'
})

const FeatureCard = styled(motion.div)({
  background: 'rgba(255, 255, 255, 0.8)',
  backdropFilter: 'blur(20px)',
  borderRadius: '16px',
  padding: '1.5rem',
  height: '100%',
  display: 'flex',

  flexDirection: 'column',
  gap: '1rem',
  transition: 'all 0.3s ease',
  border: '1px solid rgba(255, 255, 255, 0.2)',
  '&:hover': {
    transform: 'translateY(-5px)',
    boxShadow: '0 20px 25px -5px rgb(0 0 0 / 0.1)'
  }
})

const CardTitle = styled(Typography)({
  fontSize: '1.5rem',
  fontWeight: 'bold',
  fontFamily: "'Outfit', sans-serif",
  color: theme.colors.text,
  marginBottom: '1rem'
})

const CardContentText = styled(Typography)({
  color: theme.colors.lightText,
  fontFamily: "'Outfit', sans-serif"
})

const HomePage: React.FC = () => {
  const navigate = useNavigate()
  const [videoLink, setVideoLink] = useState('')

  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setVideoLink(event.target.value)
  }

  const handleSubmit = () => {
    const videoIdMatch = videoLink.match(
      /(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})/
    )
    if (videoIdMatch && videoIdMatch[1]) {
      const videoId = videoIdMatch[1]
      localStorage.setItem('videoId', videoId)
      navigate('/main-layout')
    } else {
      alert('Invalid video link')
    }
  }

  const handleStartNowClick = () => {
    navigate('/main-layout')
  }

  const containerVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: {
      opacity: 1,
      y: 0,
      transition: {
        staggerChildren: 0.2
      }
    }
  }

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: { opacity: 1, y: 0 }
  }

  return (
    <Root>
      <ContentWrapper>
        <HeroSection>
          <Title
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
          >
            Faseeh
          </Title>
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.2 }}
          >
            <Subtitle>Transform videos into interactive learning experiences</Subtitle>
          </motion.div>

          <InputSection>
            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
              <InputFieldWrapper>
                <InputField
                  placeholder="Paste YouTube or Vimeo URL"
                  fullWidth
                  value={videoLink}
                  onChange={handleInputChange}
                />
                <SubmitButton onClick={handleSubmit}>Generate</SubmitButton>
              </InputFieldWrapper>
              <Typography variant="caption" sx={{ color: theme.colors.lightText }}>
                Supports Only Youtube For now • No sign-up required
              </Typography>
            </Box>
          </InputSection>
        </HeroSection>

        <FeatureGrid>
          {[
            { 
              title: "Video Transcription",
              description: "AI-powered video transcription with high accuracy",
              icon: "🎥"
            },
            { title: "Quiz Generation", description: "Generate quizzes based on your video's content for interactive learning.", icon: "📝" },
            { title: "Grammar & Factuality Feedback", description: "Receive grammar and factuality feedback to enhance your learning.", icon: "🔍" },
            { title: "Dictionary Integration", description: "Easily access word meanings directly in the subtitles.", icon: "📚" },
            { title: "Video Difficulty Estimation", description: "Get a difficulty rating for each video (A1, A2, ..., C2).", icon: "📊" }
          ].map((feature, index) => (
            <motion.div
              key={index}
              variants={{
                hidden: { opacity: 0, y: 20 },
                visible: { opacity: 1, y: 0 }
              }}
              initial="hidden"
              animate="visible"
              transition={{ delay: index * 0.1 }}
            >
              <FeatureCard>
                <Box sx={{ fontSize: '2rem', mb: 2 }}>{feature.icon}</Box>
                <CardTitle variant="h6">{feature.title}</CardTitle>
                <CardContentText>{feature.description}</CardContentText>
              </FeatureCard>
            </motion.div>
          ))}
        </FeatureGrid>

        <Box sx={{ 
          display: 'flex', 
          justifyContent: 'center',
          mt: 4,
          gap: 2,
          flexWrap: 'wrap'
        }}>
          <SubmitButton onClick={handleStartNowClick}>
            Get Started Now
          </SubmitButton>
          <Button
            variant="outlined"
            sx={{
              borderColor: theme.colors.primary,
              color: theme.colors.primary,
              '&:hover': {
                borderColor: theme.colors.secondary,
                background: 'transparent'
              }
            }}
          >
            Watch Demo
          </Button>
        </Box>
      </ContentWrapper>
    </Root>
  )
}

export default HomePage
