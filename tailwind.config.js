const colors = require('tailwindcss/colors');

module.exports = {
    darkMode: 'class',
    content: [
        './templates/**/*.html',
        './static_src/**/*.{js,ts}',
    ],
    theme: {
        screens: {
            sm: '412px',
            md: '768px',
            lg: '1024px',
            xl: '1280px',
        },
        colors: {
            ...colors,
            white: '#FFFFFF',
            black: '#000000',
            cx: {
                ink: '#05070d',
                navy: '#08111f',
                panel: '#0d1829',
                cyan: '#28d7ff',
                blue: '#4184ff',
                text: '#edf7ff',
                muted: '#8ea7bc',
            },
            mackerel: {
                100: '#7777774D',
                200: '#96D7E5',
                300: '#26899E',
                400: '#1A2A2E',
            },
            grey: {
                100: '#EFEFEF',
                200: '#E6E6E6',
                300: '#CCCCCC',
                400: '#B3B3B3',
                500: '#999999',
                600: '#808080',
                700: '#4D4D4D',
                800: '#3A3A3A',
                900: '#1E1E1E',
            },
            inherit: 'inherit',
            current: 'currentColor',
            transparent: 'transparent',
        },
        fontFamily: {
            sans3: ["Inter", "sans-serif"],
            serif4: ["Inter", "sans-serif"],
            codepro: ["IBM Plex Mono", "monospace"],
        },
        extend: {},
    },
};
