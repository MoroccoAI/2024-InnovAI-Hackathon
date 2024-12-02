import React from 'react'
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom'
import MainLayout from './layouts/MainLayout'
import HomeLayout from './layouts/HomeLayout'

const App: React.FC = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomeLayout />} />
        <Route path="/main-layout" element={<MainLayout />} />
      </Routes>
    </Router>
  )
}

export default App
