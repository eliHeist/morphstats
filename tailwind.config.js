/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["templates/**/*.html", "**/templates/**/*.html"],
  theme: {
    extend: {
      colors: {
        'primary': '#006FFF',
        'dark': '#030E19',
        'light': '#1A2B3D',
        'lighter': '#C0D6F2',
        'warning': '#FFB300',
        'red': '#ff003c',
      },
    },
  },
  plugins: [],
}

