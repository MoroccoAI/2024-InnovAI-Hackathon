// src/components/WordInfo.tsx
import React, { Key } from 'react'
import { Box, Typography, Divider, Paper } from '@mui/material'
import { Book } from 'lucide-react'
import { useState, useEffect } from 'react'
import getSynAnt from '@renderer/services/GetSynAnt'


const WordInfo: React.FC = () => {
  const [selectedWord, setSelectedWord] = useState<string>('')
  const [id, setId] = useState<string | null>(localStorage.getItem('videoId'))
  const [def, setDef] = useState<string>('')
  const [synonyms, setSynonyms] = useState<string[]>([])
  const [opposites, setOpposites] = useState<string[]>([])
  const [usage, setUsage] = useState<string>('')
  if (!id) {
    return null
  }

  const handleSelectionChange = () => {
    const selection = window.getSelection()
    if (selection && selection.rangeCount > 0) {
      const selectedText = selection.toString().split(' ')[0]
      setSelectedWord(selectedText)
    }
  }
  useEffect(() => {
    document.addEventListener('selectionchange', handleSelectionChange)

    return () => {
      document.removeEventListener('selectionchange', handleSelectionChange)
    }
  }, [])

  useEffect(() => {
    if (selectedWord) {
      
      getSynAnt(selectedWord).then((res) => {
        setSynonyms(res.antonyms)
        setOpposites(res.antonyms)
        setUsage(res.usage)
        setDef(selectedWord+" : "+res.definition)
})
    }
  }, [selectedWord])
  

  return (
    <div className="flex flex-col items-start justify-center w-auto min-h-screen gap-5 border-l border-zinc-100">
      <div className="w-full">
        <p className="flex items-center w-full gap-2 px-5 py-3 text-2xl font-bold text-white bg-orange-400">
          {' '}
          <Book />
          Dictionnary
        </p>
      </div>
      <div className="flex flex-col gap-5 pl-2 pr-8">
        <div className="flex flex-col gap-2">
          <p className="text-xl font-bold">Definition</p>
          <p className="text-md">{def}</p>
        </div>
        <div className="flex flex-col gap-2">
          <p className="text-xl font-bold">Synonymes</p>
          <div className="flex flex-wrap gap-2">
            {synonyms?.length > 0 ? (
              synonyms.map((synonym: string, key: Key) => {
                return (
                  <p className="text-md" key={key}>
                    #{synonym}
                  </p>
                )
              })
            ) : (
              <div>No synonyms available</div>
            )}
          </div>
        </div>
        <div className="flex flex-col gap-2">
          <p className="text-xl font-bold">Opposites</p>
          <div className="flex flex-wrap gap-2">
            {opposites?.length > 0 ? (
              opposites.map((opposite: string, key: Key) => {
                return (
                  <p className="text-md" key={key}>
                    #{opposite}
                  </p>
                )
              })
            ) : (
              <div>No opposites available</div>
            )}
          </div>
          <div className="flex flex-col gap-2">
            <p className="text-xl font-bold">Usage</p>
            <p className="text-md">{usage}</p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default WordInfo
