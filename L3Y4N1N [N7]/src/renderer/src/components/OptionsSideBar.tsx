// src/components/OptionsSideBar.tsx
import React from 'react'
import { useNavigate } from 'react-router-dom'
import { Settings } from 'lucide-react'
import { Category } from '@mui/icons-material'

const OptionsSideBar: React.FC = () => {
  const navigate = useNavigate()

  const handleStartNowClick = (): void => {
    // Navigate to MainLayout
    navigate('/')
  }
  return (
    <div
      className={
        'w-auto min-h-screen px-5 flex flex-col justify-center gap-5 border-r border-zinc-100'
      }
    >
      {/* Home Button */}
      <div
        className={'p-3 bg-zinc-100 mx-auto rounded-lg hover:bg-zinc-200'}
        onClick={handleStartNowClick}
      >
        <Category className="text-orange-500" />
      </div>

      {/* Settings Button */}
      <div
        className={'p-3 bg-zinc-100 mx-auto rounded-lg hover:bg-zinc-200'}
        onClick={handleStartNowClick}
      >
        <Settings className="text-gray-400" />
      </div>
    </div>
  )
}

export default OptionsSideBar
