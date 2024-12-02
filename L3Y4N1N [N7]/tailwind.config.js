/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./index.html', './src/renderer/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {}
  },
  plugins: [require('daisyui')]
}
