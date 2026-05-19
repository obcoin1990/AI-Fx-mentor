# Contributing to AI Chart Mentor

Thank you for contributing! This guide helps ensure consistent, high-quality contributions.

## Code of Conduct

- Be respectful and professional
- Provide constructive feedback
- Focus on ideas, not people
- Help others learn and grow

## Getting Started

### Setup Development Environment

```bash
# Clone repo
git clone <repo>
cd ai-chart-mentor

# Setup frontend
cd frontend
npm install
npm run dev  # http://localhost:3000

# Setup backend (in another terminal)
cd backend
pip install -e ".[dev]"
uvicorn main:app --reload  # http://localhost:8000
```

### Or use Docker Compose

```bash
docker-compose up
```

## Git Workflow

### Branch Naming

```
feature/short-description
fix/short-description
docs/short-description
test/short-description
```

### Commits

Follow conventional commits:

```
feat(component): add new feature
fix(component): fix bug
docs(section): update documentation
test(component): add tests
refactor(component): improve code quality
chore: update dependencies
```

Example:
```
git commit -m "feat(upload-box): add drag-drop support for mobile"
```

### Pull Requests

1. Create feature branch: `git checkout -b feature/my-feature`
2. Make changes and commit atomically
3. Push to origin: `git push origin feature/my-feature`
4. Create PR with:
   - Clear description of changes
   - Reference to related issues
   - Screenshots/demos if UI changes
   - Test results

## Frontend Development

### Project Structure

```
frontend/
├── app/              # Pages and layout
├── components/       # Reusable components
├── lib/             # Utilities
├── public/          # Static assets
└── tests/           # Component tests
```

### Code Style

- Use TypeScript strictly
- Follow ESLint rules
- Format with Prettier (auto via npm scripts)
- 80-character line length

### Component Guidelines

```typescript
// Use functional components with hooks
export default function MyComponent() {
  const [state, setState] = useState()
  
  return (
    <div className="...">
      {/* JSX */}
    </div>
  )
}
```

### Styling

- Use TailwindCSS utility classes
- Dark mode: `dark:` prefix
- RTL support: HTML dir="rtl" attribute
- Responsive: `md:`, `lg:` breakpoints

### Testing

```bash
npm test  # Run Jest tests
npm run lint  # Run ESLint
```

## Backend Development

### Project Structure

```
backend/
├── routes/      # API endpoints
├── services/    # Business logic
├── schemas/     # Pydantic models
├── utils/       # Helpers
└── tests/       # Tests
```

### Code Style

- Follow PEP 8
- Type hints required
- Docstrings for functions
- Format with black, lint with flake8

```bash
black .
flake8 . --max-line-length=100
```

### API Endpoints

New endpoints in `routes/` with:
- Clear docstrings
- Input validation (Pydantic schemas)
- Error handling
- Logging

Example:
```python
@router.post("/api/analyze-chart")
async def analyze_chart(file: UploadFile) -> AnalysisResponse:
    """Analyze uploaded forex chart."""
    # Implementation
    return result
```

### Testing

```bash
pytest tests/ -v  # Run all tests
pytest tests/test_vision.py -v  # Run specific test
pytest tests/ -v --cov  # With coverage
```

## Non-Negotiables

These rules are enforced:

1. **Privacy First**: No chart images stored, only JSON analysis
2. **Honest Disclaimers**: Educational analysis, not financial advice
3. **No Hallucinations**: Validate all prices against chart data
4. **Confidence Caps**: Max 65% confidence in code
5. **Stateless MVP**: No user persistence in Phase 1
6. **Forex Only**: No crypto/stocks in Phase 1
7. **No Automated Trading**: Analysis only, user decides

Violations will be caught in PR review and CI/CD.

## Review Checklist

Before submitting PR, ensure:

- [ ] Code follows style guidelines
- [ ] Tests added for new features
- [ ] All tests pass locally
- [ ] No console errors/warnings
- [ ] Non-negotiables enforced
- [ ] Commit messages follow conventional format
- [ ] Documentation updated if needed

## Testing Requirements

### Frontend
- Unit tests for components
- Integration tests for user flows
- No console errors in dev tools

### Backend
- Unit tests for services
- Integration tests for endpoints
- No deprecation warnings

## Documentation

Update docs when:
- Adding new features
- Changing APIs
- Fixing non-obvious bugs
- Updating dependencies

## Questions?

- Check existing issues/PRs
- Open a discussion thread
- Tag maintainers in PRs

---

**Thank you for contributing to AI Chart Mentor!**
