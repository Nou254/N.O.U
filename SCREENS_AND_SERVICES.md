# N.O.U Digital Systems — Screens, Portals & Services

**Website:** nou.com · **Document status:** Current (2026-08-08)
**Frontend:** React 18 + Vite + Redux Toolkit (PWA) · **Backend:** FastAPI + SQLAlchemy (aiomysql) + MySQL 8 · **AI:** Groq key pool

This document inventories every screen and portal in the web application and every
backend service, router, and endpoint behind them. Use it as the map of the platform.

---

# 1. Portal Map (access control)

```
                        PUBLIC SITE (no login)
      Home · Products · Careers · Investors · Support · Login · Register
                  Forgot Password · Terms · Privacy
                              │
          ┌───────────────────┼───────────────────────┐
          ▼                   ▼                       ▼
   CUSTOMER PORTAL     APPLICANT PORTAL         INVESTOR PORTAL
   /customer/*          /applicant/*              /investor/*
   (role: customer)     (role: applicant)         (role: investor, read-only)
          │                                       ▲
          │                          ┌────────────┘
          ▼                          ▼
   ADMIN PORTAL               DEVELOPER PORTAL
   /admin/*                  /portal/*
   (role: admin)             (role: developer)
```

Every authenticated role first passes the **terms-of-use gate** (`/terms-accept`)
on first login, and can change their password at `/change-password`.

| Role | Home route | Can access |
| --- | --- | --- |
| visitor | `/` | Public pages only |
| customer | `/customer` | Customer portal |
| applicant | `/applicant` | Applicant portal (assessment) |
| developer | `/portal` | Developer projects portal |
| investor | `/investor` | Investor read-only project progress |
| admin | `/admin` | Admin portal (everything) |

---

# 2. Public Site Screens

| Route | Screen | Purpose |
| --- | --- | --- |
| `/` | Home | Landing page per today.md Ch.5: **hero with your `banner.png`** + "BUILDING DIGITAL SOLUTIONS" value proposition, catalogue categories, featured + new-release product rails, services (incl. WiFi/CCTV/consultancy), custom-solution CTA, careers + investor call-outs, N.O.U Lite chat widget |
| `/products` | Products | Public catalogue of N.O.U software products — **filter bar** (search, category, product status, platform, featured) + cards with status/platform/featured badges, product details, downloads |
| `/careers` | Careers | Open positions — **apply with names + email only (no account)**; choose your **place of qualification** (category → that is where you are assessed); results are emailed |
| `/request-project` | Request a project | **Guest (no account)** custom-solution request: name/email/phone, **service type** (Software Development / WiFi Installation / CCTV Installation / IT Consultancy), optional location, budget, description → lands in Admin → Customer Requests |
| `/investors` | Investors | Investor-interest application form: name, email, phone, country, organization, investment range, **monthly investment amount**, **expectations while joining**, **knowledge of business risks**, message. **No joining fee** - details are reviewed and the team contacts the investor directly |
| `/login` | Login | Email/password sign-in; development shows the OTP code on screen |
| `/register` | Register | Account creation (visitor → customer / applicant); terms checkbox required |
| `/forgot-password` | Forgot password | Request a password-reset OTP |
| `/terms` | Terms & Conditions | Full terms (mirrors `policies.md` — 9 sections; **investor agreements removed**) |
| `/privacy` | Privacy Policy | Privacy policy (Kenya Data Protection Act, 2019) |
| `/support` | Support | Public support/contribution page: **make a donation via M-Pesa (STK) or card (Flutterwave)** — no account needed — plus contact info (email, phone, location) |

**Auth-gated utility screens (any role):**

| Route | Screen | Purpose |
| --- | --- | --- |
| `/terms-accept` | Terms consent | First-login gate: must agree to terms before using any dashboard |
| `/change-password` | Change password | Change your own password |

---

# 3. Customer Portal (`/customer`, role: customer)

Layout: customer navigation bar + N.O.U Lite assistant bubble.

