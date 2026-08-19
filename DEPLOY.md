# N.O.U Digital Systems — Production Deployment Guide

## Free Hosting Setup (Render + TiDB Cloud)

This guide walks you through deploying the N.O.U platform to **Render** (free tier)
with a **TiDB Cloud** MySQL database (free tier).

---

## Prerequisites

1. A **GitHub** account
2. A **Render** account (free — no credit card) → https://dashboard.render.com
3. A **TiDB Cloud** account (free tier) → https://tidbcloud.com
4. A **Groq** API key → https://console.groq.com/keys
5. A **Gmail** account for OTP emails (with App Password enabled)

---

## Step 1: Push to GitHub

```bash
cd N.O.U
git init
git add .
git commit -m "Initial production commit"
git remote add origin https://github.com/YOUR_USERNAME/nou-digital-systems.git
git push -u origin main
```

> **Note:** Make sure the `.gitignore` file is in place — it excludes `.env`,
> `uploads/`, `logs/`, and other sensitive files.

---

## Step 2: Create MySQL Database (TiDB Cloud)

1. Go to https://tidbcloud.com → Sign up (free)
2. Create a **Serverless Cluster** (free tier: 5 GiB storage)
3. Once created, click **Connect** → **Connect with Standard SQL**
4. Copy the connection string — it looks like:
   ```
   mysql+aiomysql://username:password@gateway01.region.prod.tidbcloud.com:4000/nou_database
   ```
5. Run the schema migration manually:
   ```bash
   # In your local terminal with the TiDB connection string:
   export DATABASE_URL="mysql+aiomysql://username:password@gateway01.region.prod.tidbcloud.com:4000/nou_database"
   cd backend
   python migrate.py
   python seed_admin.py
   ```

---

## Step 3: Deploy Backend on Render

1. Go to https://dashboard.render.com → **New** → **Web Service**
2. Connect your GitHub repo → Select the `nou-digital-systems` repo
3. Configure:
   - **Name:** `nou-backend`
   - **Region:** Frankfurt (closest to Kenya)
   - **Runtime:** Python 3
   - **Root Directory:** `backend`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. Add **Environment Variables** (click "Advanced" → "Add Env Variable"):

   | Key | Value |
   |-----|-------|
   | `ENVIRONMENT` | `production` |
   | `DEBUG` | `false` |
   | `SECRET_KEY` | *(generate a random 32+ char string)* |
   | `DATABASE_URL` | *(paste your TiDB connection string)* |
   | `CORS_ORIGINS` | `https://nou-frontend.onrender.com` |
   | `NOU_ADMIN_EMAIL` | `your-admin@gmail.com` |
   | `NOU_ADMIN_PASSWORD` | `your-strong-password` |
   | `SMTP_HOST` | `smtp.gmail.com` |
   | `SMTP_PORT` | `587` |
   | `SMTP_USER` | `your-gmail@gmail.com` |
   | `SMTP_PASSWORD` | `your-gmail-app-password` |
   | `EMAILS_FROM_EMAIL` | `your-gmail@gmail.com` |
   | `GROQ_API_KEY` | `your-groq-key` |
   | `FRONTEND_BASE_URL` | `https://nou-frontend.onrender.com` |

5. Click **Create Web Service**
6. Wait for the build to complete (~3-5 min)
7. Your backend URL will be: `https://nou-backend.onrender.com`

---

## Step 4: Deploy Frontend on Render

1. Go to https://dashboard.render.com → **New** → **Static Site**
2. Connect your GitHub repo
3. Configure:
   - **Name:** `nou-frontend`
   - **Region:** Frankfurt
   - **Root Directory:** `frontend`
   - **Build Command:** `npm install && npm run build`
   - **Publish Directory:** `dist`
4. Add **Environment Variable**:

   | Key | Value |
   |-----|-------|
   | `VITE_API_BASE_URL` | `https://nou-backend.onrender.com/api/v1` |

5. Under **Rewrites/Routes**, add:
   - **Source:** `/*`
   - **Destination:** `/index.html`
6. Click **Create Static Site**
7. Wait for build (~2-5 min)
8. Your frontend URL will be: `https://nou-frontend.onrender.com`

---

## Step 5: Post-Deployment

1. **Update CORS:** Go to the backend service → Environment → set
   `CORS_ORIGINS` to `https://nou-frontend.onrender.com`

2. **Run migrations on TiDB:**
   ```bash
   # Connect to TiDB and run:
   cd backend
   python migrate.py
   python seed_admin.py
   ```

3. **Seed the question banks:**
   ```bash
   python generate_banks.py
   python seed_banks.py
   ```

4. **Test:**
   - Open `https://nou-frontend.onrender.com`
   - Test registration, assessment, admin login
   - Verify OTP emails arrive

---

## Important Notes

- **Render Free Tier:** Services sleep after 15 min of inactivity. First request
  after sleep takes 30-50 seconds to wake. This is normal for free tier.
- **TiDB Free Tier:** 5 GiB storage, shared resources. Sufficient for development
  and light production use.
- **Gmail SMTP:** Use a Gmail App Password (not your regular password).
  Enable 2FA → Google Account → Security → App Passwords.
- **Groq Free Tier:** Limited API calls per day. The per-feature key pool system
  handles quota management automatically.
- **Admin Login:** Two-factor — after entering admin credentials, an OTP is
  emailed. Check the email for the code.

---

## Custom Domain (Optional)

Once deployed, you can add a custom domain:
1. Buy a domain (e.g., from Namecheap, Cloudflare Registrar)
2. On Render, go to your service → Settings → Custom Domains
3. Add your domain and update DNS as instructed
4. Render auto-provisions free SSL certificates

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Backend 500 error | Check Render logs → Environment tab |
| CORS error in browser | Ensure `CORS_ORIGINS` matches your frontend URL exactly |
| OTP emails not arriving | Verify Gmail App Password, check SMTP settings |
| Database connection fails | Verify TiDB connection string, ensure IP whitelist includes Render |
| Assessment questions empty | Run `python generate_banks.py && python seed_banks.py` |
| Frontend can't reach API | Verify `VITE_API_BASE_URL` env var on the frontend service |
