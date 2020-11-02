module.exports = {
  future: {
     removeDeprecatedGapUtilities: true,
     purgeLayersByDefault: true,
  },
  purge: {
    enabled: process.env.NODE_ENV === "production",
    content: ['../fm/templates/**/*.html'],
  },
  theme: {
    extend: {},
  },
  variants: {
    backgroundColor: ['responsive', 'dark', 'hover'],
    textColor: ['responsive', 'dark', 'hover'],
    visibility: ['responsive', 'hover', 'group-hover'],
    display: ['responsive', 'hover'],
  },
  plugins: [
    require('tailwindcss-dark-mode')()
  ],
}
