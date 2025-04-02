import requests
import json
import time

def test_multi_urls():
    """测试多URL并发处理功能"""
    print("开始测试多URL并发处理...")
    
    # 测试URL列表
    test_urls = [
        "https://www.tiktok.com/@tiktok",
        "https://www.tiktok.com/@charlidamelio",
        "https://www.tiktok.com/@khaby.lame",
        "https://www.tiktok.com/@zachking",
        "https://www.tiktok.com/@bellapoarch",
        "https://www.tiktok.com/@willsmith",
        "https://www.tiktok.com/@addisonre",
        "https://www.tiktok.com/@spencerx"
    ]
    
    # 测试数据
    test_data = {
        "urls": test_urls
    }
    
    # API URL
    api_url = "http://localhost:5166/api/validate"
    
    print(f"将测试 {len(test_urls)} 个URL的并发处理")
    print("URL列表:")
    for i, url in enumerate(test_urls):
        print(f"  {i+1}. {url}")
    
    print("\n正在发送请求...")
    start_time = time.time()
    
    try:
        response = requests.post(api_url, json=test_data)
        
        end_time = time.time()
        total_time = end_time - start_time
        
        print(f"\n请求完成，总耗时: {total_time:.2f} 秒")
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            
            print("\n处理结果摘要:")
            if "meta" in result:
                meta = result["meta"]
                print(f"- 总URL数: {meta.get('total_urls')}")
                print(f"- 处理时间: {meta.get('process_time')} 秒")
                print(f"- 每秒处理速度: {meta.get('urls_per_second')} URLs/秒")
                print(f"- 请求ID: {meta.get('request_id')}")
            
            print("\n各URL处理结果:")
            if "results" in result and isinstance(result["results"], list):
                valid_count = sum(1 for r in result["results"] if r.get("valid"))
                
                print(f"- 有效URL数: {valid_count}/{len(result['results'])}")
                
                for i, r in enumerate(result["results"]):
                    status = "✓" if r.get("valid") else "✗"
                    print(f"  {i+1}. {status} {r.get('url')} - {r.get('username')} ({r.get('followers')})")
        else:
            print(f"请求失败: {response.text}")
    
    except Exception as e:
        print(f"测试过程中出错: {str(e)}")

if __name__ == "__main__":
    test_multi_urls() 