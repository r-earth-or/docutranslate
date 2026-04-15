@echo off
setlocal

REM 切换到脚本所在目录
cd /d "%~dp0"

REM 检查 .venv 是否存在
if not exist ".venv\Scripts\activate.bat" (
    echo [ERROR] 未找到 .venv\Scripts\activate.bat
    pause
    exit /b 1
)

REM 激活虚拟环境
call ".venv\Scripts\activate.bat"

REM 如果传了参数，就用参数；否则默认用当前目录
if "%~1"=="" (
    python docutranslate/cli.py -i --host 0.0.0.0
) else (
    python docutranslate/cli.py -i "%~1"
)

set EXIT_CODE=%ERRORLEVEL%

REM 退出虚拟环境
call deactivate >nul 2>nul

if not "%EXIT_CODE%"=="0" (
    echo.
    echo [ERROR] 程序退出，返回码: %EXIT_CODE%
    pause
)

exit /b %EXIT_CODE%