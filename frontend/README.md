# Placement Predictor UI (Next.js)

Minimal Next.js App Router (TypeScript) frontend for the placement toy example. Triggers training and sends predictions to the FastAPI backend.

## Requirements

- Node.js and npm

## Setup

```bash
cd frontend
npm install
```

## Run

- Development: `npm run dev` (opens at http://localhost:3000)
- Build: `npm run build`
- Start: `npm start`

The UI expects the backend at `http://localhost:8000` by default. You can override with environment variable:

```
NEXT_PUBLIC_API_BASE=http://127.0.0.1:8000
```

## Notes

- Headings use the Bricolage Grotesque font via Next Fonts. Body text uses Geist.
- The page includes a basic form for `cgpa` and `iq`, a button to train on the backend, and displays returned metrics.
