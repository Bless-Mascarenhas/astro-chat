@echo off
title AstroChat Launcher
color 0D

echo.
echo  ✦ AstroChat — Cosmic AI Guide
echo  ═══════════════════════════════
echo.

REM ── Step 1: Allow browser requests to Ollama (CORS fix) ──
set OLLAMA_ORIGINS=*

REM ── Step 2: Pull model if not already downloaded ──
echo  [1/3] Checking Ollama model (qwen3.5:4b)...
ollama pull qwen3.5:4b
if %ERRORLEVEL% NEQ 0 (
  echo  [WARN] Could not pull model. Make sure Ollama is installed.
  echo         Download: https://ollama.com/download
)

echo.
echo  [2/3] Starting Ollama server with CORS enabled...
start "" cmd /c "set OLLAMA_ORIGINS=* && ollama serve"
timeout /t 3 /nobreak >nul

echo.
echo  [3/3] Starting AstroChat web server on port 8080...
echo.
echo  ══════════════════════════════════════════
echo    Open in browser:  http://localhost:8080
echo  ══════════════════════════════════════════
echo.
echo  Press Ctrl+C to stop the server.
echo.

cd /d "%~dp0"
python server.py
