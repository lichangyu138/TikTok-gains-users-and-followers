# TikTok链接验证工具

这是一个用于验证TikTok账号链接的工具，可以提取账号的用户名和粉丝数量信息。

## 功能特点

- 验证TikTok账号链接的有效性
- 提取TikTok账号的用户名和粉丝数量
- 支持批量测试多个TikTok链接
- 详细的HTML分析和调试信息

## 系统要求

- Python 3.6+
- 安装requirements.txt中的依赖包

## 快速开始

### Windows系统

1. 正常启动（Web服务模式）:
   ```
   start.bat
   ```

2. 测试模式:
   ```
   test.bat
   ```

### Linux/Mac系统

1. 首先给脚本添加执行权限:
   ```bash
   chmod +x start.sh test.sh
   ```

2. 正常启动（Web服务模式）:
   ```bash
   ./start.sh
   ```

3. 测试模式:
   ```bash
   ./test.sh
   ```

### 在服务器上部署

如果在服务器（如宝塔）上部署，请遵循以下步骤：

1. 上传项目文件到服务器
2. 安装依赖：`pip install -r requirements.txt`
3. 设置环境变量：`export SERVER_ENVIRONMENT=production`
4. 启动应用：`python run.py`
5. 访问API：`http://服务器IP:5166/api/validate`
6. 也可以直接访问：`http://服务器IP:5166/` 查看API文档或前端页面

## 使用方法

### Web服务模式

启动Web服务后，访问浏览器中打开的前端页面，输入TikTok账号链接进行验证。

### API使用方法

向 `/api/validate` 端点发送POST请求，格式为：

```json
{
  "urls": [
    "https://www.tiktok.com/@用户名1",
    "https://www.tiktok.com/@用户名2"
  ]
}
```

返回结果格式：

```json
{
  "results": [
    {
      "url": "TikTok链接",
      "valid": true/false,
      "username": "用户名",
      "followers": "粉丝数",
      "message": "处理结果消息"
    }
  ]
}
```

### 测试模式

测试模式将对预设的几个TikTok账号链接进行测试，验证工具的功能。

也可以手动指定测试链接:
```bash
# Windows
python run.py --test https://www.tiktok.com/@nasa

# Linux/Mac
python3 run.py --test https://www.tiktok.com/@nasa
```

## 服务端口

默认情况下，服务运行在5166端口。如需修改，请编辑run.py文件中的相应配置。

## 常见问题

- **404错误**：确保访问正确的URL，直接访问 `/` 会显示API文档或前端页面
- **端口冲突**：如果5166端口被占用，可以编辑run.py文件修改端口号
- **在服务器上无法打开前端页面**：尝试直接访问 `http://服务器IP:5166/` 查看API文档

### 问题排查指南

#### 验证失败：Failed to fetch

这个错误通常表示前端无法连接到后端API。可能的原因和解决方法：

1. **后端服务未运行**
   - 检查后端服务是否正在运行：`ps aux | grep python`
   - 重新启动后端服务：`python run.py`

2. **网络连接问题**
   - 使用测试脚本确认API是否可访问：`python test_api.py`
   - 确认API服务器IP和端口是否正确

3. **跨域(CORS)问题**
   - 如果使用本地文件（file://协议）打开前端，浏览器可能会阻止跨域请求
   - 解决方法：通过HTTP服务器提供前端文件，或使用浏览器插件禁用CORS限制

4. **API地址配置错误**
   - 确认前端中API地址配置正确，最新版本会自动检测环境
   - 如果手动部署，可以在浏览器控制台中查看实际请求地址

5. **防火墙或网络限制**
   - 确认服务器防火墙允许5166端口的访问
   - 在宝塔面板中，确认安全组设置允许该端口

#### 测试API连接

可以使用以下命令测试API连接：

```bash
# 测试API健康状态
python test_api.py --url http://服务器IP:5166

# 使用具体的TikTok URL测试验证功能
python test_api.py --url http://服务器IP:5166 --test https://www.tiktok.com/@tiktok
```

如果测试成功但前端仍无法连接，可能是前端配置问题，请检查浏览器控制台中的网络请求。 