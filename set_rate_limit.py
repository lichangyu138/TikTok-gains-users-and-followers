import requests
import json
import sys

def set_rate_limit(new_rate=20):
    """设置TikTok验证服务的请求速率限制"""
    try:
        url = "http://localhost:5166/api/rate_limit"
        
        # 首先获取当前配置
        response = requests.get(url)
        if response.status_code == 200:
            current = response.json()
            print(f"当前速率限制: 每分钟 {current['max_requests_per_minute']} 请求")
            print(f"当前活跃请求数: {current['current_requests_count']}")
        else:
            print(f"获取当前配置失败: HTTP状态码 {response.status_code}")
            return
        
        # 设置新的速率限制
        data = {"max_requests_per_minute": new_rate}
        response = requests.post(url, json=data)
        
        if response.status_code == 200:
            result = response.json()
            print(f"速率限制调整成功: {result['message']}")
        else:
            print(f"速率限制调整失败: HTTP状态码 {response.status_code}")
            if response.text:
                print(response.text)
    except Exception as e:
        print(f"操作过程中出错: {e}")

if __name__ == "__main__":
    rate = 20  # 默认设置为每分钟20个请求
    
    if len(sys.argv) > 1:
        try:
            rate = int(sys.argv[1])
        except ValueError:
            print(f"无效的速率参数: {sys.argv[1]}, 使用默认值 {rate}")
    
    set_rate_limit(rate) 