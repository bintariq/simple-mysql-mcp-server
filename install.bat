@echo off
echo 🔧 Installing Simple MySQL MCP Server...

IF EXIST config.sample.json (
    copy config.sample.json config.json
    echo ✅ config.json created from config.sample.json
) ELSE (
    echo ❌ config.sample.json not found!
    exit /b 1
)

where pip >nul 2>nul
IF %ERRORLEVEL% NEQ 0 (
    echo ❌ pip not found. Please install Python and pip first.
    exit /b 1
)

pip install -r requirements.txt
echo ✅ Dependencies installed.

echo 🚀 To start the server, run:
echo uvicorn main:app --host 0.0.0.0 --port 8081
