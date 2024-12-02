
import { defineConfig } from 'vite'
import electron from 'vite-electron-plugin'
import renderer from 'vite-plugin-electron-renderer'

export default defineConfig({
  plugins: [
    electron(),
    renderer()
  ],
  optimizeDeps: {
    exclude: ['@ffmpeg/ffmpeg', '@ffmpeg/util']
  },
  server: {
    headers: {
      'Cross-Origin-Embedder-Policy': 'require-corp',
      'Cross-Origin-Opener-Policy': 'same-origin'
    }
  }
})