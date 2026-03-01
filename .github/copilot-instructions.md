# Copilot Instructions for Morphstats

## Big Picture Architecture
- This is a Django monolith with multiple apps: `App`, `Stat`, `facilitators`, `events`, `dashboard`, and `api`.
- `App` is the main web entry app for most pages and facilitator CRUD/list flows (`App/urls.py`, `App/views.py`).
- `dashboard` is separate and serves aggregated analytics (`dashboard/views.py`).
- `Stat` contains core domain models (`Stat`, `Service`) and helper methods used heavily by templates/views for computed metrics (`Stat/models.py`).
- Facilitators are linked to services through `Service.facilitators_available` (ManyToMany), so facilitator activity queries usually traverse `Service -> Stat.date`.
- API endpoints live under `/api/` and are a mix of function-based and class-based DRF views (`api/views.py`).

## Data Flow and Integration Points
- UI templates are Django-rendered (mostly in `App/templates/...`) with Alpine.js enhancements loaded from `static/src/index.ts`.
- Checklist interaction flow:
  - Template initializes Alpine `checklist` state.
  - Frontend fetches active facilitators from `/api/facilitators/`.
  - Frontend fetches services via `/api/services/?stat_id=<id>`.
  - Frontend persists updates with `PUT /api/services/` and CSRF token from cookies (`static/src/ts/checklist.ts`).
- `app_base.html` always loads compiled frontend assets from `static/public/dist/bundle.{js,css}`.

## Critical Workflows
- Python setup: project expects Python 3.10+ (`pyproject.toml`).
- Backend dev server:
  - `pip install -r requirements.txt`
  - `python manage.py runserver`
- Frontend build/dev (run from `static/`):
  - `npm install` (or `pnpm install` since `pnpm-lock.yaml` exists)
  - `npm run dev` for watch mode
  - `npm run build` for one-off bundle build
- During development, run both Django server and frontend bundler (README describes a 2-server workflow).

## Project-Specific Conventions
- Staff-only pages commonly enforce access with `RedirectNonStaffMixin` (`App/mixins.py`). Reuse this instead of adding ad-hoc checks.
- Keep route namespaced (`App:...`, `events:...`, `facilitators:...`, `api:...`) and follow existing URL naming style.
- Many stats calculations are intentionally encapsulated as model methods on `Stat` (`totalAttendance`, `facilitatorsData`, etc.); prefer extending these patterns over duplicating aggregation logic in templates.
- Existing code uses both CBVs and lightweight manual `View` classes with `request.POST` parsing (example: `events/views.py`). Match the local style of the file you modify.
- Preserve current app naming and imports exactly (`App` and `Stat` are capitalized app modules).

## Config and Environment Notes
- Required env-driven settings include `DEBUG`, `SECRET_KEY`, and `ALLOWED_HOSTS` (`statsapp/settings.py`).
- DB defaults to SQLite in debug; production DB is env-configured in settings.
- Static files are served from `static/public` via `STATICFILES_DIRS`; webpack outputs to `static/public/dist`.

## When Adding Features
- For facilitator-related features, check cross-app touchpoints: `App/views.py`, `Stat/models.py`, `api/views.py`, and `static/src/ts/checklist.ts`.
- For dashboard metrics, prefer adding/adjusting helper methods and aggregations in `dashboard/views.py` + `Stat/models.py` rather than complex template logic.
- If introducing optional pluggable apps, wire through `statsapp/appsConfig.py` (`getAppNames`, `getAppUrls`).