| Route | Screen | Purpose |
| --- | --- | --- |
| `/customer` | Dashboard | Overview + announcements feed (maintenance/news) |
| `/customer/downloads` | Downloads | Download purchased products / licensed software |
| `/customer/support` | Support | Submit support tickets, view/reply to own tickets |
| `/customer/projects` | Projects | Submit custom-development **project requests** (NOU-REQ number) + track the full quotation timeline (submitted → under review → feasibility → quoted → **accept/decline quote** → pay → **receipt NOU-RCP** → activated); **Company Portfolio** gallery of published projects (section tabs, product status/platform badges, downloadable deliverables) |
| `/customer/nou-lite` | N.O.U Lite | Full chat history with the AI assistant + order history |

---

# 4. Applicant Portal (`/applicant`, role: applicant)

Layout: applicant navigation bar.

| Route | Screen | Purpose |
| --- | --- | --- |
| `/applicant` | (redirect) | **No applicant dashboard** — `/applicant` redirects straight to the assessment selection |
| `/applicant/applications` | Applications | Job applications + status |
| `/applicant/assessment/:id` | Assessment | Take the AI-graded technical assessment for your chosen **place of qualification** (short-answer/scenario/practical; math editor) |
| `/applicant/results` | Results | Assessment result + competency classification |

**Flow:** apply on Careers (names + email, choose category) → receive temp login by email →
login → assessment for that category → AI grades → admin verifies & selects → promoted
to `developer` → receives results + portal login by email.

---

# 5. Developer Portal (`/portal`, role: developer)

Layout: developer navigation bar + announcements feed.

| Route | Screen | Purpose |
| --- | --- | --- |
| `/portal` | Projects | All company projects: join (headcount rules), 3-project cap, team leader assignment; **department welcome banner** linking to the developer's department community |
| `/portal/department` | My Department | **Department screen** for the developer's place of qualification (professional category): department members with @handles, and the **department's own community** (posts scoped to that category) |
| `/portal/projects/:id` | Project detail | Members, roles (database engineer etc.), documents (spec released at full headcount), **upload completed work**, **weekly progress report** (team leader), **request deadline extension** (max 4 weeks), **request extra developers** (max 3), **help-doc uploads** (anytime), project chat with **Ask N.O.U Lite AI** |
| `/portal/community` | Community | **General community** linking every department — post questions/ideas/showcases (categories), **filter by department** or browse all; each department also has its own community on `/portal/department` |

Portal rules enforced by the API:
- Docs release only when the required headcount has joined.
- A developer may be on at most **3 active projects**.
- Teams may request up to **3 extra developers** (admin approves).
- Only the team leader submits weekly progress / extension requests (403 otherwise).
- Admin is always in the chat (reads/posts without membership).

---

# 6. Investor Portal (`/investor`, role: investor)

| Route | Screen | Purpose |
| --- | --- | --- |
| `/investor` | Projects (read-only) | Company project list: status, **admin-graded progress %**, weekly report history, effective deadline/overdue. **No join/upload/chat actions.** |

Investors who are also developers retain full member access via `/portal`.

---

# 7. Admin Portal (`/admin`, role: admin)

Layout: admin sidebar (12 sections) + announcements.

