import { ipcMain } from 'electron'

const wd = require('word-definition')

const getDefinition = async (word: string): Promise<string> => {
  try {
    const definition = await new Promise<string>((resolve, reject) => {
      wd.getDef(word, 'en', null, (definition) => {
        if (definition) {
          resolve(definition)
        } else {
          reject(new Error('Definition not found'))
        }
      })
    })
    return definition
  } catch (error) {
    console.error('Failed to get definition:', error)
    throw error
  }
}

ipcMain.handle('get-definition', getDefinition)

export default {}
