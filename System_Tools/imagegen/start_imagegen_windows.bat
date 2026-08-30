@echo off
setlocal EnableExtensions
chcp 65001 >nul
set "SCRIPT_DIR=%~dp0"

if not "%~1"=="" (
  set "WORK_DIR=%~1"
) else (
  for /f "usebackq delims=" %%I in (`powershell.exe -NoProfile -STA -Command "Add-Type -AssemblyName System.Windows.Forms; $d=New-Object System.Windows.Forms.FolderBrowserDialog; $d.Description='画像を作る作品フォルダを選んでください'; if($d.ShowDialog() -eq 'OK'){ $d.SelectedPath }"`) do set "WORK_DIR=%%I"
)

if not defined WORK_DIR exit /b 1

where py.exe >nul 2>&1
if not errorlevel 1 (
  py.exe -3 "%SCRIPT_DIR%install_for_student.py" "%WORK_DIR%"
  if errorlevel 1 goto :failed
  goto :success
)

where python.exe >nul 2>&1
if errorlevel 1 goto :no_python
python.exe "%SCRIPT_DIR%install_for_student.py" "%WORK_DIR%"
if errorlevel 1 goto :failed

:success
echo.
echo この画面は閉じて構いません。画像生成はバックグラウンドで続きます。
pause
exit /b 0

:no_python
echo Python 3 が見つかりません。Python 3 をインストールしてから、もう一度実行してください。
pause
exit /b 1

:failed
echo.
echo 準備に失敗しました。上のメッセージを講師へ送ってください。
pause
exit /b 1
