export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      animation: {
        breath: 'breath 4s ease-in-out infinite',
      },
      keyframes: {
        breath: {
          '0%, 100%': { transform: 'scale(1)', opacity: '0.6' },
          '50%': { transform: 'scale(1.3)', opacity: '1' },
        },
      },
    },
  },
  plugins: [],
}
