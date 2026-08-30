@echo off
setlocal

:: =====================================================================
:: All three servers live in this same folder — edit only if it moves
:: =====================================================================
set PROJECT_DIR=C:\Users\bgmik\OneDrive\Desktop\Anahita
:: =====================================================================

echo.
echo [1/3] Starting TrueForge server (via WSL)...
start "TrueForge Server" cmd /k "cd /d "%PROJECT_DIR%" && wsl npx @truefoundry/trueforge"

echo Waiting 15s for TrueForge to come up on localhost:8790...
timeout /t 15 /nobreak >nul

echo.
echo [2/3] Starting Anahita voice server (TTS proxy)...
start "Anahita Voice Server" cmd /k "cd /d "%PROJECT_DIR%" && call .venv\Scripts\activate.bat && uvicorn tts_proxy:app --host 0.0.0.0 --port 8791"

echo Waiting 5s for voice server to come up on port 8791...
timeout /t 5 /nobreak >nul

echo.
echo [3/3] Starting Anahita UI server...
start "Anahita UI Server" cmd /k "cd /d "%PROJECT_DIR%" && node proxy.js"

echo Waiting 3s for UI server to come up on port 4000...
timeout /t 3 /nobreak >nul

echo.
echo All three servers launched. Opening Anahita in Edge...
start msedge "http://localhost:4000/anahita.html"

endlocal