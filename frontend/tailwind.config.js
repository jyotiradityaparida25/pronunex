/** @type {import('tailwindcss').Config} */
export default {
 content: [
  "./index.html",
  "./src/App.jsx",
  "./src/main.jsx",
  "./src/pages/**/*.{js,ts,jsx,tsx}",      // Scans everything in pages
  "./src/components/**/*.{js,ts,jsx,tsx}", // Scans everything in components
],
  theme: {
    extend: {
      colors: {
        primary: "#10b981", // Emerald Green
        secondary: "#34d399",
        dark: "#0f172a",
      },
      animation: {
        'blob': 'blob 7s infinite',
      },
      keyframes: {
        blob: {
          '0%': { transform: 'translate(0px, 0px) scale(1)' },
          '33%': { transform: 'translate(30px, -50px) scale(1.1)' },
          '66%': { transform: 'translate(-20px, 20px) scale(0.9)' },
          '100%': { transform: 'translate(0px, 0px) scale(1)' },
        }
      }
    },
  },
  plugins: [],
}