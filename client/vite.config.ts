import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
      '@components': path.resolve(__dirname, './src/components'),
      '@pages': path.resolve(__dirname, './src/pages'),
      '@hooks': path.resolve(__dirname, './src/hooks'),
      '@utils': path.resolve(__dirname, './src/utils'),
      '@types': path.resolve(__dirname, './src/types'),
      '@services': path.resolve(__dirname, './src/services'),
    },
  },
  server: {
    port: 5173, // Using standard Vite port 5173
    host: '127.0.0.1', // Explicit host binding for Windows compatibility
    strictPort: true,
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:5002', // Backend running on port 5002
        changeOrigin: true,
        secure: false,
        rewrite: (path) => path
      },
    },
  },
})
