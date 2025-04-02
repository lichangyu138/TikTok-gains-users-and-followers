import requests
import json
import time
import sys
import random

def test_high_concurrency(url_count=100):
    """测试高并发性能"""
    print(f"===== 多线程高并发性能测试 =====")
    
    # 首先检查系统状态
    try:
        response = requests.get("http://localhost:5166/api/system_status")
        if response.status_code == 200:
            status = response.json()
            print(f"系统状态:")
            print(f"  CPU: {status['cpu']['physical_cores']} 物理核心, {status['cpu']['logical_cores']} 逻辑线程")
            print(f"  当前CPU使用率: {status['cpu']['average_usage']:.1f}%")
            print(f"  内存: 总计 {status['memory']['total'] / (1024**3):.1f}GB, 已用 {status['memory']['percent']:.1f}%")
            print(f"  线程池: 最大 {status['threads']['max_workers']}, 当前活跃 {status['threads']['active_threads']}")
            print()
        else:
            print(f"无法获取系统状态: {response.status_code}")
    except Exception as e:
        print(f"检查系统状态时出错: {e}")
    
    # 生成测试URL
    popular_tiktok_accounts = [
        "tiktok", "charlidamelio", "khaby.lame", "bellapoarch", "addisonre", 
        "lorengray", "zachking", "spencerx", "justinbieber", "willsmith", 
        "bts.official", "kimberly.loaiza", "jlo", "selenagomez", "kylie",
        "nike", "chipotle", "nba", "houseofhighlights", "espn"
    ]
    
    # 随机选择账号并生成足够数量的URL
    test_urls = []
    for _ in range(url_count):
        account = random.choice(popular_tiktok_accounts)
        test_urls.append(f"https://www.tiktok.com/@{account}")
    
    print(f"准备测试 {len(test_urls)} 个URL")
    print(f"前10个URL样本:")
    for i in range(min(10, len(test_urls))):
        print(f"  {i+1}. {test_urls[i]}")
    print()
    
    # 创建测试数据
    test_data = {"urls": test_urls}
    
    # 执行测试
    print("开始并发测试...")
    start_time = time.time()
    
    try:
        response = requests.post(
            "http://localhost:5166/api/validate", 
            json=test_data,
            timeout=600  # 设置10分钟超时
        )
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        
        if response.status_code == 200:
            result = response.json()
            
            print(f"\n测试完成！总耗时: {elapsed_time:.2f}秒")
            
            if "meta" in result:
                meta = result["meta"]
                print(f"服务器处理时间: {meta.get('process_time', 'N/A')}秒")
                print(f"平均处理速度: {meta.get('urls_per_second', 'N/A')} URL/秒")
                print(f"线程池信息: 最大配置 {meta.get('thread_stats', {}).get('max_workers', 'N/A')}, "
                      f"最大使用 {meta.get('thread_stats', {}).get('max_used', 'N/A')}")
            
            if "results" in result and isinstance(result["results"], list):
                valid_count = sum(1 for r in result["results"] if r.get("valid"))
                print(f"有效URL: {valid_count}/{len(result['results'])} ({valid_count/len(result['results'])*100:.1f}%)")
        else:
            print(f"测试失败: HTTP状态码 {response.status_code}")
            print(response.text)
    
    except Exception as e:
        print(f"测试过程中出错: {e}")
    
    # 最后再次检查系统状态
    try:
        response = requests.get("http://localhost:5166/api/system_status")
        if response.status_code == 200:
            status = response.json()
            print(f"\n测试后系统状态:")
            print(f"  CPU使用率: {status['cpu']['average_usage']:.1f}%")
            print(f"  内存使用率: {status['memory']['percent']:.1f}%")
            print(f"  线程池状态: 最大 {status['threads']['max_workers']}, 当前活跃 {status['threads']['active_threads']}")
        else:
            print(f"无法获取测试后系统状态: {response.status_code}")
    except Exception as e:
        print(f"检查测试后系统状态时出错: {e}")

if __name__ == "__main__":
    # 获取命令行参数
    url_count = 20  # 默认测试20个URL
    
    if len(sys.argv) > 1:
        try:
            url_count = int(sys.argv[1])
        except ValueError:
            print(f"无效的URL数量参数: {sys.argv[1]}, 使用默认值 {url_count}")
    
    test_high_concurrency(url_count) 