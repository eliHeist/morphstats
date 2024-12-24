module.exports = {
    content: ['../templates/*.html', '../**/templates/**/*.html'],
    darkMode: 'media', // or 'class'
    theme: {
        extend: {
            colors: {
                'primary': '#006FFF',
                'dark': '#030E19',
                'light': '#1a2b3d',
                'lighter': '#C0D6F2',
                'warning': '#FFB300',
                'danger': '#ff003c',
                'success': '#00C853',
                grey: {
                    50: 'rgb(252, 252, 252)',
                    100: 'rgb(245, 245, 245)',
                    200: 'rgb(234, 234, 234)',
                    300: 'rgb(219, 219, 219)',
                    400: 'rgb(175, 175, 175)',
                    500: 'rgb(130, 130, 130)',
                    600: 'rgb(97, 97, 97)',
                    700: 'rgb(69, 69, 69)',
                    800: 'rgb(42, 42, 42)',
                    900: 'rgb(28, 28, 28)'
                }
            },
            fontFamily: {
                nunito: ['Nunito Sans', 'sans-serif']
            },
        },
    },
    variants: {
      extend: {},
    },
    plugins: [
        require('@tailwindcss/container-queries'),
    ],
  };
  