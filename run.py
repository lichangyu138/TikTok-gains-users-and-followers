import sys
import os
import webbrowser
import time
import argparse
import json
import re
from threading import Thread
from backend.app import validate_tiktok_url, app

def start_backend():
    """启动后端Flask服务"""
    # 将backend目录添加到路径
    backend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend')
    sys.path.insert(0, backend_dir)
    
    # 导入app并运行
    app.run(host='0.0.0.0', port=5166, debug=True, use_reloader=False)

def open_frontend():
    """打开前端页面"""
    # 等待后端启动
    time.sleep(2)
    
    # 获取前端HTML文件的绝对路径
    frontend_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'frontend', 'index.html')
    
    # 在服务器环境中，不要尝试打开浏览器
    if os.environ.get('SERVER_ENVIRONMENT') == 'production':
        print(f"前端页面位于: {frontend_path}")
        print(f"请访问: http://服务器IP:5166/api/validate 来使用API")
    else:
        # 本地开发环境，打开浏览器
        frontend_url = 'file://' + os.path.normpath(frontend_path)
        webbrowser.open(frontend_url)

def test_tiktok_crawler(urls):
    """
    测试TikTok爬虫功能
    """
    print("=" * 50)
    print("TikTok爬虫测试")
    print("=" * 50)
    print()
    
    results = []
    valid_count = 0
    success_count = 0
    
    for i, url in enumerate(urls):
        print(f"[测试 {i+1}/{len(urls)}] URL: {url}")
        print("-" * 40)
        
        # 验证URL (在测试模式下保留调试文件)
        result = validate_tiktok_url(url, keep_debug_file=True)
        results.append(result)
        
        # 打印结果
        print(f"结果: {json.dumps(result, indent=2, ensure_ascii=False)}")
        
        # 统计有效URL和成功提取信息的URL
        if result.get('valid'):
            valid_count += 1
            if result.get('username') != 'Unknown' and result.get('followers') != 'Unknown':
                success_count += 1
        
        # 如果是失败的URL，分析一下HTML内容
        if not result.get('valid') or result.get('username') == 'Unknown' or result.get('followers') == 'Unknown':
            # 查找最新的debug文件
            debug_files = [f for f in os.listdir('.') if f.startswith('debug_tiktok_') and f.endswith('.html')]
            if debug_files:
                # 按修改时间排序，获取最新的文件
                debug_file = sorted(debug_files, key=lambda x: os.path.getmtime(x), reverse=True)[0]
                
                # 分析HTML结构
                print(f"\n分析HTML结构 (文件: {debug_file}):\n")
                
                # 读取HTML内容
                with open(debug_file, 'r', encoding='utf-8') as f:
                    html_content = f.read()
                
                # 1. 检查用户名元素
                print("1. 检查用户名元素:")
                if '<h1 data-e2e="user-title">' in html_content:
                    user_title = re.search(r'<h1 data-e2e="user-title">(.*?)</h1>', html_content)
                    if user_title:
                        print(f"   ✓ 找到用户名元素: {user_title.group(1)}")
                    else:
                        print("   ✗ 找到用户名元素标签，但无法提取内容")
                else:
                    print("   ✗ 未找到用户名元素 (data-e2e='user-title')")
                    print("   尝试查找其他可能包含用户名的元素:")
                
                # 2. 检查粉丝数元素
                print("\n2. 检查粉丝数元素:")
                if '<strong data-e2e="followers-count">' in html_content:
                    followers_count = re.search(r'<strong data-e2e="followers-count">(.*?)</strong>', html_content)
                    if followers_count:
                        print(f"   ✓ 找到粉丝数元素: {followers_count.group(1)}")
                    else:
                        print("   ✗ 找到粉丝数元素标签，但无法提取内容")
                else:
                    print("   ✗ 未找到粉丝数元素 (data-e2e='followers-count')")
                    print("   尝试查找其他可能包含粉丝数的元素:")
                
                # 3. 检查是否有账号不存在的提示
                print("\n3. 页面类型分析:")
                if "Couldn't find this account" in html_content or "Account Not Found" in html_content:
                    print("   ✗ 页面显示账号不存在")
                else:
                    print("   ✓ 页面未显示账号不存在")
                
                # 4. 查找页面中所有data-e2e属性
                print("\n4. 页面中所有data-e2e属性:")
                data_e2e_attrs = re.findall(r'data-e2e="([^"]+)"', html_content)
                if data_e2e_attrs:
                    unique_attrs = set(data_e2e_attrs)
                    for attr in sorted(unique_attrs):
                        print(f"   - {attr}")
                else:
                    print("   未找到任何data-e2e属性")
                    
                # 5. 检查是否有JSON数据
                print("\n5. 页面中的JSON数据:")
                json_data_matches = re.findall(r'"uniqueId":"([^"]+)","nickname":"([^"]+)"', html_content)
                if json_data_matches:
                    for match in json_data_matches:
                        print(f"   - uniqueId: {match[0]}, nickname: {match[1]}")
                else:
                    print("   未找到包含用户信息的JSON数据")
        
        print()
    
    # 统计结果
    print("=" * 50)
    print("测试汇总")
    print("=" * 50)
    print(f"总共URL: {len(urls)}")
    print(f"有效URL: {valid_count} ({valid_count/len(urls)*100:.1f}%)")
    print(f"成功提取用户信息: {success_count} ({success_count/len(urls)*100:.1f}%)")
    
    # 显示失败项详情
    if len(urls) - success_count > 0:
        print("\n失败项详情:")
        for i, result in enumerate(results):
            if not result.get('valid') or result.get('username') == 'Unknown' or result.get('followers') == 'Unknown':
                print(f"{i+1}. {result.get('url')} - {result.get('message')}")

def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description='TikTok链接验证工具')
    parser.add_argument('--test', action='store_true', help='运行测试模式')
    parser.add_argument('urls', nargs='*', help='要测试的TikTok URL列表')
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    
    if args.test:
        # 运行测试模式
        print("运行TikTok链接验证测试...")
        
        # 如果提供了URL参数，使用这些URL进行测试
        if args.urls:
            urls = args.urls
        else:
            # 否则使用预设的测试URL
            urls = [
                "https://www.tiktok.com/@tiktok",
                "https://www.tiktok.com/@chmohammadsarwar",
                "https://www.tiktok.com/@this_account_definitely_does_not_exist_1234567890",
                "https://www.tiktok.com/@teamtaunsa"
            ]
        
        test_tiktok_crawler(urls)
    else:
        # 运行Web服务模式
        print("启动TikTok链接验证工具...")
        
        # 启动后端服务
        backend_thread = Thread(target=start_backend)
        backend_thread.daemon = True
        backend_thread.start()
        
        # 打开前端页面
        open_frontend()
        
        print("后端服务已启动，按Ctrl+C停止...")
        try:
            # 保持主线程运行
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("停止服务...")
            sys.exit(0) 