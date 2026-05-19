# Wave 1 Task Breakdown

**Generated:** 2026-05-19T06:31:06Z
**Status:** Ready for Execution
**Plans:** 02 (Foundation) + 03 (Frontend UI)
**Execution Mode:** Parallel (independent task streams)

---

## Plan 02: Foundation (DevOps/Backend Track)

### Task 02.1: Git Initialization & Monorepo Setup
**Objective:** Initialize git repo and create frontend/backend directory structure
**Duration:** 15 minutes
**Acceptance Criteria:**
- [ ] `.git/` directory exists
- [ ] `frontend/` directory created with `package.json`
- [ ] `backend/` directory created with `pyproject.toml`
- [ ] `.github/workflows/` directory created
- [ ] `.gitignore` configured for Node and Python
- [ ] Initial commit: "chore(01-mvp): initialize git monorepo"

**Tasks:**
1. Initialize git repo: `git init`
2. Create directory structure:
   - `mkdir -p frontend backend .github/workflows`
3. Create `.gitignore` with Python and Node patterns
4. Create placeholder `package.json` in frontend/
5. Create placeholder `pyproject.toml` in backend/
6. Commit initial structure

---

### Task 02.2: Next.js Project Setup
**Objective:** Initialize Next.js 16 + React 19 in frontend/
**Duration:** 20 minutes
**Acceptance Criteria:**
- [ ] Next.js 16.2.6 installed (check package.json)
- [ ] React 19 installed
- [ ] TailwindCSS v3 configured
- [ ] `frontend/tsconfig.json` exists
- [ ] `frontend/app/layout.tsx` and `frontend/app/page.tsx` exist
- [ ] `npm run dev` would start the dev server (no errors in package.json scripts)

**Tasks:**
1. Create `frontend/package.json` with dependencies:
   - next@16.2.6, react@19, react-dom@19, tailwindcss@3
2. Create `frontend/tsconfig.json`
3. Create `frontend/tailwind.config.ts`
4. Create placeholder app structure: `frontend/app/{layout,page}.tsx`

---

### Task 02.3: FastAPI Backend Setup
**Objective:** Initialize FastAPI 0.104 in backend/
**Duration:** 20 minutes
**Acceptance Criteria:**
- [ ] FastAPI 0.104 in `pyproject.toml`
- [ ] Uvicorn installed
- [ ] `backend/main.py` exists with basic FastAPI app
- [ ] `backend/requirements.txt` generated from pyproject.toml
- [ ] Health check endpoint `/health` returns 200 OK (when run)

**Tasks:**
1. Create `backend/pyproject.toml` with:
   - fastapi==0.104.0
   - uvicorn[standard]
   - python-dotenv
   - anthropic (Claude SDK)
   - psycopg[binary] (PostgreSQL)
   - redis
2. Create `backend/main.py` with basic FastAPI app
3. Create `backend/.env` template with placeholder values

---

### Task 02.4: Environment Configuration
**Objective:** Create `.env.example` with all required secrets
**Duration:** 10 minutes
**Acceptance Criteria:**
- [ ] `.env.example` exists in project root
- [ ] Contains all required env vars (see below)
- [ ] Clear comments for each variable
- [ ] No actual secrets (just placeholders like `sk-...`)

**Required Env Vars:**
```
# Claude API
ANTHROPIC_API_KEY=sk-ant-xxxxx

# Database (PostgreSQL/Supabase)
DATABASE_URL=postgresql://user:password@host/db
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_KEY=xxxxx

# Cache (Redis)
REDIS_URL=redis://localhost:6379/0

# Deployment
VERCEL_ORG_ID=xxxxx
VERCEL_PROJECT_ID=xxxxx
RAILWAY_API_TOKEN=xxxxx

# Monitoring
SENTRY_DSN=https://xxxxx@xxxxx.ingest.sentry.io/xxxxx
```

**Tasks:**
1. Create `.env.example` at project root
2. Document each variable with description

---

