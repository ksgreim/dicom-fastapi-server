import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      // This redirects any call to /api over to your actual backend
      '/api': {
        target: 'http://localhost:8000', // Change this to your backend port
        changeOrigin: true,
      },
      '/idc': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        // rewrite: (path) => path.replace(/^\/idc/, '/idc') // Ensure it doesn't strip the prefix
      },
    },
  },
})