@echo on
echo 启动TikTok验证工具（调试模式）...
cd /d %~dp0
echo 当前目录: %CD%
echo 检查Python可执行文件...
python -c "import sys; print('Python路径:', sys.executable)"
echo 检查必要文件...
if exist run.py (echo run.py - 存在) else (echo run.py - 不存在！)
if exist backend\app.py (echo backend\app.py - 存在) else (echo backend\app.py - 不存在！)
if exist frontend\index.html (echo frontend\index.html - 存在) else (echo frontend\index.html - 不存在！)
echo 正在启动服务...
python run.py
pause 