/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        f1: {
          red: '#FF1801',
          dark: '#15151E',
          gray: '#38383F',
          light: '#F7F4F4',
        }
      },
      fontFamily: {
        'f1': ['Formula1', 'Arial', 'sans-serif'],
      }
    },
  },
  plugins: [],
}
