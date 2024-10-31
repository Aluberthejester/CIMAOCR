/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './ocr/templates/**/*.html',  // Escanea todas las plantillas HTML de ocr
    './**/*.py',                  // Escanea archivos Python si es necesario
    './node_modules/flowbite/**/*.js',  // Incluye los archivos de Flowbite
  ],
  theme: {
    extend: {},
  },
  plugins: [
    require('flowbite/plugin',)  // Incluye Flowbite como plugin
  ],
};