### Task 02.5: GitHub Actions CI/CD
**Objective:** Set up automated lint, test, build pipelines
**Duration:** 30 minutes
**Acceptance Criteria:**
- [ ] `.github/workflows/frontend-ci.yml` exists
- [ ] `.github/workflows/backend-ci.yml` exists
- [ ] Frontend CI: lint (ESLint) → test (Jest) → build
- [ ] Backend CI: lint (flake8) → test (pytest) → build
- [ ] Both workflows trigger on push to main/dev
- [ ] Status badge ready for README

**Frontend CI Workflow Tasks:**
1. Checkout code
2. Set up Node 24
3. Install dependencies
4. Run `npm run lint`
5. Run `npm run test`
6. Run `npm run build`

**Backend CI Workflow Tasks:**
1. Checkout code
2. Set up Python 3.14
3. Install dependencies from pyproject.toml
4. Run flake8 lint
5. Run pytest
6. Build Docker image

---

### Task 02.6: Deployment Configuration (Vercel & Railway)
**Objective:** Configure infrastructure for deployment
**Duration:** 25 minutes
**Acceptance Criteria:**
- [ ] `vercel.json` exists with Next.js config
- [ ] `railway.toml` exists with FastAPI config
- [ ] `Dockerfile` exists for backend
- [ ] Docker image builds successfully (docker build .)
- [ ] `docker-compose.yml` for local dev with 3 services (frontend, backend, postgres)

**Vercel Config (vercel.json):**
```json
{
  "buildCommand": "npm run build",
  "installCommand": "npm ci",
  "outputDirectory": "frontend/.next"
}
```

**Railway Config (railway.toml):**
```toml
[build]
builder = "dockerfile"
dockerfile = "./Dockerfile"

[deploy]
startCommand = "uvicorn backend.main:app --host 0.0.0.0 --port $PORT"
```

**Docker & Compose:**
- Create `Dockerfile` for FastAPI
- Create `docker-compose.yml` with postgres + redis services

---

### Task 02.7: PostgreSQL Schema Setup
**Objective:** Define database schema (audit_logs, no images)
**Duration:** 20 minutes
**Acceptance Criteria:**
- [ ] Migration file created in `backend/migrations/001_audit_logs.sql`
- [ ] `audit_logs` table has: id, analysis_json (JSONB), created_at, expires_at
- [ ] `cache_keys` table has: key (varchar), value (JSONB), ttl_seconds, created_at
- [ ] Index on `expires_at` for 30-day cleanup
- [ ] Schema enforces PRIVACY-01 constraint (no image storage)

