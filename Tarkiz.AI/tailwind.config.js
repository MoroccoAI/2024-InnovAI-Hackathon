/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        neon: {
          green: '#00ff9d',
          blue: '#00f0ff',
          purple: '#b400ff',
          pink: '#ff00f7',
          
        },
      },
      boxShadow: {
        'neon': '0 0 10px rgba(0, 255, 157, 0.3)',
        'neon-hover': '0 0 20px rgba(0, 255, 157, 0.5)',
      },
      filter: {
        'drop-shadow-neon': 'drop-shadow(0 0 10px rgba(155, 77, 255, 0.5))', // More purple drop-shadow neon
      },
    },
    
  },
  plugins: [],
}
