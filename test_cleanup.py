import requests
import os
import time

def test_cleanup_endpoint():
    """测试清理调试文件的API端点"""
    print("开始测试清理调试文件功能...")
    
    # 测试健康检查端点
    health_url = "http://localhost:5166/api/health"
    try:
        print(f"测试健康检查API: {health_url}")
        response = requests.get(health_url)
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {response.json()}")
    except Exception as e:
        print(f"健康检查API测试失败: {str(e)}")
    
    # 测试清理端点
    cleanup_url = "http://localhost:5166/api/cleanup"
    try:
        print(f"\n测试清理API: {cleanup_url}")
        response = requests.get(cleanup_url)
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {response.json()}")
    except Exception as e:
        print(f"清理API测试失败: {str(e)}")
    
    # 检查调试文件目录是否存在
    debug_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'debug_files')
    if os.path.exists(debug_dir):
        print(f"\n调试文件目录存在: {debug_dir}")
        files = os.listdir(debug_dir)
        print(f"目录中的文件数量: {len(files)}")
        if files:
            print("文件列表:")
            for file in files:
                print(f"- {file}")
    else:
        print(f"\n调试文件目录不存在: {debug_dir}")

if __name__ == "__main__":
    test_cleanup_endpoint() 