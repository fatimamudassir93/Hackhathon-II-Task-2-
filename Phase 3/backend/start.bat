@echo off
echo Starting FastAPI backend on port 8001...
cd /d "%~dp0"
call venv\Scripts\activate.bat
uvicorn src.main:app --reload --host 0.0.0.0 --port 8001
