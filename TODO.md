# AgriCrop Refactor & Optimization - TODO

## Frontend (UI/UX + Modularization)
- [ ] Create reusable header template: `frontend/templates/header.html`
  - [ ] Centralize navbar/branding + conditional links using `session`
  - [ ] Include consistent CSS/JS imports shared across pages (or keep in per-page head if required)
- [ ] Integrate header into all pages via proper placement:
  - [ ] `frontend/templates/login.html` (header must be at the top)
  - [ ] `frontend/templates/dashboard.html`
  - [ ] `frontend/templates/profile.html`
  - [ ] `frontend/templates/output.html`
  - [ ] `frontend/templates/index.html`
  - [ ] `frontend/templates/about.html`
  - [ ] `frontend/templates/register.html`
- [ ] Improve CSS reliability and modern UI/UX:
  - [ ] Fix broken/incomplete CSS block in `frontend/static/css/style.css` (currently ends mid-section)
  - [ ] Ensure consistent spacing/typography/colors using existing CSS variables
  - [ ] Add/verify hover + focus styles for forms and buttons
  - [ ] Ensure responsive behavior across auth + main pages
- [ ] Remove unused CSS/JS references:
  - [ ] Confirm which JS files are actually used by templates (`static/js/main.js`, `static/js/output.js`)
  - [ ] Remove dead references from templates

## Backend (Reliability + Modularization)
- [ ] Add centralized utilities (without changing ML/Flask functionality):
  - [ ] Create `backend/utils/validators.py` for route input validation
  - [ ] Create `backend/utils/logging.py` or consistent logging helpers
  - [ ] Create `backend/utils/responses.py` for consistent JSON errors
- [ ] Consistent error handling:
  - [ ] Add global error handler(s) in `backend/app.py`
  - [ ] Ensure all routes log errors using the same format
- [ ] Database optimization:
  - [ ] Create a lightweight DB pooling wrapper in `backend/utils/db.py`
    - [ ] Implement per-thread cached connection or simple pool utility around `pymysql.connect`
  - [ ] Update managers to use pooled connections:
    - [ ] `backend/modules/auth_manager.py`
    - [ ] `backend/modules/feedback_manager.py`
    - [ ] `backend/modules/history_manager.py`
    - [ ] `backend/setup_db.py` / `backend/migrate_db.py` if needed
  - [ ] Verify queries remain functionally identical but more efficient/reliable
- [ ] Keep feedback/history lightweight:
  - [ ] Ensure history/feedback methods fetch only required rows and respect existing limits
  - [ ] Avoid repeated heavy processing in request paths

## Documentation
- [ ] Update `README.md` (and/or `docs/`) to reflect:
  - [ ] New structure (`backend`, `frontend`, `static`)
  - [ ] Location/name of shared header file
  - [ ] Any new utility modules added under `backend/utils`

## Testing & Verification
- [ ] Run `pytest`
- [ ] Smoke test flows:
  - [ ] Login/Register navigation
  - [ ] Dashboard → Recommendation → Output page render
  - [ ] Feedback submission
  - [ ] Profile update (including photo upload preview/upload)
  - [ ] History delete
- [ ] Validate CSS layout (desktop + responsive)
