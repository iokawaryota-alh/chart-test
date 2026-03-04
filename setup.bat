@echo off
chcp 65001 > nul
echo ====================================
echo デモサイト - 初回セットアップ
echo ====================================
echo.

echo Pythonのバージョン確認中...
python --version
if errorlevel 1 (
    echo エラー: Pythonがインストールされていません。
    echo Python 3.7以降をインストールしてください。
    pause
    exit /b 1
)

echo.
echo 依存パッケージをインストールしています...
pip install -r requirements.txt

if errorlevel 1 (
    echo エラー: Flaskのインストールに失敗しました。
    pause
    exit /b 1
)

echo.
echo ====================================
echo セットアップ完了！
echo ====================================
echo.
echo 次回からは start.bat を実行してください。
echo.
pause
