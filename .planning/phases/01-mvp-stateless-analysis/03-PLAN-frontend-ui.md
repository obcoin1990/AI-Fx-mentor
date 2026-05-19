---
wave: 1
depends_on:
  - 02-PLAN-foundation.md
files_modified:
  - frontend/app/layout.tsx
  - frontend/app/page.tsx
  - frontend/components/upload-box.tsx
  - frontend/components/result-display.tsx
  - frontend/lib/store.ts
  - frontend/lib/i18n.ts
  - frontend/lib/theme.ts
  - frontend/app/globals.css
  - frontend/tailwind.config.ts
  - frontend/public/locales/en.json
  - frontend/public/locales/ar.json
  - frontend/public/locales/zh.json
autonomous: true
---

# Plan 2: Frontend UI & Upload
**Objective:** Build Next.js frontend with upload interface, theme/i18n support, and responsive design. Create reusable components and establish state management.

## What We're Building
Next.js 16 + React 19 frontend with drag-drop upload box, dark/light theme support via next-themes, internationalization (EN/AR/CN with RTL for Arabic), responsive design for mobile/tablet/desktop. Create component foundation for results display (trend badge, zones, trade idea, mentor explanation).

## Must-Haves
1. Upload form with drag-drop support and file picker
2. Image validation (PNG/JPG, 200x200 min, 5MB max)
3. Upload progress indicator
4. Dark/light theme toggle with system detection
5. i18n support (EN, AR with RTL, CN)
6. Mobile-responsive layout
7. Zustand store for UI state (uploaded image, results, loading)
8. Camera upload for mobile (file input accept=image/*)

## Requirements Mapped
- UPLOAD-01: User can upload forex chart screenshot (PNG/JPG)
- UPLOAD-02: Image validation (200x200 min, 5MB max)
- UPLOAD-03: Reject non-image files with error
- UPLOAD-04: Upload progress displays
- UX-01: Dark and light theme support
- UX-02: i18n (EN/AR/CN with RTL)
- UX-03: Mobile-responsive (phone/tablet/desktop)
- UX-04: Mobile camera upload
- UX-05: Drag & drop upload box
- UX-06: Visual hierarchy (prepared for plan 4)

**Duration:** 4-5 days | **Team:** Frontend Engineer

---

*Plan created: 2025-05-19*
