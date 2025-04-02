import requests
import json
import sys

def set_thread_pool(new_size=24):
    try:
        url = "http://localhost:5166/api/thread_pool"
        
        # 首先获取当前配置
        response = requests.get(url)
        if response.status_code == 200:
            current = response.json()
            print(f"当前线程池配置: 最大工作线程 = {current['max_workers']}")
        else:
            print(f"获取当前配置失败: HTTP状态码 {response.status_code}")
            return
        
        # 设置新的配置
        data = {"max_workers": new_size}
        response = requests.post(url, json=data)
        
        if response.status_code == 200:
            result = response.json()
            print(f"线程池调整成功: {result['message']}")
        else:
            print(f"线程池调整失败: HTTP状态码 {response.status_code}")
            if response.text:
                print(response.text)
    except Exception as e:
        print(f"操作过程中出错: {e}")

if __name__ == "__main__":
    size = 24  # 默认设置为24线程
    
    if len(sys.argv) > 1:
        try:
            size = int(sys.argv[1])
        except ValueError:
            print(f"无效的线程数参数: {sys.argv[1]}, 使用默认值 {size}")
    
    set_thread_pool(size) 