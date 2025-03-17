/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        indigo: {
          400: '#818cf8',
          500: '#6366f1',
          600: '#4f46e5',
          700: '#4338ca',
        }
      },
      typography: (theme) => ({
        DEFAULT: {
          css: {
            color: theme('colors.gray.300'),
            a: {
              color: theme('colors.indigo.400'),
              '&:hover': {
                color: theme('colors.indigo.300'),
              },
            },
            h1: {
              color: theme('colors.white'),
            },
            h2: {
              color: theme('colors.white'),
            },
            h3: {
              color: theme('colors.white'),
            },
            h4: {
              color: theme('colors.white'),
            },
            strong: {
              color: theme('colors.white'),
            },
            code: {
              color: theme('colors.gray.300'),
              backgroundColor: theme('colors.gray.800'),
              padding: '0.25rem',
              borderRadius: '0.25rem',
              fontWeight: '400',
            },
            pre: {
              backgroundColor: theme('colors.gray.800'),
            },
          },
        },
        invert: {
          css: {
            color: theme('colors.gray.200'),
          },
        },
      }),
    },
  },
  plugins: [
    require('@tailwindcss/typography'),
  ],
};