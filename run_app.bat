@echo off
REM Script to run the application using the virtual environment
echo Starting FastAPI application using venv...
.\venv\Scripts\python.exe -m uvicorn main:app --reload --port 8001
pause
