@echo off
echo ===================================================
echo TikTok链接验证工具自动启动脚本
echo ===================================================
echo.

echo 正在检查Python环境...
python --version 2>NUL
if %ERRORLEVEL% NEQ 0 (
    echo [错误] 未检测到Python，请安装Python后再运行此脚本。
    goto :end
)

echo 正在安装项目依赖...
pip install -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo [警告] 安装依赖时出现问题，但将继续尝试启动程序。
)

echo.
echo 依赖安装完成，正在启动TikTok链接验证工具...
echo.

python run.py

:end
echo.
echo 按任意键退出...
pause > nul 