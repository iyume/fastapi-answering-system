// do the customization
const colors = require('tailwindcss/colors')
const plugin = require('tailwindcss/plugin')

module.exports = {
  purge: {
    enabled: false, // set to false if you are in developing
    preserveHtmlElements: true,
    content: [
      './app/templates/**',
    ],
  },
  darkMode: false, // or 'media' or 'class'
  theme: {
    fontFamily: {
      sans: [
        'Helvetica',
        'Arial',
        'Roboto',
        'system-ui',
        '-apple-system',
        'BlinkMacSystemFont',
        '"Segoe UI"',
      ],
    },
    colors: {
      white: '#ffffff',
      gray: colors.trueGray,
      yellow: colors.amber,
      indigo: colors.indigo,
      blue: colors.blue,
      red: colors.red,
    },
    extend: {
      width: {
        'normal': '1160px',
        '870': '870px',
        '280': '280px',
      },
      colors: {
        'green': colors.emerald[500],
        'main': 'orange',
        'ali': '#ff6a00',
        'darkless': '#f8f8f8',
        'darker': '#e9ebec',
        'darkest': '#000000',
        },
    },
  },
  variants: {
    extend: {},
  },
  plugins: [
    require('@tailwindcss/custom-forms'),
    plugin(function({ theme, addBase }) {
      addBase({
        'hr': {
          // 'display': 'block',
          // 'height': '1px',
          // 'border-top': '1px solid #ccc',
          // 'margin': '1em auto',
          display: theme('display.block'),
          height: theme('height.1'),
          borderWidth: theme('borderWidth.t.DEFAULT'),
          // margin: theme('margin.x.auto'),
          // margin: theme('margin.y.4'),
          'margin': '0.5em auto',
        },
      })
    }),
  ],
}
