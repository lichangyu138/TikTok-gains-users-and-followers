#!/usr/bin/env python3
"""
TikTok验证API测试脚本
用于检查API服务是否正常运行及诊断连接问题
"""

import requests
import json
import sys
import argparse

def test_api(base_url, endpoint='/api/health'):
    """测试API端点是否可访问"""
    url = f"{base_url}{endpoint}"
    print(f"测试API: {url}")
    
    try:
        response = requests.get(url, timeout=5)
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            print("成功! API正常运行")
            try:
                data = response.json()
                print(f"响应数据: {json.dumps(data, indent=2, ensure_ascii=False)}")
            except:
                print(f"响应内容: {response.text[:200]}...")
            return True
        else:
            print(f"错误: API返回非200状态码")
            try:
                data = response.json()
                print(f"错误信息: {json.dumps(data, indent=2, ensure_ascii=False)}")
            except:
                print(f"响应内容: {response.text[:200]}...")
            return False
    except requests.exceptions.ConnectionError:
        print(f"连接错误: 无法连接到 {url}")
        print("可能原因:")
        print("1. API服务未运行")
        print("2. 网络连接问题")
        print("3. 端口被防火墙阻止")
        print("4. URL或端口错误")
    except requests.exceptions.Timeout:
        print(f"超时错误: 连接到 {url} 超时")
    except Exception as e:
        print(f"其他错误: {str(e)}")
    
    return False

def test_validate_api(base_url, test_url="https://www.tiktok.com/@tiktok"):
    """测试验证接口"""
    url = f"{base_url}/api/validate"
    print(f"\n测试验证API: {url}")
    print(f"使用测试URL: {test_url}")
    
    try:
        response = requests.post(
            url, 
            json={"urls": [test_url]},
            headers={"Content-Type": "application/json"},
            timeout=15
        )
        
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            print("成功! 验证API正常运行")
            try:
                data = response.json()
                print(f"响应数据: {json.dumps(data, indent=2, ensure_ascii=False)}")
                return True
            except:
                print(f"响应内容不是有效的JSON: {response.text[:200]}...")
        else:
            print(f"错误: API返回非200状态码")
            try:
                data = response.json()
                print(f"错误信息: {json.dumps(data, indent=2, ensure_ascii=False)}")
            except:
                print(f"响应内容: {response.text[:200]}...")
    except Exception as e:
        print(f"请求错误: {str(e)}")
    
    return False

def check_network():
    """检查网络连接"""
    print("\n检查网络连接...")
    
    try:
        response = requests.get("https://www.baidu.com", timeout=5)
        if response.status_code == 200:
            print("网络连接正常 (可以访问百度)")
        else:
            print(f"可以连接到百度，但返回状态码 {response.status_code}")
    except Exception as e:
        print(f"无法连接到百度: {str(e)}")
        print("网络连接可能有问题")

def main():
    parser = argparse.ArgumentParser(description='测试TikTok验证API服务')
    parser.add_argument('--url', '-u', default='http://localhost:5166', 
                        help='API服务的基础URL，默认为 http://localhost:5166')
    parser.add_argument('--test', '-t', default='https://www.tiktok.com/@tiktok',
                        help='用于测试的TikTok URL，默认为 https://www.tiktok.com/@tiktok')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("TikTok验证API测试工具")
    print("=" * 60)
    
    # 测试健康检查API
    health_ok = test_api(args.url)
    
    # 测试验证API
    if health_ok:
        validate_ok = test_validate_api(args.url, args.test)
    else:
        check_network()
    
    print("\n测试完成!")

if __name__ == "__main__":
    main() 