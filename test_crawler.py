#!/usr/bin/env python
import sys
import os
import json
import re
from backend.app import validate_tiktok_url

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
        
        # 验证URL
        result = validate_tiktok_url(url)
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

if __name__ == "__main__":
    # 如果提供了URL参数，使用这些URL进行测试
    if len(sys.argv) > 1:
        urls = sys.argv[1:]
    else:
        # 否则使用预设的测试URL
        urls = [
            "https://www.tiktok.com/@tiktok",
            "https://www.tiktok.com/@chmohammadsarwar",
            "https://www.tiktok.com/@this_account_definitely_does_not_exist_1234567890",
            "https://www.tiktok.com/@teamtaunsa"
            
        ]
    
    test_tiktok_crawler(urls) 