import requests
import os
import time
import json

def test_validate_endpoint():
    """测试验证TikTok链接API端点"""
    print("开始测试验证TikTok链接功能...")
    
    # 测试验证端点
    validate_url = "http://localhost:5166/api/validate"
    
    # 测试数据
    test_data = {
        "urls": [
            "https://www.tiktok.com/@tiktok"
        ]
    }
    
    # 检查调试文件目录初始状态
    debug_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'debug_files')
    if os.path.exists(debug_dir):
        print(f"测试前调试文件目录: {debug_dir}")
        initial_files = os.listdir(debug_dir)
        print(f"目录中的初始文件数量: {len(initial_files)}")
    
    try:
        print(f"\n测试验证API: {validate_url}")
        print(f"测试数据: {json.dumps(test_data, ensure_ascii=False)}")
        
        response = requests.post(validate_url, json=test_data)
        print(f"状态码: {response.status_code}")
        result = response.json()
        print(f"响应内容: {json.dumps(result, ensure_ascii=False, indent=2)}")
        
        # 检查调试文件目录变化
        if os.path.exists(debug_dir):
            print(f"\n测试后调试文件目录: {debug_dir}")
            after_files = os.listdir(debug_dir)
            print(f"目录中的文件数量: {len(after_files)}")
            if after_files:
                print("文件列表:")
                for file in after_files:
                    print(f"- {file}")
        
        # 等待一下，让自动清理有时间执行
        print("\n等待3秒，检查自动清理是否工作...")
        time.sleep(3)
        
        # 再次检查目录
        if os.path.exists(debug_dir):
            final_files = os.listdir(debug_dir)
            print(f"清理后的文件数量: {len(final_files)}")
            if final_files:
                print("剩余文件列表:")
                for file in final_files:
                    print(f"- {file}")
            else:
                print("所有调试文件已成功清理！")
                
    except Exception as e:
        print(f"验证API测试失败: {str(e)}")

if __name__ == "__main__":
    test_validate_endpoint() 