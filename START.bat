@echo off
cls
color 0A
echo.
echo ╔════════════════════════════════════════════════════════╗
echo ║                                                        ║
echo ║     EMPLOYEE ATTENDANCE API                            ║
echo ║     Professional FastAPI + MongoDB System              ║
echo ║                                                        ║
echo ╚════════════════════════════════════════════════════════╝
echo.

REM Check if MongoDB is configured
if not exist .env (
    echo [ERROR] MongoDB not configured!
    echo.
    echo Please setup MongoDB first:
    echo 1. Use MongoDB Atlas: https://mongodb.com/cloud/atlas
    echo 2. Or install local MongoDB
    echo 3. Copy .env.example to .env
    echo 4. Update MONGO_URI in .env
    echo.
    pause
    exit /b 1
)

echo [1/3] Installing dependencies...
pip install -q -r requirements.txt

echo [2/3] Starting API server...
echo.
echo ╔════════════════════════════════════════════════════════╗
echo ║  API RUNNING                                           ║
echo ║                                                        ║
echo ║  Documentation: http://localhost:8000/docs             ║
echo ║  Health Check:  http://localhost:8000/health           ║
echo ║                                                        ║
echo ║  Press Ctrl+C to stop                                  ║
echo ╚════════════════════════════════════════════════════════╝
echo.

timeout /t 2 /nobreak >nul
start http://localhost:8000/docs

echo [3/3] Server starting...
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
