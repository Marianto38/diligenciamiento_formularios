import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': 'http://localhost:5050',
    },
  },
  build: {
    // Vercel compila con root en frontend/ y necesita el output dentro de esa carpeta (dist).
    // Para el deploy en Render (Flask sirviendo public/) se sigue generando ../public localmente.
    outDir: process.env.VERCEL ? 'dist' : '../public',
    emptyOutDir: true,
  },
})
