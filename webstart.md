# N.O.U Digital Systems — How to Start (Command Prompt Guide)

This guide explains exactly how to start the **backend** and **frontend** of the
N.O.U website from the Windows **Command Prompt (cmd)**, after a fresh boot or
when the servers are not running.

> **Quick reference**
> - Backend API: **http://localhost:8000** (health check: `http://localhost:8000/health`)
> - Frontend website: **http://localhost:3000**
> - API docs (dev): **http://localhost:8000/api/docs**

---

## 0. Prerequisites (one-time setup)

| Requirement | Check it works |
| --- | --- |
| **Node.js 18+ / npm** | `node --version` and `npm --version` |
| **Python 3.10+** | `python --version` |
| **MySQL 8** running on `localhost:3306` | `mysql --version` (and the MySQL service must be started) |
| **Frontend dependencies** | `frontend\node_modules` must exist (run `npm install` once if missing) |
| **Backend .env** | `backend\.env` must exist (copy from `.env.example` and edit) |
| **Database** | `nou_database` must exist on MySQL with the schema applied (see section 3) |

On this machine the Python interpreter is:
```
C:\Users\Erick Juma\AppData\Local\Programs\Python\Python314\python.exe
```
and the backend `.env` is already configured (MySQL, Groq key, secret, CORS).

---

## 1. Start the Backend (FastAPI / Uvicorn on port 8000)

### Option A — One-command restart script (recommended)

Open **Command Prompt** and run:

```bat
cd /d C:\Users\Erick Juma\Projects\N.O.U\backend
"C:\Users\Erick Juma\AppData\Local\Programs\Python\Python314\python.exe" restart_backend.py
```

This script:
1. Kills anything already listening on port **8000**.
2. Starts `uvicorn app.main:app --host 0.0.0.0 --port 8000`.
3. Waits for the `/health` endpoint and prints:
   ```
   health-after (Xs): 200 {"status":"healthy",...}
   ```
   Logs are written to `backend\uvicorn-ai.log`.

### Option B — Manual uvicorn (visible in the window)

```bat
cd /d C:\Users\Erick Juma\Projects\N.O.U\backend
"C:\Users\Erick Juma\AppData\Local\Programs\Python\Python314\python.exe" -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

You should see:
```
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

> ⚠️ The backend creates/verifies the database tables at startup and takes
> **20–60 seconds** to become healthy (MySQL connection + table checks). Wait
> for `Application startup complete` before moving on.

### Verify the backend

Open a browser and visit **http://localhost:8000/health** — you should see:
```json
{"status":"healthy","timestamp":...,"version":"1.0.0","environment":"development"}
```

---

## 2. Start the Frontend (Vite dev server on port 3000)

Open a **second Command Prompt** window and run:

```bat
cd /d C:\Users\Erick Juma\Projects\N.O.U\frontend
npm run dev
```

You should see:
```
  VITE v5.4.21  ready in ~3 s
  ➜  Local:   http://localhost:3000/
```

### Verify the frontend

- Open **http://localhost:3000** — the N.O.U home page should load.
- The frontend proxies `/api` to the backend automatically (configured in
  `frontend\vite.config.ts`), so no extra configuration is needed.

> 🔑 **Important:** `frontend\.env` must keep `VITE_API_BASE_URL=/api/v1`
> (the **relative** path). If it is changed to `http://localhost:8000/api/v1`,
> the browser's Content-Security-Policy blocks the API calls and products /
> careers / admin pages show empty data. If you change `.env`, **restart**
> `npm run dev` (the dev server reads `.env` only at startup).

---

## 3. Database Setup (only the first time / after a fresh MySQL)

The backend auto-creates missing tables at startup, but you must create the
database and load seed data (products, jobs, demo users) once:

```bat
cd /d C:\Users\Erick Juma\Projects\N.O.U
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS nou_database;"
mysql -u root -p nou_database < database\schema.sql
mysql -u root -p nou_database < database\seeds.mysql.sql
```

> `seeds.mysql.sql` is the **MySQL-compatible** seed script (the original
> `seeds.sql` is PostgreSQL-only and will fail on MySQL). It is idempotent —
> safe to re-run.

### Demo accounts (from the seed)

| Role | Email | Password |
| --- | --- | --- |
| Admin | `admin@nou.com` | `admin123` (login requires an OTP code shown on screen in dev mode) |
| Customer | `john.doe@example.com` | `password123` |
| Applicant | `jane.smith@example.com` | `password123` |

---

