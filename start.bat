@echo off
chcp 65001 > nul
echo ====================================
echo デモサイト - 起動中...
echo ====================================
echo.

cd /d "%~dp0"

echo サーバーを起動しています...
echo ブラウザが自動的に開きます（数秒お待ちください）
echo.
echo サーバーを停止するには、このウィンドウで Ctrl+C を押してください。
echo.

start /min cmd /c "timeout /t 3 /nobreak > nul && start http://localhost:5000"

python app\server.py
