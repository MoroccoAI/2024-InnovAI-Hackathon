import { contextBridge, ipcRenderer } from 'electron'
import { electronAPI } from '@electron-toolkit/preload'
import { Transcript } from '../types/types'
import {
  FactCheckRequestEvent,
  FactCheckResponseEvent,
  GrammarEvalRequestEvent,
  GrammarEvalResponseEvent,
  QuizRequestEvent,
  QuizResponseEvent
} from '../types/events'



// Custom APIs for renderer
const api = {
 

  evalGrammar: async (
    grammarEvalRequest: GrammarEvalRequestEvent
  ): Promise<GrammarEvalResponseEvent> => {
    return await ipcRenderer.invoke(GrammarEvalRequestEvent.event, grammarEvalRequest.userResponse)
  },

  generateQuiz: async (transcript: Transcript): Promise<QuizResponseEvent> => {
    return await ipcRenderer.invoke(QuizRequestEvent.event, transcript)
  },

  evalFactCheck: async (
    factCheckRequest: FactCheckRequestEvent
  ): Promise<FactCheckResponseEvent> => {
    return await ipcRenderer.invoke(FactCheckRequestEvent.event, factCheckRequest)
  }
}

window.addEventListener('DOMContentLoaded', () => {
  console.log('Preload script loaded')
}) /*  */

// Use `contextBridge` APIs to expose Electron APIs to
// renderer only if context isolation is enabled, otherwise
// just add to the DOM global.
if (process.contextIsolated) {
  try {
    contextBridge.exposeInMainWorld('electron', electronAPI)
    contextBridge.exposeInMainWorld('api', api)
    contextBridge.exposeInMainWorld('electronAPI', {
      getQuizzes: (transcript: string) => ipcRenderer.invoke('get-quizzes', transcript)
    })
  } catch (error) {
    console.error(error)
  }
} else {
  // @ts-ignore (define in dts)
  window.electron = electronAPI
  // @ts-ignore (define in dts)
  window.api = api
}
