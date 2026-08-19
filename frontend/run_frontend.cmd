@echo off
rem Detached launcher for the N.O.U frontend (Vite dev server on :3000).
cd /d "C:\Users\Erick Juma\Projects\N.O.U\frontend"
cmd /c "npm run dev > vite.out.log 2>&1"
