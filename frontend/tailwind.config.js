/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: { ink: "#101828", canvas: "#f6f8fc", violet: "#6d5dfc" },
      boxShadow: { soft: "0 14px 40px rgba(16, 24, 40, 0.08)" },
    },
  },
  plugins: [],
};
