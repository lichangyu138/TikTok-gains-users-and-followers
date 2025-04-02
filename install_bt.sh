#!/bin/bash

echo "==================================================="
echo "TikTok链接验证工具 - 宝塔面板安装脚本"
echo "==================================================="
echo

# 获取当前目录
CURRENT_DIR=$(pwd)
echo "当前目录: $CURRENT_DIR"

# 检查是否在宝塔环境
if [ ! -d "/www/server" ]; then
    echo "[警告] 未检测到宝塔面板环境，但将继续安装..."
fi

echo "正在检查Python环境..."
if ! command -v python3 &> /dev/null; then
    echo "[错误] 未检测到Python，请在宝塔面板中安装Python 3后再运行此脚本。"
    exit 1
fi

# 输出Python版本
PYTHON_VERSION=$(python3 --version)
echo "$PYTHON_VERSION"

# 检查是否已存在虚拟环境
VENV_DIR="/www/server/pyporject_evn/tiktok_venv"
if [ ! -d "$VENV_DIR" ]; then
    echo "创建Python虚拟环境..."
    mkdir -p /www/server/pyporject_evn
    python3 -m venv $VENV_DIR
fi

# 激活虚拟环境
echo "激活虚拟环境..."
source $VENV_DIR/bin/activate

echo "正在安装项目依赖..."
pip install -r requirements.txt

echo
echo "创建启动服务..."

# 创建启动脚本
cat > /www/server/panel/script/tiktok_server.sh << 'EOF'
#!/bin/bash
cd <CURRENT_DIR>
export SERVER_ENVIRONMENT=production
source /www/server/pyporject_evn/tiktok_venv/bin/activate
python3 run.py
EOF

# 替换当前目录
sed -i "s|<CURRENT_DIR>|$CURRENT_DIR|g" /www/server/panel/script/tiktok_server.sh

# 添加执行权限
chmod +x /www/server/panel/script/tiktok_server.sh

# 创建supervisor配置
cat > /www/server/panel/vhost/supervisor/tiktok_server.conf << EOF
[program:tiktok_server]
command=bash /www/server/panel/script/tiktok_server.sh
directory=$CURRENT_DIR
autostart=true
autorestart=true
startretries=3
stderr_logfile=/www/wwwlogs/tiktok_server_err.log
stdout_logfile=/www/wwwlogs/tiktok_server.log
user=root
EOF

# 重启supervisor
echo "正在重启Supervisor服务..."
supervisorctl update
supervisorctl restart tiktok_server

echo
echo "安装完成! TikTok链接验证工具服务已启动。"
echo "服务状态:"
supervisorctl status tiktok_server
echo
echo "您可以通过以下URL访问服务:"
echo "  API文档: http://服务器IP:5166/"
echo "  验证API: http://服务器IP:5166/api/validate"
echo
echo "如需停止服务，请运行: supervisorctl stop tiktok_server"
echo "如需启动服务，请运行: supervisorctl start tiktok_server"
echo "如需查看日志，请查看: /www/wwwlogs/tiktok_server.log"
echo "===================================================" 