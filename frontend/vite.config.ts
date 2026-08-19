import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [
    react(),
    {
      // Security hardening headers for the dev server responses so the UI
      // origin itself is protected (the API adds the same headers). In
      // production these belong on the hosting web server (nginx etc.).
      name: 'security-headers',
      configureServer(server) {
        server.middlewares.use((_req, res, next) => {
          res.setHeader('X-Frame-Options', 'DENY')
          res.setHeader('X-Content-Type-Options', 'nosniff')
          res.setHeader('Referrer-Policy', 'strict-origin-when-cross-origin')
          // Dev-friendly CSP (allows Vite HMR + inline React refresh preamble)
          res.setHeader(
            'Content-Security-Policy',
            "default-src 'self'; " +
              "script-src 'self' 'unsafe-inline'; " +
              "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; " +
              "font-src 'self' https://fonts.gstatic.com data:; " +
              "img-src 'self' data: blob:; " +
              "connect-src 'self' ws: wss:; " +
              "frame-ancestors 'none'"
          )
          next()
        })
      },
    },
  ],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    host: '0.0.0.0', // bind all interfaces so IPv4 (127.0.0.1) works in Chrome, not just ::1
    port: 3000,
    strictPort: true,
    // NOTE: no explicit hmr override - Vite auto-configures the HMR
    // websocket to match the server host. An explicit hmr.host caused
    // 'WebSocket handshake 400' errors in Chrome.
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
  preview: {
    host: '0.0.0.0', // same IPv4/IPv6 fix for `npm run preview` (production build)
    port: 3000,
    strictPort: true,
  },
  build: {
    outDir: 'dist',
    sourcemap: true,
  },
})