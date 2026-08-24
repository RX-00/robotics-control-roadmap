import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  base: '/robotics-control-roadmap/',
  plugins: [react()],
})
