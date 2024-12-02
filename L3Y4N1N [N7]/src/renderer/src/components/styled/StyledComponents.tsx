// StyledComponents.tsx
import { Box, Typography, TextField, Button, Card } from '@mui/material'
import { styled } from '@mui/system'

export const Root = styled(Box)({
  backgroundColor: '#ffffff',
  minHeight: '100vh',
  display: 'flex',
  flexDirection: 'column',
  justifyContent: 'center',
  alignItems: 'center',
  textAlign: 'center',
  padding: '2rem'
})

export const Title = styled(Typography)({
  fontSize: '4rem',
  fontWeight: 'bold',
  color: '#333333',
  fontFamily: '"Cambria", serif', // Cambria font family
  fontStyle: 'italic' // Italic text
})

export const Subtitle = styled(Typography)({
  fontSize: '1rem',
  color: '#666666',
  fontFamily: '"Cambria", serif', // Cambria font family
  fontStyle: 'italic', // Italic text
  marginBottom: '2rem'
})

export const InputFieldWrapper = styled(Box)({
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center', // Center content horizontally
  marginBottom: '2rem', // Larger margin for better spacing
  borderRadius: '8px',
  width: '100%',
  maxWidth: '500px' // Limit width for aesthetic purposes
})

export const InputField = styled(TextField)({
  flex: 1,
  '& .MuiOutlinedInput-root': {
    borderRadius: '8px', // Same border radius for the input
    '&:hover fieldset': {
      borderColor: '#000000' // Border color on hover
    },
    '&.Mui-focused fieldset': {
      borderColor: '#000000' // Focused border color
    }
  },
  '& .MuiInputLabel-root': {
    color: '#333333' // Label color
  },
  '& .MuiInputBase-input': {
    padding: '10px' // Ensure input text is properly spaced
  }
})

export const SubmitButton = styled(Button)({
  backgroundColor: '#000000',
  color: '#fff',
  padding: '8.9px 25px',
  fontFamily: '"Cambria", serif', // Cambria font family
  borderRadius: '8px', // Consistent radius with input
  '&:hover': {
    backgroundColor: '#333333' // Darker color on hover
  },
  marginLeft: '10px', // Space between input and button
  transition: 'all 0.3s ease' // Smooth transition
})

export const FeatureCard = styled(Card)({
  backgroundColor: '#000000',
  height: '200px',
  width: '250px',
  color: '#ffffff',
  borderRadius: '50%',
  padding: '1.5rem',
  textAlign: 'center',
  boxShadow: '0 4px 8px rgba(0, 0, 0, 0.2)',
  transition: 'transform 0.3s ease-in-out',
  display: 'flex',
  flexDirection: 'column', // Ensure the content stacks vertically
  justifyContent: 'center', // Vertically center the content
  alignItems: 'center', // Horizontally center the content
  '&:hover': {
    transform: 'scale(1.05)'
  }
})

export const CardTitle = styled(Typography)({
  fontSize: '1.5rem',
  fontWeight: 'bold',
  fontFamily: '"Cambria", serif', // Cambria font family
  color: '#ffffff',
  marginBottom: '1rem'
})

export const CardContentText = styled(Typography)({
  color: '#dddddd',
  fontFamily: '"Cambria", serif' // Cambria font family
})
