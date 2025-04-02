#!/bin/bash

echo "==================================================="
echo "TikTok链接验证工具自动启动脚本"
echo "==================================================="
echo

echo "正在检查Python环境..."
if ! command -v python3 &> /dev/null; then
    echo "[错误] 未检测到Python，请安装Python后再运行此脚本。"
    exit 1
fi

# 输出Python版本
python3 --version

echo "正在安装项目依赖..."
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "[警告] 安装依赖时出现问题，但将继续尝试启动程序。"
fi

echo
echo "依赖安装完成，正在启动TikTok链接验证工具..."
echo

# 设置服务器环境变量
export SERVER_ENVIRONMENT=production

# 检查端口5166是否已被占用
if netstat -tuln | grep -q ":5166 "; then
    echo "[警告] 端口5166已被占用，尝试使用随机端口..."
    # 修改run.py中的端口号为随机端口
    RANDOM_PORT=$((8000 + RANDOM % 2000))
    echo "将使用端口: $RANDOM_PORT"
    sed -i "s/port=5166/port=$RANDOM_PORT/g" run.py
fi

# 启动应用
python3 run.py

echo
echo "服务已停止。" 