**Schema Definition:**
```sql
CREATE TABLE audit_logs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  analysis_json JSONB NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  expires_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP + INTERVAL '30 days'
);

CREATE INDEX idx_audit_logs_expires_at ON audit_logs(expires_at);

CREATE TABLE cache_keys (
  key VARCHAR(256) PRIMARY KEY,
  value JSONB NOT NULL,
  ttl_seconds INT DEFAULT 172800, -- 48 hours
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

### Task 02.8: Docker Compose Local Dev Setup
**Objective:** Enable local development with docker-compose
**Duration:** 15 minutes
**Acceptance Criteria:**
- [ ] `docker-compose.yml` exists
- [ ] Services: frontend, backend, postgres, redis
- [ ] Frontend on port 3000, backend on port 8000
- [ ] Database on 5432, Redis on 6379
- [ ] `.env.local` sourced by compose
- [ ] `docker-compose up` starts all services (or would if credentials exist)

---

## Plan 03: Frontend UI (Frontend Track)

### Task 03.1: Next.js App Structure & Layout
**Objective:** Create page layout with header, upload zone, results area
**Duration:** 20 minutes
**Acceptance Criteria:**
- [ ] `frontend/app/layout.tsx` exists with proper Meta tags
- [ ] `frontend/app/page.tsx` exists with basic structure
- [ ] `frontend/components/header.tsx` exists
- [ ] `frontend/components/upload-box.tsx` component file created
- [ ] `frontend/components/result-display.tsx` component file created
- [ ] `frontend/app/globals.css` has Tailwind imports

**Tasks:**
1. Create `frontend/app/layout.tsx` with:
   - Proper Next.js metadata
   - HTML lang attribute (for i18n)
   - Tailwind styles
2. Create `frontend/app/page.tsx` with page structure
3. Create `frontend/components/header.tsx` with nav/title
4. Create placeholder component files for upload and results
5. Create `frontend/app/globals.css` with Tailwind directives

---

### Task 03.2: Zustand Store Setup
**Objective:** Create client-side state management for UI
**Duration:** 15 minutes
**Acceptance Criteria:**
- [ ] `frontend/lib/store.ts` exists
- [ ] Store tracks: `uploadedImage` (File | null), `results` (JSON | null), `loading` (bool), `error` (string | null)
- [ ] Actions: `setImage()`, `setResults()`, `setLoading()`, `setError()`, `reset()`
- [ ] Store is properly typed with TypeScript

**Store State:**
```typescript
type AppStore = {
  uploadedImage: File | null;
  results: AnalysisResult | null;
  loading: boolean;
  error: string | null;
  setImage: (file: File | null) => void;
  setResults: (results: AnalysisResult | null) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
  reset: () => void;
};
```

---

### Task 03.3: Dark/Light Theme Support
**Objective:** Implement next-themes for theme switching
**Duration:** 15 minutes
**Acceptance Criteria:**
- [ ] `next-themes` package installed
- [ ] `frontend/lib/theme.ts` exists with theme utilities
- [ ] `frontend/components/theme-toggle.tsx` created
- [ ] Layout wraps app with ThemeProvider
- [ ] Dark mode CSS classes applied (dark: prefix in Tailwind)
- [ ] System preference detection works (initial theme detection)

**Tasks:**
1. Install `next-themes` in package.json
2. Create `frontend/lib/theme.ts` with:
   - Enum for themes (light, dark, system)
   - Utility functions to get/set theme
3. Create `frontend/components/theme-toggle.tsx` with toggle button
4. Update `frontend/app/layout.tsx` to wrap with ThemeProvider
5. Configure `frontend/tailwind.config.ts` with darkMode: 'class'

---

### Task 03.4: Internationalization (i18n) Setup
**Objective:** Configure EN/AR/CN support with RTL for Arabic
**Duration:** 20 minutes
**Acceptance Criteria:**
- [ ] `frontend/lib/i18n.ts` exists
- [ ] `frontend/public/locales/en.json` created
- [ ] `frontend/public/locales/ar.json` created with RTL direction
- [ ] `frontend/public/locales/zh.json` created
- [ ] i18n hook `useTranslation()` available in components
- [ ] Language switcher component exists

**i18n Structure:**
```json
// en.json
{
  "upload_title": "Upload Your Chart",
  "upload_description": "Drag and drop a forex chart image (PNG/JPG)"
}
```

```json
// ar.json (RTL)
{
  "upload_title": "رفع الرسم البياني الخاص بك",
  "dir": "rtl"
}
```

**Tasks:**
1. Create i18n utility in `frontend/lib/i18n.ts`
2. Create JSON locale files (en, ar, zh)
3. Create language switcher component
4. Update layout to detect user language and apply dir="rtl" for Arabic

---

### Task 03.5: Upload Box Component
**Objective:** Build drag-drop + file picker for image upload
**Duration:** 25 minutes
**Acceptance Criteria:**
- [ ] `frontend/components/upload-box.tsx` created
- [ ] Supports drag-drop (dragover, drop events)
- [ ] Supports file picker (input type="file")
- [ ] Shows upload progress (visual indicator 0-100%)
- [ ] Image validation client-side:
  - PNG or JPG only
  - Min 200x200 pixels
  - Max 5MB
- [ ] Error messages for invalid files
- [ ] State managed via Zustand store
- [ ] Responsive layout (mobile-friendly)

**Component Features:**
- Drag-drop zone with visual feedback
- File input with accept="image/png,image/jpeg"
- Preview of selected image
- Progress bar while uploading
- Error messages for:
  - Wrong file type
  - File too large (>5MB)
  - Image too small (<200x200)
  - Upload failed

---

### Task 03.6: Image Validation Utility
**Objective:** Create validation function for image checks
**Duration:** 10 minutes
**Acceptance Criteria:**
- [ ] `frontend/lib/image-validation.ts` exists
- [ ] Function `validateImage(file: File): ValidationResult` exists
- [ ] Checks: type (PNG/JPG), size (<5MB), dimensions (>200x200)
- [ ] Returns: { valid: bool, error?: string }

**Validation Logic:**
```typescript
export async function validateImage(file: File): Promise<ValidationResult> {
  // Check type
  if (!['image/png', 'image/jpeg'].includes(file.type)) {
    return { valid: false, error: 'Only PNG and JPG images allowed' };
  }
  
  // Check size
  if (file.size > 5 * 1024 * 1024) {
    return { valid: false, error: 'Image must be under 5MB' };
  }
  
  // Check dimensions
  const img = new Image();
  // ... dimension check logic
  
  return { valid: true };
}
```

---

### Task 03.7: API Integration Setup
**Objective:** Create API client for backend communication
**Duration:** 15 minutes
**Acceptance Criteria:**
- [ ] `frontend/lib/api.ts` exists
- [ ] Function `uploadChart(file: File): Promise<AnalysisResult>`
- [ ] Handles upload progress callbacks
- [ ] Error handling with user-friendly messages
- [ ] Timeout handling (>10s shows fallback message)

**API Client:**
```typescript
export async function uploadChart(
  file: File,
  onProgress?: (percent: number) => void
): Promise<AnalysisResult> {
  const formData = new FormData();
  formData.append('file', file);
  
  // XMLHttpRequest for progress tracking
  return new Promise((resolve, reject) => {
    // ... implementation
  });
}
```

---

### Task 03.8: Mobile Camera Upload
**Objective:** Enable camera capture for mobile devices
**Duration:** 10 minutes
**Acceptance Criteria:**
- [ ] File input has `accept="image/*"` for mobile camera
- [ ] On mobile, camera app opens when tapping upload box
- [ ] Fallback to gallery for older devices
- [ ] Same validation applies to camera images

**Implementation:**
- Input element with `accept="image/*"` and `capture` attribute
- Mobile browsers will offer camera option
- Desktop browsers will only show file picker

---

## Task Dependencies

### Plan 02 Task Sequence:
1. **02.1** → 02.2, 02.3 (parallel after init)
2. **02.2** → 02.5 (frontend CI needs package.json)
3. **02.3** → 02.5 (backend CI needs pyproject.toml)
4. **02.4** → Parallel to 02.2, 02.3
5. **02.5** → Parallel (CI/CD)
6. **02.6** → Parallel (deployment config)
7. **02.7** → 02.8 (schema before compose)
8. **02.8** → Parallel (local dev)

### Plan 03 Task Sequence:
1. **03.1** → 03.2, 03.3, 03.4 (parallel after layout)
2. **03.2** → 03.5 (store before components)
3. **03.3** → Parallel (theme)
4. **03.4** → Parallel (i18n)
5. **03.5** → 03.6, 03.7 (upload box, validation)
6. **03.6** → Used by 03.5
7. **03.7** → Integration in 03.5
8. **03.8** → Parallel to 03.5 (mobile capture)

## Execution Order

### Parallel Execution Timeline:

**Phase A (Start):**
- 02.1 (Git init)
- Blocks until init complete

**Phase B (Scaffolding, parallel):**
- 02.2 (Next.js setup) | 02.3 (FastAPI setup)
- 02.4 (Env config) | 03.1 (App layout)
- All run in parallel

**Phase C (Infrastructure, parallel):**
- 02.5 (CI/CD) | 02.6 (Deployment)
- 02.7 (DB schema) | 03.2 (Store)
- All run in parallel

**Phase D (Features, parallel):**
- 02.8 (Docker compose) | 03.3 (Theme)
- 03.4 (i18n) | 03.5 (Upload box)
- 03.6 (Validation) | 03.7 (API client)
- 03.8 (Mobile camera)
- All run in parallel

---

**Status:** Task breakdown complete. Ready for execution.
**Next:** Execute Phase A (Git init), then proceed with parallel phases.
