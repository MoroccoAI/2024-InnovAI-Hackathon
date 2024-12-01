/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./App.{js,jsx,ts,tsx}", 
    "./screens/**/*.{js,jsx,ts,tsx}",
    "./components/**/*.{js,jsx,ts,tsx}"
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#7EA497', // Couleur principale par défaut
        },
        secondary: {
          DEFAULT: '#E3EFEC',
        },
      },
    },
  },
  plugins: [],
};