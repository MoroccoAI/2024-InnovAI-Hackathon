import type { Config } from "tailwindcss";

const config: Config = {
    darkMode: ["class"],
    content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
  	extend: {
		colors: {
			
			'light-green': '#43A047', // Light green color
			'light-green-foreground': '#2D6A4F', // Darker green text for contrast
			"light-blue": "#A8DADC",
			 
			background: 'hsl(0, 0%, 98%)', // Changed to a lighter color
			foreground: 'hsl(0, 0%, 20%)', // Dark text for contrast
			card: {
				DEFAULT: 'hsl(240, 10%, 95%)', // Light card color
				foreground: 'hsl(0, 0%, 20%)',
			},
			popover: {
				DEFAULT: 'hsl(240, 10%, 95%)',
				foreground: 'hsl(0, 0%, 20%)',
			},
			primary: {
				DEFAULT: 'hsl(220, 100%, 50%)', // Brighter primary color
				foreground: 'hsl(0, 0%, 100%)',
			},
			secondary: {
				DEFAULT: 'hsl(240, 80%, 90%)', // Light secondary color
				foreground: 'hsl(0, 0%, 20%)',
			},
				muted: {
  				DEFAULT: 'hsl(var(--muted))',
  				foreground: 'hsl(var(--muted-foreground))'
  			},
  			accent: {
  				DEFAULT: 'hsl(var(--accent))',
  				foreground: 'hsl(var(--accent-foreground))'
  			},
  			destructive: {
  				DEFAULT: 'hsl(var(--destructive))',
  				foreground: 'hsl(var(--destructive-foreground))'
  			},
  			border: 'hsl(var(--border))',
  			input: 'hsl(var(--input))',
  			ring: 'hsl(var(--ring))',
  			chart: {
  				'1': 'hsl(var(--chart-1))',
  				'2': 'hsl(var(--chart-2))',
  				'3': 'hsl(var(--chart-3))',
  				'4': 'hsl(var(--chart-4))',
  				'5': 'hsl(var(--chart-5))'
  			}
			
  		},
  		borderRadius: {
  			lg: 'var(--radius)',
  			md: 'calc(var(--radius) - 2px)',
  			sm: 'calc(var(--radius) - 4px)'
  		}
  	}
  },
  plugins: [require("tailwindcss-animate"), require("tailwindcss-animate"), require("@tailwindcss/typography")],
};
export default config;
