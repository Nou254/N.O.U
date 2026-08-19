/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Brand palette (white, green, dark blue). Every value is a CSS
        // variable defined in src/index.css :root - change those variables
        // to re-theme the whole site without touching component code.
        primary: {
          50: 'rgb(var(--p-50) / <alpha-value>)',
          100: 'rgb(var(--p-100) / <alpha-value>)',
          200: 'rgb(var(--p-200) / <alpha-value>)',
          300: 'rgb(var(--p-300) / <alpha-value>)',
          400: 'rgb(var(--p-400) / <alpha-value>)',
          500: 'rgb(var(--p-500) / <alpha-value>)',
          600: 'rgb(var(--p-600) / <alpha-value>)',
          700: 'rgb(var(--p-700) / <alpha-value>)',
          800: 'rgb(var(--p-800) / <alpha-value>)',
          900: 'rgb(var(--p-900) / <alpha-value>)',
          950: 'rgb(var(--p-950) / <alpha-value>)',
        },
        accent: {
          50: 'rgb(var(--a-50) / <alpha-value>)',
          100: 'rgb(var(--a-100) / <alpha-value>)',
          200: 'rgb(var(--a-200) / <alpha-value>)',
          300: 'rgb(var(--a-300) / <alpha-value>)',
          400: 'rgb(var(--a-400) / <alpha-value>)',
          500: 'rgb(var(--a-500) / <alpha-value>)',
          600: 'rgb(var(--a-600) / <alpha-value>)',
          700: 'rgb(var(--a-700) / <alpha-value>)',
          800: 'rgb(var(--a-800) / <alpha-value>)',
          900: 'rgb(var(--a-900) / <alpha-value>)',
          950: 'rgb(var(--a-950) / <alpha-value>)',
        },
        secondary: {
          50: '#f8fafc',
          100: '#f1f5f9',
          200: '#e2e8f0',
          300: '#cbd5e1',
          400: '#94a3b8',
          500: '#64748b',
          600: '#475569',
          700: '#334155',
          800: '#1e293b',
          900: '#0f172a',
          950: '#020617',
        },
      },
      fontFamily: {
        sans: ['var(--font-sans)', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      },
      animation: {
        'fade-in': 'fadeIn 0.5s ease-in-out',
        'slide-up': 'slideUp 0.3s ease-out',
        'slide-down': 'slideDown 0.3s ease-out',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { transform: 'translateY(10px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
        slideDown: {
          '0%': { transform: 'translateY(-10px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
      },
    },
  },
  plugins: [],
}