| Route | Screen | Purpose |
| --- | --- | --- |
| `/admin` | Dashboard | KPIs: users, products, jobs, applications, assessments, orders, investor interests, AI pool state + **Payments Summary** (project payments: collected, pending, receipts, project requests, awaiting deposit/quotation) + **Support Contributions** card (donations separate) |
| `/admin/products` | Products | Create/edit/delete products, publish to catalogue, manage downloads |
| `/admin/users` | Users | Manage accounts, activate/deactivate |
| `/admin/assessments` | Assessments | Configure assessments/modules/questions |
| `/admin/results` | Assessment results | View results; **verify & select** any completed session; approval emails results + portal credentials |
| `/admin/reports` | Reports | Business/assessment reporting |
| `/admin/investors` | Investors | Review investor-interest forms (name, country, monthly amount, expectations, risk knowledge), update status (new/contacted/declined/closed). **No joining-fee fields** (requirement removed) |
| `/admin/onboarding` | Onboarding | Approved candidates → promote to developer (generates credentials, emails them) |
| `/admin/recruitment` | Recruitment | **Direct hire without assessment**: enter official details + official email → credentials emailed; full portal access except admin; lists recruited devs with qualification |
| `/admin/projects` | Company projects | Post projects/jobs (PDF/DOCX spec, headcount), manage members, **grade weekly progress**, approve **extensions** + **extra-developer requests**, review help requests + completed work, **upload software releases** (.apk/.aab/.zip/.exe…), **publish** to gallery (section + product status + platform), chat |
| `/admin/project-requests` | Project requests | Customer custom-solution pipeline: review → feasibility notes → issue **quotation** (amount/currency/validity) → **verify payment** → activate / close |
| `/admin/community` | Community moderation | Moderate the N.O.U. Community feed (hide/delete inappropriate posts) |
| `/admin/nou-lite` | N.O.U Lite orders | Customer orders from the AI assistant; status workflow |
| `/admin/ai-pool` | AI pool | Groq key pool status (keys per section, daily usage, failures, top-ups) |
| `/admin/announcements` | Announcements | Post jokes/quotes/updates to developers/customers; **batch email** broadcast to customers |
| `/admin/support-contributions` | Support contributions | List footer donations (who contributed, amount, method, status, receipt) with collected/pending totals - separate from project payments |

---

# 8. Backend API Surface (13 routers)

Base URL `/api/v1`. Errors are always `{error, message, status_code}`.

### Auth — `/auth` (auth.py)
| Method | Endpoint | Purpose |
| --- | --- | --- |
| POST | `/auth/register` | Create account (visitor/customer/applicant) + send OTP |
| POST | `/auth/register/verify` | Verify registration OTP |
| POST | `/auth/login` | Password login + send OTP (admin → OTP 2-step) |
| POST | `/auth/login/verify` | Verify login OTP → JWT pair |
| POST | `/auth/forgot-password` | Request reset OTP |
| POST | `/auth/reset-password` | Reset password with OTP |
| POST | `/auth/resend-otp` | Resend an OTP |
| POST | `/auth/username` | **Set company @handle** (unique, e.g. @henrydatabase) |
| POST | `/auth/refresh` | Refresh access token |
| GET | `/auth/me` | Current user profile |
| POST | `/auth/accept-terms` | Record first-login terms agreement |
| POST | `/auth/change-password` | Change own password |
| POST | `/auth/logout` | Revoke tokens |

### Products — `/products` (products.py)
`GET /` (catalogue — filters: `search`, `category`, `status`, `platform`, `featured`),
`GET /{id}` (detail), `GET /{id}/download` (licensed download).

### Customers — `/customers` (customers.py)
`GET/PUT /customers/me` (own profile).

### Employment — `/employment` (employment.py)
`GET /jobs`, `GET /jobs/{id}`, `POST /applications`, `GET /applications/me`, `GET /applications/{id}`,
`POST /applications/public-apply` (**guest apply** — names + email + place of qualification,
no account; creates a temp applicant login and emails credentials).

### Assessments — `/assessments` (assessments.py)
`GET /modules`, `GET /results/me`, `GET /`, `GET /{id}`, `GET /active`,
`POST /{id}/start`, `POST /sessions/{id}/submit`, `GET /sessions/{id}/results`.

### Support — `/support` (support.py)
`POST /tickets`, `GET /tickets/me`, `GET /tickets/{id}`, `POST /tickets/{id}/reply`.

### Administration — `/admin` (admin.py)
Dashboard stats; product/job CRUD; user status; ticket assign; assessment config;
assessment-results (incl. verification); investors list/status; onboarding
candidates + decision; company projects CRUD + publish (+section/status/platform);
extensions + extra-request decisions; N.O.U Lite orders; AI pool status.

