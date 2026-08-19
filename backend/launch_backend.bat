@echo off
cd /d "C:\Users\Erick Juma\Projects\N.O.U\backend"
"C:\Users\Erick Juma\AppData\Local\Programs\Python\Python314\python.exe" -m uvicorn app.main:app --host 0.0.0.0 --port 8000 > uvicorn.out.log 2>&1
