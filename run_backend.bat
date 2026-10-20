@echo off
title BookHub Backend Server (FastAPI)
echo ===================================================
echo   DANG KHOI DONG BOOKHUB BACKEND SERVER (PORT 8000)
echo ===================================================
cd /d "%~dp0backend"
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
pause