### Projects (customer) — `/projects` (projects.py)
`POST /projects` (create request → NOU-REQ number; **service_type** + **location** fields),
`POST /projects/public-request` (**guest request**, no account), `GET /projects/me`
(list own requests), `GET /projects/{id}` (detail incl. payments),
`POST /projects/{id}/accept-quotation` | `/decline-quotation`,
`POST /projects/{id}/payments` (submit deposit). Every request is
**owner-scoped** via `_get_owned_request` (another customer's id → 404).
The `NOU-RCP-{year}-{seq}` receipt is assigned by the admin's
`POST /admin/project-requests/{request_id}/payments/{payment_id}/verify`
endpoint when the payment is approved (which also activates the project).

### Payments — `/payments` (payments.py)
`POST /initiate` (customer project payments: M-Pesa **Daraja C2B STK push** or
**Flutterwave card checkout**; simulation mode when provider keys are empty),
`POST /support` (**public support/contribution** — no account or project
needed; creates a `ProjectPayment` with `project_request_id = NULL` and uses
the same M-Pesa/Flutterwave gateways; card redirects to `/support?paid=…`;
Flutterwave receives ISO code **KES** — KSh is mapped), `POST /webhooks/mpesa`
(Daraja callback), `POST /webhooks/flutterwave` (signed webhook → auto-verify
payment + receipt). Config in `backend/.env` (`MPESA_*`, `FLUTTERWAVE_*`).
Admin views support donations via `GET /admin/support-contributions` and the
dashboard includes `support_collected / support_pending / support_count`.
Project payment summaries **exclude** `payment_type=support` rows.

### Software releases (admin) — `/admin` (admin.py)
`POST /projects/{id}/releases` (upload .apk/.aab/.zip/.exe/… ≤300 MB),
`DELETE /projects/{id}/releases/{release_id}`; customers download released builds
from the gallery via a signed URL.

### Investors — `/investors` (investors.py)
`POST /interest` (public, rate-limited 10/hr/IP).

### Projects Portal — `/portal` (projects_portal.py)
List projects (viewer-aware), published gallery (sections), project detail, join/leave,
member roles, request extra developers, weekly progress (submit + admin grade + history),
deadline extensions, help uploads + downloads, document downloads (signed URLs),
work uploads (deadline-enforced), project chat (+ AI).

### N.O.U Lite — `/nou-lite` (nou_lite.py)
`POST /chat` (AI order-taking), `GET /orders`.

### Announcements — `/announcements` (announcements.py)
`POST/GET /announcements`, `DELETE /announcements/{id}`, `POST /announcements/email`
(batch broadcast), `GET /announcements/customers-count`, `GET /announcements/feed`.

### Community — `/community` (community.py)
`POST /posts` (developer-compose; optional **department** — validated against
active professional categories), `GET /posts` (feed with **category + department
filters**), `GET /members?department=…` (**department members** with @handles -
only personnel whose place of qualification matches the department),
admin moderation: `GET /admin/community/posts`, `POST /admin/community/posts/{id}/hide` | `/unhide` | `/delete`.

### Admin quotation pipeline — `/admin` (admin.py, project requests)
`GET /project-requests` (list incl. payments), `POST /project-requests/{request_id}/review`
→ `/feasibility` → `/quotation` (amount/currency/validity),
`POST .../payments/{payment_id}/verify` (issues NOU-RCP receipt + activates),
`POST .../status` (close/cancel etc.). Product CRUD accepts the catalogue fields
(status, platform, featured, version, licence, currency, setup fee).

---

# 9. Background & Integration Services (`backend/app/services/`)

| Service | Purpose |
| --- | --- |
| `ai_assessment.py` | Generates assessment questions + grades answers via Groq |
| `assessment_results.py` | Aggregates/scores sessions into competency results |
| `results_email.py` | Background worker: emails assessment results 2 h after submission; onboarding approval emails (results + portal credentials) |
| `email.py` | SMTP sender + templates (OTP, results, announcements, recruitment credentials) |
| `groq_pool.py` | Groq key pool: per-section pools (assessments/nou_lite/project_chat), 10 keys/day per section, top-up +2 on depletion, auto-rotate failed keys |
| `onboarding.py` | Candidate → developer promotion + credential generation |
| `payments.py` | M-Pesa Daraja C2B STK push + Flutterwave card checkout, webhook verification, payment finalisation (simulation mode without keys) |

## Infrastructure services

| Service | Role | Config |
| --- | --- | --- |
| MySQL 8 | Primary database (aiomysql, pool_size 20 / max_overflow 10) | `DATABASE_URL` in `backend/.env` |
| SMTP | Transactional email (OTP, results, broadcasts) | `SMTP_*` in `.env` (optional) |
| Redis (optional) | Shared rate-limit counters + JWT revocation across workers | `REDIS_URL`; in-memory fallback |
| Groq | AI: assessments, project chat, N.O.U Lite | `GROQ_API_KEYS` pool |
| Uploads | Project docs / help files / completed work (PDF/DOCX/images, ≤10 MB) | `UPLOAD_DIR` |

---

# 10. Error Handling Mechanisms

### Backend
- **HTTP errors** → global `HTTPException` handler returns `{error, message, status_code}` (no HTML/stack).
- **Unhandled exceptions** → global handler logs the full traceback (`loguru`) and returns a generic 500 (`Internal server error`) — **no stack trace leaks to the client**.
- **Validation** → FastAPI 422 with field detail (no sensitive data).
- **Rate limiting** → `app/core/rate_limit.py` (429) on login/OTP, register, investor interest, help uploads, AI calls; Redis-backed when `REDIS_URL` is set.
- **Signed download URLs** → HMAC + expiry; tampered/expired → 403.
- **Path traversal** → `_safe_download_path()` refuses paths outside `UPLOAD_DIR`.

### Frontend
- **Axios interceptors** (`services/api.ts`) — attaches the bearer token; on **401** attempts a single **refresh-token retry**, and if refresh fails clears tokens and redirects to `/login`.
- **Page-level error toasts** via `react-hot-toast` (all forms/mutations show friendly messages).
- **React ErrorBoundary** — top-level boundary catches render errors and shows a friendly fallback instead of a blank page (see `components/ErrorBoundary.tsx`).

### Operational
- Structured logs to `backend/logs/app.log` + console; `X-Process-Time` only in development.
- Health endpoints: `GET /health`, `GET /`.

---

# 11. Load Balancing & High-Traffic Controls

See `deployment/` for the production topology:

- **nginx** (`deployment/nginx.conf`) — single entry point: **least_conn load balancing across N backend replicas**, keepalive upstreams, active health checks, request-rate limiting, gzip, static caching, SPA fallback, `client_max_body_size`, security headers, and HSTS (HTTPS).
- **Backend replicas** — run `uvicorn` with `--workers N` (multi-process) via
  `restart_backend.py --workers N`. **Requires `REDIS_URL`** so rate limits and
  token revocation are shared across workers (in-memory state is single-process only).
- **Database pool** — 20 connections + 10 overflow per worker; MySQL tuned for concurrent async access.
- **Rate limits (API)** — brute-force protection (login/OTP), upload throttling, AI-call budgets, investor spam control.
- **Docker Compose** (`deployment/docker-compose.yml`) — nginx entry + scaled backend + MySQL + optional Redis with healthchecks and resource limits.
- **PWA service worker** — app shell cached; `/api/*` never cached.

---

**Maintained with:** `webstart.md` (local launch), `pentest.md` (security), `Error-Reasolution.md` (issues log), `policies.md` (legal), `today.md` (classification).

**Document status:** Updated 2026-08-10 (guest request/apply pages, admin recruitment + @handles,
place-of-qualification assessment, software releases, M-Pesa/Flutterwave payments, technical
services, admin payments summary, support contributions, department communities, investor
terms/fee removal).
