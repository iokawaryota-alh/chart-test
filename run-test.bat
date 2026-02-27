@echo off
chcp 65001 > nul
echo ====================================
echo テスト実行
echo ====================================
echo.

cd /d "%~dp0"

echo サーバーが起動していることを確認してください
echo (起動していない場合は、別のターミナルで start.bat を実行)
echo.
echo テストを開始します...
echo.

pytest test/ -v

echo.
pause
