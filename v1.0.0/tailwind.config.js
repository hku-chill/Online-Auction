
const colors = require('tailwindcss/colors')

module.exports = {
  mode: "jit",
  purge: ["./public/**/*.html", "./public/**/**.scss"],
  darkMode: false, // or 'media' or 'class'
  theme: {
    extend: {
      outline: {
        main_mavi: '2px solid theme("colors.mavi")',
      },
      colors: {
        beyaz: {
          0: "#FAFAFA",
          5: "#F0F0F0",
          10: "#DCDCDC",
          15: "#C8C8C8",
          20: "#B4B4B4",
          25: "#A0A0A0",
          30: "#8C8C8C",
          35: "#787878",
        },
        siyah: {
          0: "#191919",
          5: "#5A5A5A",
          10: "#464646",
          15: "#323232",
          20: "#282828",
          25: "#1e1e1e",
          30: "#0a0a0a",
        },
        mavi: "#2EC4B6",
        mavi_5: "#59ADFF",
        mor: "#9B5DE5",
        sari: "#FFC107",
        turuncu: "#F69313"
      },
    },
    fontFamily: {
      sans: ['Poppins', 'sans-serif']
    },
  },
  variants: {
    extend: {
      outline: ['hover', 'active'],
    },
  },
  plugins: [
    require("@tailwindcss/forms")({
      strategy: 'class',
    }),
  ],
};
