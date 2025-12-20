# Deployment notes (brief)

- Backend (Flask) can be deployed to Render, Railway, or VPS.
- MySQL: production use managed DB (Amazon RDS / PlanetScale).
- Frontend: Host as static site on Vercel/Netlify/GitHub Pages.
- Set environment variables in production (OPENAI_API_KEY, DB credentials).
