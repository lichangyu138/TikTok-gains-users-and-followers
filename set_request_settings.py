import requests
import json
import sys
import argparse

def set_request_settings(settings=None):
    """设置TikTok验证服务的请求设置"""
    try:
        url = "http://localhost:5166/api/request_settings"
        
        # 首先获取当前配置
        response = requests.get(url)
        if response.status_code == 200:
            current = response.json()
            print("当前请求设置:")
            for key, value in current.items():
                print(f"  {key}: {value}")
        else:
            print(f"获取当前配置失败: HTTP状态码 {response.status_code}")
            return
        
        # 如果没有提供设置，只显示当前设置
        if not settings:
            return
        
        # 设置新的配置
        response = requests.post(url, json=settings)
        
        if response.status_code == 200:
            result = response.json()
            print(f"\n请求设置调整成功!")
            print("已更新的设置:")
            for key, value in result.get('updated_settings', {}).items():
                print(f"  {key}: {current.get(key)} -> {value}")
        else:
            print(f"\n请求设置调整失败: HTTP状态码 {response.status_code}")
            if response.text:
                print(response.text)
    except Exception as e:
        print(f"操作过程中出错: {e}")

def main():
    parser = argparse.ArgumentParser(description="TikTok验证服务请求设置管理工具")
    
    # 添加所有可能的设置参数
    parser.add_argument("--min_delay", type=float, help="最小请求延迟(秒)")
    parser.add_argument("--max_delay", type=float, help="最大请求延迟(秒)")
    parser.add_argument("--batch_interval", type=int, help="每多少个请求暂停一次")
    parser.add_argument("--batch_pause", type=float, help="批次间暂停时间(秒)")
    parser.add_argument("--conn_timeout", type=float, help="连接超时(秒)")
    parser.add_argument("--read_timeout", type=float, help="读取超时(秒)")
    parser.add_argument("--max_retries", type=int, help="最大重试次数")
    parser.add_argument("--retry_factor", type=float, help="重试延迟因子")
    
    # 添加简易模式切换
    parser.add_argument("--mode", choices=["fast", "normal", "safe"], 
                       help="预设模式: fast(快速)、normal(正常)、safe(安全)")
    
    args = parser.parse_args()
    
    # 预设模式
    if args.mode:
        if args.mode == "fast":
            settings = {
                "min_request_delay": 0.2,
                "max_request_delay": 0.5,
                "batch_interval": 15,
                "batch_pause": 1.0,
                "connection_timeout": 10,
                "read_timeout": 15,
                "max_retries": 2,
                "retry_delay_factor": 1.5
            }
            print("使用快速模式配置 - 高速率，最低延迟")
        elif args.mode == "normal":
            settings = {
                "min_request_delay": 0.5,
                "max_request_delay": 2.0,
                "batch_interval": 10,
                "batch_pause": 2.0,
                "connection_timeout": 20,
                "read_timeout": 30,
                "max_retries": 3,
                "retry_delay_factor": 2.0
            }
            print("使用正常模式配置 - 平衡速度和稳定性")
        elif args.mode == "safe":
            settings = {
                "min_request_delay": 1.0,
                "max_request_delay": 3.0,
                "batch_interval": 5,
                "batch_pause": 3.0,
                "connection_timeout": 30,
                "read_timeout": 45,
                "max_retries": 4,
                "retry_delay_factor": 2.5
            }
            print("使用安全模式配置 - 稳定性优先，降低速率")
        
        set_request_settings(settings)
        return
    
    # 收集所有设置
    settings = {}
    
    if args.min_delay is not None:
        settings["min_request_delay"] = args.min_delay
    
    if args.max_delay is not None:
        settings["max_request_delay"] = args.max_delay
    
    if args.batch_interval is not None:
        settings["batch_interval"] = args.batch_interval
    
    if args.batch_pause is not None:
        settings["batch_pause"] = args.batch_pause
    
    if args.conn_timeout is not None:
        settings["connection_timeout"] = args.conn_timeout
    
    if args.read_timeout is not None:
        settings["read_timeout"] = args.read_timeout
    
    if args.max_retries is not None:
        settings["max_retries"] = args.max_retries
    
    if args.retry_factor is not None:
        settings["retry_delay_factor"] = args.retry_factor
    
    # 检查是否有任何设置被修改
    if not settings:
        print("没有指定任何设置。使用 --help 查看可用选项。")
        set_request_settings()  # 只显示当前设置
    else:
        set_request_settings(settings)

if __name__ == "__main__":
    main() 