## 4. Stopping the Servers

- **Frontend**: press `Ctrl+C` in the Vite window.
- **Backend (manual)**: press `Ctrl+C` in the uvicorn window.
- **Backend (restart script)**: re-run `restart_backend.py` — it kills the
  old process automatically.

---

## 5. Troubleshooting

| Symptom | Fix |
| --- | --- |
| `Port 8000 is already in use` | Run `restart_backend.py` (kills the old process), or manually: `netstat -ano \| findstr :8000` then `taskkill /F /PID <pid>` |
| `Port 3000 is already in use` | Vite auto-switches to 3001/3002 — or kill the old node process. |
| `Can't connect to MySQL` | Ensure the MySQL service is running and `backend\.env` has the correct `DATABASE_URL`. |
| Backend starts but `/health` hangs | Wait 30–60 s (table verification). If it still fails, check `backend\uvicorn-ai.log`. |
| Products/Careers pages show "No products found" | `frontend\.env` must have `VITE_API_BASE_URL=/api/v1`, then restart `npm run dev`. |
| Assessment returns 502 "Groq rate limit" | The free Groq tier was momentarily rate-limited (a full assessment generates 160 questions in 16 rapid calls). Wait a minute and retry; or upgrade the Groq tier. |
| Admin login asks for an OTP you don't have | In development the code is **shown on the login screen** (dev mode). |
| Home page won't load / Chrome says connection refused (fixed 2026-08-10) | `vite.config.ts` now sets `server.host: '0.0.0.0'`. Previously Vite bound only to IPv6 `::1`, so Chrome's IPv4 connection to `localhost:3000` failed. If the server was started before this fix, restart `npm run dev`. |
| Dev websocket (HMR) keeps failing with `WebSocket handshake 400` | Remove any explicit `server.hmr.host/protocol` override (Vite auto-configures HMR). Also, a **stale service worker** can cache an old app shell — bump `const VERSION` in `frontend/public/sw.js` (e.g. `nou-v1.0.1`) so `activate` purges old caches, then hard-refresh (Ctrl+Shift+R) once. |
| API calls blocked by CSP (`connect-src 'self'`) even though `.env` is correct | This is almost always a **stale service worker** serving an old cached build (the cache-first asset handler). Fix: bump the SW `VERSION` in `frontend/public/sw.js`, then hard-refresh twice or clear site data for `localhost:3000`. Verify the live code is correct with: `curl http://localhost:3000/api/v1/products/` (must return JSON through the proxy). |

---

## 6. Useful Commands & Checks

```bat
:: Backend health
curl http://localhost:8000/health

:: Frontend (served page returns 200)
curl -o NUL -w "%%{http_code}" http://localhost:3000

:: API through the frontend proxy (same as the browser)
curl http://localhost:3000/api/v1/products/

:: Frontend type check + production build
cd /d C:\Users\Erick Juma\Projects\N.O.U\frontend
npx tsc --noEmit
npm run build
```

---

## 7. Investor Funding Section (added 2026-08-07, expanded 2026-08-10)

Investors can submit their funding interest from the public page:

- **Public page:** http://localhost:3000/investors
  (name, email, phone, country, organization, investment range, **monthly
  investment amount**, **expectations while joining**, **knowledge of business
  risks**, message — **no joining fee**; the team reviews the details and
  contacts the investor directly)
- **Admin review:** http://localhost:3000/admin/investors
  (list, view details incl. the new questions, change status: new / contacted /
  declined / closed — **joining-fee fields removed** from the UI and API)
- **API:** `POST /api/v1/investors/interest` (public, rate-limited 10/hour/IP)
  and `GET/PUT /api/v1/admin/investors...` (admin only).
- The admin dashboard also shows an **Investor Interests** counter.

### Support contributions (footer)
- The public footer now has a **Support** section linking to
  http://localhost:3000/support — anyone can send the company money via
  **M-Pesa (STK push)** or **card (Flutterwave)**, no account needed.
- API: `POST /api/v1/payments/support` (public, rate-limited 5/hour/IP).
  Creates a `ProjectPayment` with `project_request_id = NULL`; admin sees the
  contribution in the payments summary. Card checkout redirects back to
  `/support?paid=<id>`.

---

## 8. Developer Onboarding & Projects Portal (added 2026-08-07)

