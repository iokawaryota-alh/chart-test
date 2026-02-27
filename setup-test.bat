@echo off
chcp 65001 > nul
echo ====================================
echo テスト環境 - セットアップ
echo ====================================
echo.

cd /d "%~dp0"

echo Pythonパッケージをインストールしています...
pip install -r requirements.txt

echo.
echo Playwrightブラウザをインストールしています...
playwright install chromium

echo.
echo ====================================
echo セットアップが完了しました！
echo ====================================
echo.
echo テストを実行するには:
echo   1. サーバーを起動: start.bat
echo   2. 新しいターミナルで: pytest test/ -v
echo.
pause
