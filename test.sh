#!/bin/bash

echo "==================================================="
echo "TikTok链接验证工具测试模式启动脚本"
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
echo "依赖安装完成，正在启动TikTok链接验证工具（测试模式）..."
echo

python3 run.py --test

echo
echo "测试已完成。" 