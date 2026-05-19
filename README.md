# AI Chart Mentor - MVP Phase 1

AI-powered forex chart analysis platform with instant, structured analysis and mentor-style guidance.

## Overview

Traders upload a forex chart screenshot and receive instant analysis including:
- **Trend Direction**: Bullish, bearish, or consolidating
- **Support & Resistance Zones**: With price levels and touch counts
- **Trade Scenarios**: 1-2 potential setups with entry, stop-loss, take-profit, and risk-reward
- **Mentor Explanation**: Educational analysis in plain English
- **Confidence Score**: Capped at 65% to prevent false confidence

## Project Structure

```
ai-chart-mentor/
├── frontend/              # Next.js 16 + React 19 frontend
│   ├── app/              # Next.js app router pages
│   ├── components/       # Reusable React components
│   ├── lib/             # Utilities (API client, validation, theme)
│   ├── public/          # Static assets and localization files
│   ├── package.json
│   ├── tailwind.config.ts
│   └── tsconfig.json
│
├── backend/             # FastAPI Python backend
│   ├── routes/          # API endpoints
│   ├── services/        # Business logic (vision, reasoning)
│   ├── schemas/         # Pydantic request/response models
│   ├── utils/           # Helper utilities (prompts, validation)
│   ├── tests/           # Test suite
│   ├── migrations/      # PostgreSQL migrations
│   ├── main.py          # FastAPI application
│   └── pyproject.toml
│
├── .github/workflows/   # CI/CD pipelines
│   ├── frontend-ci.yml
│   └── backend-ci.yml
│
├── docker-compose.yml   # Local development with postgres, redis
├── Dockerfile           # Backend container
├── .env.example        # Environment template
├── vercel.json         # Vercel deployment config
├── railway.toml        # Railway deployment config
└── README.md           # This file
```

## Quick Start

### Prerequisites
- Node.js 24+ and npm
- Python 3.11+
- Docker and Docker Compose (for local dev)
- Git

### Local Development

1. **Clone and setup:**
   ```bash
   git clone <repo>
   cd ai-chart-mentor
   cp .env.example .env
   # Edit .env with your API keys
   ```

2. **Start services (Docker Compose):**
   ```bash
   docker-compose up
   ```
   - Frontend: http://localhost:3000
   - Backend: http://localhost:8000
   - Backend docs: http://localhost:8000/docs
   - PostgreSQL: localhost:5432
   - Redis: localhost:6379

3. **Or run separately:**

   **Frontend:**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

   **Backend:**
   ```bash
   cd backend
   pip install -e .
   uvicorn main:app --reload
   ```

## Features (Phase 1 MVP)

### ✅ Upload & Processing
- Drag-drop or click to upload forex charts (PNG/JPG)
- Image validation (200x200 min, 5MB max)
- Mobile camera capture support
- Upload progress indicator

### ✅ Vision Analysis
- Claude 3.5 Sonnet vision model extracts:
  - Trend direction (bullish/bearish/consolidating)
  - Swing highs and lows
  - Support zones (with touch counts)
  - Resistance zones (with touch counts)
  - Chart patterns (double tops, channels, triangles, etc.)

### ✅ Reasoning & Scenarios
- Generate 1-2 trade scenarios from vision analysis
- Calculate risk-reward ratios
- Assign confidence scores (capped at 65%)
- Mentor-style explanations (3-5 sentences)

### ✅ Display & UX
- Responsive design (mobile, tablet, desktop)
- Dark/light theme with system detection
- Internationalization (EN/AR/CN with RTL for Arabic)
- Clear visual hierarchy
- Prominent legal disclaimers

### ✅ Performance
- Response time <5 seconds for typical charts
- Cache by image hash (48-hour TTL)
- Cached requests <500ms
- Claude API timeout handling

### ✅ Privacy & Quality
- **NO chart image storage** (PRIVACY-01)
- Store **only** analysis JSON output (PRIVACY-02)
- Auto-delete analyses after 30 days (PRIVACY-04)
- No user tracking or cookies (PRIVACY-03)
- Confidence capped at 65% (QUALITY-02)
- No hallucinated prices (QUALITY-03)
- Legal disclaimers prominent (QUALITY-01)

## Tech Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| **Frontend** | Next.js + React | 16.2.6 + 19 |
| **Styling** | TailwindCSS | 3.4.0 |
| **State** | Zustand | 5.0.0 |
| **i18n** | next-i18n-routing | latest |
| **Theme** | next-themes | latest |
| **Backend** | FastAPI | 0.104.0 |
| **Server** | Uvicorn | latest |
| **AI Vision** | Claude 3.5 Sonnet | 4.6 |
| **AI Reasoning** | Claude 3.5 Sonnet | 4.6 |
| **Database** | PostgreSQL | 15+ |
| **Cache** | Redis | 7.0+ |
| **Deploy Frontend** | Vercel | - |
| **Deploy Backend** | Railway | - |

## API Endpoints

### Health Check
- `GET /health` - Server health status

### Analysis
- `POST /api/analyze-chart` - Upload chart and get analysis
  - Request: multipart/form-data with image file
  - Response: Analysis result with trend, zones, scenarios

### Documentation
- `GET /docs` - Interactive API docs (Swagger UI)
- `GET /redoc` - ReDoc documentation

## Environment Variables

See `.env.example` for required configuration:

```
ANTHROPIC_API_KEY=sk-ant-...
DATABASE_URL=postgresql://...
REDIS_URL=redis://...
BACKEND_CORS_ORIGINS=http://localhost:3000
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Deployment

### Frontend (Vercel)
```bash
vercel deploy
```

### Backend (Railway)
```bash
railway up --service backend
```

## Testing

### Run tests:
```bash
cd backend
pytest tests/ -v
```

### Consistency testing (same chart → same output):
```bash
pytest tests/test_consistency.py -v
```

### Load testing:
```bash
pytest tests/test_performance.py -v
```

## Non-Negotiables

1. **Privacy First** - Charts are never stored, only JSON analysis outputs
2. **Honest Disclaimers** - All prominent, educational analysis only
3. **No Hallucinations** - All extracted prices validated against chart data
4. **Confidence Caps** - Maximum 65% to prevent false confidence
5. **Stateless MVP** - No user accounts or persistent profiles in Phase 1
6. **Forex Only** - Phase 1 focuses on forex pairs only
7. **No Automated Trading** - Analysis only, user makes trading decisions

## Known Limitations

- **Forex-only**: Phase 1 covers forex pairs only (EUR/USD, GBP/USD, etc.)
- **No user accounts**: Phase 1 is stateless, no saved history
- **Confidence cap**: 65% maximum (conservative)
- **Single timeframe**: Analyze individual charts (multi-timeframe in Phase 2)

## Phase 2 Roadmap

- User accounts (Supabase Auth)
- Analysis history and search
- Feedback loop (accuracy tracking)
- Multi-timeframe consensus analysis
- Extended assets (crypto, indices)
- A/B testing (Claude vs GPT-4o)

## Contributing

See `CONTRIBUTING.md` for guidelines on:
- Code style and conventions
- Git workflow
- Testing requirements
- Commit message format

## License

MIT License - See LICENSE file

## Support & Feedback

For bugs, feature requests, or feedback:
1. Check existing issues
2. Create a new issue with:
   - Description of problem/request
   - Steps to reproduce (for bugs)
   - Expected vs actual behavior
3. Include relevant logs or screenshots

---

**Status**: MVP Phase 1 - In Active Development
**Started**: 2025-05-19
**Target Launch**: 2025-06-30