### How developers get in
1. Applicants pass the AI-graded assessment (threshold).
2. Their details appear under **Admin → Onboarding**
   (http://localhost:3000/admin/onboarding).
3. When the admin **approves**, the applicant is promoted to `developer`, new
   login credentials are generated, and an email with their results +
   credentials is sent (results are also shown on screen in dev mode).
4. The developer logs in and lands on the **Projects Portal**
   (http://localhost:3000/portal).

### Portal rules (implemented in the API)
- Admin posts projects/jobs (with optional PDF/DOCX spec) and sets the
  required headcount: **Admin → Projects** (http://localhost:3000/admin/projects).
- Documentation is **locked until the required number of developers join**;
  if 1 person is required, the first joiner works alone.
- A developer may be on **at most 3 active projects**.
- Teams have a **team leader** (first joiner); members set **roles** (e.g.
  database engineer) and are not restricted to one role.
- Overwhelmed teams can **request up to 3 extra developers** (admin approves
  via the extra-requests tab).
- Members chat per project and can **ask the AI** (Groq) for help on bugs/
  problems (**Ask N.O.U Lite AI** checkbox in chat).
- Completed work is uploaded for **admin review**, then the admin can
  **publish** it for customers.

### Investor read-only access
Investors (registered with role `investor`) can **view** company project
progress at http://localhost:3000/investor — read-only, no join/chat actions.
A user can be both an investor and a developer (full member access).

---

## 9. N.O.U Lite — Customer AI Assistant (added 2026-08-07)

N.O.U Lite is the website's AI assistant (modeled on the WhatsApp chatbot). It
**takes customer orders** (products, projects, support) conversationally:

- Floating chat bubble on the public site and customer dashboard.
- Full chat + order history: http://localhost:3000/customer/nou-lite
  (customer must be logged in).
- Orders are stored and visible to admins at
  http://localhost:3000/admin/nou-lite (status: new / in_progress /
  completed / declined, with the full AI transcript).
- Uses the **Groq key pool** (`nou_lite` section).

---

## 10. Groq Key Pool (added 2026-08-07)

The backend now shares Groq API keys through a key pool instead of one key:

- `GROQ_API_KEYS` (comma-separated) in `backend\.env` — if empty, the existing
  `GROQ_API_KEY` is used (current config: 1 key).
- **10 keys/day per AI section** (assessments, project chat, nou_lite), and if
  a section depletes its keys it is **topped up with 2 extra for the day**.
- Keys that return auth errors are **automatically removed from rotation**.
- Admin status page: http://localhost:3000/admin/ai-pool
  (active key, requests used today, daily limit, failed keys).
- When you have 60 real keys, paste them comma-separated into `GROQ_API_KEYS`
  and restart the backend — the pool will rotate through them automatically.

---

## 11. Weekly Progress Reports, Help Requests & Published Gallery (added 2026-08-07)

### Weekly progress reports (graded %)
- The **team leader** submits a weekly progress report (week label, 0–100%,
  summary) from the project page in the developer portal.
- Only the team leader can submit (non-leaders get 403); one report per week
  label is enforced.
- **Investors** see the graded progress (latest % + full report history) on
  their read-only page at http://localhost:3000/investor.
- Admins see reports under **Admin → Projects → Chat & progress**.
- API: `POST/GET /api/v1/portal/projects/{id}/progress`.

### Developer help requests (upload a document for help, anytime)
- Any project member can upload a PDF/DOCX with a message asking for help
  (rate-limited 10/hour per user).
- Admins see the request (with a **Download** link) under
  **Admin → Projects → Chat & progress**; the team sees it in the project page.
- API: `POST /api/v1/portal/projects/{id}/help`,
  `GET .../help`, `GET .../help/{help_id}/download` (members + admin only).
- Project documentation (spec/completed) can also be downloaded:
  `GET /api/v1/portal/projects/{id}/documents/{doc_id}/download` (members +
  admin; investors only when docs are released).

### Customer project gallery
- Completed projects published by admin appear in the customer portal at
  http://localhost:3000/customer/projects ("Company Portfolio").
- API: `GET /api/v1/portal/projects/published` (any logged-in user; omits
  internal help requests).

### Admin is always in the project chat
- Admins can read and post in any project chat (Admin → Projects →
  Chat & progress), even without being a member.

---

## 12. Database Migration & Key Rotation

### Migration script
After pulling new code, run the idempotent migration (adds missing columns/
verifies tables - safe to re-run):
```bat
cd /d C:\Users\Erick Juma\Projects\N.O.U\backend
"C:\Users\Erick Juma\AppData\Local\Programs\Python\Python314\python.exe" migrate.py
```

### Test suites (all green)
```bat
cd /d C:\Users\Erick Juma\Projects\N.O.U\backend
"C:\Users\Erick Juma\AppData\Local\Programs\Python\Python314\python.exe" test_support_departments.py :: 20 checks (support contributions, department communities, investor fee removal)
```
(Other throwaway test scripts from earlier sessions were cleaned up after their
final green runs; the features they covered remain verified live.)

**New roles:** `developer` (projects portal), `investor` (read-only progress
view). Login redirects developers to `/portal` and investors to `/investor`.

---

## 13. Admin Grading, Deadlines, Publish Sections & Signed Downloads (added 2026-08-08)

### Admin grades weekly progress
- Admins grade each weekly report under **Admin → Projects → Chat & progress**
  (0–100%). The admin's grade is the **official percentage** investors see;
  until graded, the leader-reported value is shown.
- API: `POST /api/v1/portal/projects/{id}/progress/{report_id}/grade` (admin).

### Deadline enforcement + extensions (max 4 weeks)
- Completed work uploads are **blocked after the effective deadline** passes.
- The team leader can **request an extension** (max 28 days) from the project
  page; the admin approves/denies it under **Admin → Projects → Extensions**.
- Effective deadline = scheduled deadline + approved days; the investor page
  shows the effective deadline and overdue status.
- API: `POST /api/v1/portal/projects/{id}/extension` (team leader),
  `GET/POST /api/v1/admin/projects/extensions...` (admin).

### Publish sections (N.O.U. category system)
- When publishing a completed project the admin picks a **section** from the
  full N.O.U. software-category list (Games and Entertainment, Bots, Education
  and Learning, Business and Enterprise, Finance and Accounting, Networking and
  Infrastructure, Artificial Intelligence, ... — see `today.md`).
- The customer gallery renders **section tabs** automatically from the
  published sections (http://localhost:3000/customer/projects).

### Secure signed download URLs
- Document/help download links are now **short-lived HMAC-signed tokens**
  (30 min, bound to the recipient class: member / investor / customer) so a
  copied link cannot be shared forever. Investors cannot open completed-work
  docs; customers can only open docs of **published** projects.
- Expired/tampered tokens return 403; downloads still work with a normal login
  for members/admins.

### Multi-worker hardening
- The rate limiter and JWT token revocation now **optionally use Redis** when
  `REDIS_URL` is set in `backend\.env`, and transparently fall back to
  in-memory storage otherwise — safe to run on one worker or many.

### Assessment verification / selection
- Admins can verify & select **any completed assessment** (not just AI-pass) in
  **Admin → Assessment Results**; approving sends the results + new project
  portal login credentials to the applicant by email.

---

## 14. Terms & Policies, Announcements & Batch Email (added 2026-08-08)

### Terms of use gate (first login)
- Full terms live at http://localhost:3000/terms and privacy at
  http://localhost:3000/privacy — rewritten to mirror the current
  `policies.md` (version 1.0, effective 7 Aug 2026): customer T&C, software
  licensing & distribution, privacy (Data Protection Act 2019), the developer
  engagement agreement (minimum periods subject to employment law and lawful
  termination rights), company policies for developers (incl. AI-tool rules),
  IP & confidentiality, project development, and the dispute-resolution
  ladder. **The investor participation framework has been removed from the
  terms** (and from the first-login consent screen). Contacts:
  noudigitalsystem@gmail.com · nouprivacy@gmail.com · 079298662 · Kisumu.
- New accounts must **agree to the terms on first login** before they can use
  any dashboard (backend gate + redirect screen). Registering also requires
  ticking the terms checkbox.
- API: `POST /api/v1/auth/accept-terms`; `terms_accepted_at` is stored on the
  user record.

### Announcements (jokes of the day, quotes, updates)
- Admins post announcements at http://localhost:3000/admin/announcements
  (title, body, audience: developers / customers / both).
- Developers see the feed on the portal dashboard; customers on the customer
  dashboard; investors on their page.
- API: `POST/GET/DELETE /api/v1/announcements` (admin posts/deletes, role-
  scoped reads).

### Batch email to customers
- Admins can **broadcast an announcement by email** to all customers from the
  announcements page (used for maintenance notices or new services). Sends run
  concurrently (bounded pool) so they complete quickly even with many
  customers; each recipient also gets an in-app announcement.
- API: `POST /api/v1/announcements/broadcast` (admin).

---

## 15. Branding & House Style (added 2026-08-08)

- **Favicon:** `frontend\public\favicon.svg` — N.O.U. mark in the brand palette
  (white / green / dark blue).
- **Home page:** the favicon image is used as a **banner** on the home screen
  (hero), so the logo is front and centre.
- **Theme:** brand colors and the site font are driven by **CSS custom
  properties** (`:root` in `frontend\src\index.css`) — white, green and dark
  blue with room for customization. Tailwind is wired to the same palette
  (`frontend\tailwind.config.js`).
- Emoji characters have been **removed** across the frontend, backend and
  templates (only functional math arrows remain in the assessment editor).

---

## 16. N.O.U is a Progressive Web Application (added 2026-08-08)

The site is installable and works offline as a PWA:

- **Icon:** `frontend\public\favicon1.png` (512×512 brand icon, plus
  192×192, 180×180 apple-touch, and a maskable 512×512 variant — generated
  from the favicon SVG).
- **Manifest:** `frontend\public\manifest.webmanifest` — name "N.O.U Digital
  Systems", theme colour `#0f172a` (dark blue), display standalone, app
  shortcuts for Products / Careers / Invest.
- **Service worker:** `frontend\public\sw.js` — caches the app shell for
  offline start, cache-first for built assets (stale-while-revalidate),
  network-first for navigations, and **never caches `/api/*`** (private data).
  Registered automatically from `frontend\src\main.tsx`.
- **index.html** declares the manifest, theme colour, apple-touch-icon and
  iOS/mobile web-app meta tags.
- Install from the browser's address bar / Install app button after visiting
  the site. The production build copies all PWA files into `dist\`.

### Product classification on published projects (today.md)

When publishing a completed project the admin also picks the **product
status** (Free / Paid / Subscription / Freemium / Enterprise / Custom /
Internal) and **platform** (Web / PWA / Android / Windows / iOS / Cloud-SaaS /
Multi-Platform) from the N.O.U. classification system in `today.md`; the
customer gallery shows these as badges next to the section.

---

## 17. Customer Quotation & Payment Workflow (added 2026-08-09)

The remaining `today.md` services are implemented end-to-end:

### How a customer buys a custom solution
1. Customer opens **My Projects** in the customer dashboard
   (http://localhost:3000/customer/projects) and submits a **project
   request** (title, description, budget range, preferred timeline). The API
   returns a request number (`NOU-REQ-xxxxx`).
2. Admin reviews it at **Admin → Project Requests**
   (http://localhost:3000/admin/project-requests) — status moves
   submitted → under review → **feasibility** (admin notes) → **quoted**
   (amount, currency, validity date).
3. Customer sees the quote, **accepts or declines** it. On acceptance a
   **payment form** appears; the customer submits the deposit (M-Pesa
   reference or card) with the amount and method.
4. Admin **verifies the payment** (`POST .../payments/{payment_id}/verify`)
   — on approval the payment gets its official `NOU-RCP-{year}-{seq}`
   receipt number and the project is **activated** automatically. The
   customer sees the full timeline (submitted → quoted → paid → activated)
   with the receipt number and its verification status.

APIs: `POST /api/v1/projects/projects`, `GET /api/v1/projects/projects/me`,
`GET /api/v1/projects/projects/{id}`, `POST .../{id}/accept-quotation`,
`POST .../{id}/decline-quotation`, `POST .../{id}/payments`;
admins: `GET /api/v1/admin/project-requests`, `POST .../{request_id}/review`,
`.../feasibility`, `.../quotation`, `.../payments/{payment_id}/verify`
(issues the NOU-RCP receipt + activates), `.../status`.

### Product catalogue (public)
The products page (http://localhost:3000/products) now has a **filter bar**
(search, category, product status, platform, featured only) and cards show
status/platform/featured badges. Admin add/edit product forms include the new
fields (status, platform, featured, version, licence, currency, setup fee).

### Home screen (today.md Ch.5)
The home page is rebuilt around the brand: hero using your **Banner.png**,
catalogue categories, featured + new-release rails, services, a custom-solution
CTA, careers and investor call-outs. Your real `Favicon1.png` / `Banner.png`
are now `frontend\public\favicon1.png` / `banner.png`.

### N.O.U. Community (developers)
- **General community** (links every department):
  http://localhost:3000/portal/community — post questions, ideas and status
  updates (categories: general / help / ideas / showcase / jobs / off-topic),
  filter by department or browse all.
- **Department communities:** each professional category has its own
  community at http://localhost:3000/portal/department ("My Department" in the
  developer nav) — shows the developer's place of qualification, the
  department members with @handles, and a department-scoped feed.
- **Admins:** http://localhost:3000/admin/community — moderate the feed
  (hide / delete inappropriate posts).
- API: `POST/GET /api/v1/community/posts` (optional `department` field +
  filter), `GET /api/v1/community/members?department=...`.

### Validation for the latest features
```bat
cd /d C:\Users\Erick Juma\Projects\N.O.U\backend
"C:\Users\Erick Juma\AppData\Local\Programs\Python\Python314\python.exe" test_support_departments.py  :: 20 checks (support contributions, department communities, investor fee removal)
```

### Validation
```bat
:: Full suite (adds the today.md regression: 40 checks)
cd /d C:\Users\Erick Juma\Projects\N.O.U\backend
"C:\Users\Erick Juma\AppData\Local\Programs\Python\Python314\python.exe" test_todaymd.py
```

The throwaway test scripts were removed from the repo after the final green
run (the features they covered are verified live in section 18).

---

## 18. Guest Flows, Admin Recruitment & Company Handles (added 2026-08-10)

### No account needed for customers or applicants
- **Customers** request an app/project from the public page
  (http://localhost:3000/request-project) — no registration. They pick a
  **service type** (Software Development, **WiFi Installation**, **CCTV
  Installation**, **IT Consultancy**) and optionally a **location**, and the
  request appears in **Admin → Customer Requests**.
- **Applicants** apply for jobs from http://localhost:3000/careers — they only
  enter their **official names + email** (no account). An email with temporary
  login credentials is sent so they can take the assessment; results are
  emailed to the same address. **There is no applicant dashboard** — applicants
  go straight to the assessment after login.

### Every applicant chooses their place of qualification
- In the apply form (and again before starting the assessment) the applicant
  picks the **professional category** they will be assessed in (e.g. John
  chooses *Software Engineering* → John is assessed on Software Engineering)
  and an optional position.
- The chosen qualification is saved on the account and **pre-selected** when
  the assessment starts.

### Admin recruitment (direct hire, no assessment)
- **Admin → Recruitment** (http://localhost:3000/admin/recruitment) lets an
  admin enter a developer's official details + official email.
- Login credentials are generated and **emailed** to them (the email explains
  the @handle step). The recruited developer gets full access to the projects
  portal and community — everything except the admin section — **without
  taking an assessment**.
- Recruited developers are listed on the same page with their qualification
  category.
- API: `POST /api/v1/admin/recruit`, `GET /api/v1/admin/recruited` (admin).

### Company handles (@username)
- After receiving credentials, each developer **creates their company handle**
  once (e.g. `@henrydatabase`) from the banner in the developer portal
  (`POST /api/v1/auth/username`).
- The handle is used to interact with other developers in the **community**
  and on **projects** (shown as `@handle` next to posts/authors).
- Handles are **unique** — a taken handle returns 409.

### Software releases for customers
- Admins upload the developed software (**.apk, .aab, .zip, .exe, .msi,
  .dmg, ...**) for a project from **Admin → Projects → Releases**
  (`POST /api/v1/admin/projects/{id}/releases`, up to 300 MB).
- Customers download the released build from the gallery
  (http://localhost:3000/customer/projects) once the project is published
  (signed, short-lived download URL).

### Payments: M-Pesa Daraja C2B + Flutterwave (cards)
- Customer deposits can be paid via **M-Pesa STK push** (Daraja C2B) or
  **Flutterwave card checkout** — configured in `backend/.env`:
  `MPESA_CONSUMER_KEY/SECRET/SHORTCODE/PASSKEY` and
  `FLUTTERWAVE_SECRET_KEY/PUBLIC_KEY/WEBHOOK_SECRET_HASH`.
- **When the keys are empty the system runs in SIMULATION mode** (records the
  payment as pending without contacting the provider) so the flow is fully
  testable locally. Paste your real credentials into `backend/.env` and
  restart when ready.
- Webhooks: `POST /api/v1/payments/webhooks/mpesa` (Daraja callback) and
  `POST /api/v1/payments/webhooks/flutterwave` — both verify signatures and
  auto-finalize the payment (status → successful + receipt number).

### Payments summary on the admin dashboard
- **Admin → Dashboard** shows a Payments Summary card: total collected,
  awaiting verification (with count), successful receipts, project requests,
  awaiting deposit and quotation-issued counts — all computed live.

---

**Last updated:** 2026-08-10
