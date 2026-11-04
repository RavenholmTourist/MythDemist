import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.tsx'
import { PortraitsProvider } from './lib/portraits.tsx'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <PortraitsProvider>
      <App />
    </PortraitsProvider>
  </StrictMode>,
)

if ('serviceWorker' in navigator && import.meta.env.PROD) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register(`${import.meta.env.BASE_URL}sw.js`).catch(() => {})
  })
}
