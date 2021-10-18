module.exports = {
  mode: "jit",
  purge: ["./public/**/*.html", "./public/**/**.scss"],
  darkMode: false, // or 'media' or 'class'
  theme: {
    extend: {},
    fontFamily: {
      sans: ['Poppins', 'sans-serif']
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
    },
  },
  variants: {
    extend: {},
  },
  plugins: [],
};