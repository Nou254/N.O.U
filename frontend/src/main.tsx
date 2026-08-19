import React from 'react'
import ReactDOM from 'react-dom/client'
import { Provider } from 'react-redux'
import { BrowserRouter } from 'react-router-dom'
import { Toaster } from 'react-hot-toast'
import App from './App'
import ErrorBoundary from './components/ErrorBoundary'
import { store } from './store'
import { initTheme } from './services/theme'
import './index.css'

// Apply the customer's saved theme before the first paint (no flash of the
// wrong theme).
initTheme()

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <ErrorBoundary>
      <Provider store={store}>
        <BrowserRouter>
          <App />
        <Toaster 
          position="top-right"
          toastOptions={{
            duration: 4000,
            style: {
              background: '#363636',
              color: '#fff',
            },
            success: {
              duration: 3000,
              iconTheme: {
                primary: '#10b981',
                secondary: '#fff',
              },
            },
            error: {
              duration: 4000,
              iconTheme: {
                primary: '#ef4444',
                secondary: '#fff',
              },
            },
          }}
        />
        </BrowserRouter>
      </Provider>
    </ErrorBoundary>
  </React.StrictMode>,
)

// N.O.U is a Progressive Web Application: register the service worker so the
// app shell installs, works offline, and can be added to the home screen.
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/sw.js').catch((err) => {
      // Non-fatal: the site works fully without a service worker.
      console.warn('Service worker registration failed:', err)
    })
  })
}