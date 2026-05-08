# AI 文案评测对比系统

一个基于 Flask 的 Web 应用项目，用于批量处理图片文案，支持并发调用外部 API 生成文案，并可将结果导出为 Excel 文件。

## 功能特性

- 📊 **批量处理**: 支持批量处理多个数据项，每个数据项可包含多张图片
- 🚀 **并发请求**: 使用异步并发请求，提高处理效率
- 🎨 **文风选择**: 支持多种文风选择（文艺、网红、叙事、自定义）
- 📝 **自定义提示词**: 支持用户自定义提示词和系统提示词
- 📈 **进度跟踪**: 实时显示处理进度和统计信息
- 📥 **Excel 导出**: 支持将结果导出为 Excel 文件，图片直接嵌入单元格
- 🖼️ **图片预览**: 支持本地图片的在线预览

## 技术栈

- **后端**: Flask 3.0.0
- **前端**: HTML5 + CSS3 + JavaScript (ES6+)
- **异步处理**: asyncio + aiohttp
- **Excel 生成**: openpyxl 3.1.2
- **图片处理**: Pillow 12.1.1
- **HTTP 客户端**: requests 2.31.0

## 项目结构

```
my_project/
├── app.py                      # Flask 应用主文件（路由和业务逻辑）
├── config.py                   # 配置文件（环境变量和常量）
├── requirements.txt            # Python 依赖列表
├── .venv/                      # Python 虚拟环境
├── config/                     # 数据配置目录
│   └── data.json               # 照片数据配置文件
├── templates/                  # HTML 模板目录
│   └── index.html             # 主页面模板
├── static/                     # 静态资源目录
│   ├── css/
│   │   └── style.css         # 样式文件
│   └── js/
│       └── main.js           # 前端逻辑脚本
└── services/                   # 服务层目录
    ├── __init__.py
    ├── api_service.py          # API 调用服务（封装层）
    └── concurrent_service.py   # 并发请求服务（核心逻辑）
```

## 快速开始

### 1. 激活虚拟环境（推荐）

```powershell
.venv\Scripts\Activate.ps1
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置数据文件

编辑 `config/data.json` 文件，配置你的数据项和图片路径。

### 4. 配置环境变量（可选）

Linux/Mac:
```bash
export API_BASE_URL=http://your-api-server.com/api
export API_TIMEOUT=30
export MAX_CONCURRENT_REQUESTS=5
```

Windows (PowerShell):
```powershell
$env:API_BASE_URL="http://your-api-server.com/api"
$env:API_TIMEOUT=30
$env:MAX_CONCURRENT_REQUESTS=5
```

### 5. 启动项目

```bash
python app.py
```

### 6. 访问应用

打开浏览器访问 http://localhost:5000

## 环境变量

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `FLASK_DEBUG` | 调试模式 | `True` |
| `SECRET_KEY` | Flask 密钥 | `your-secret-key-here` |
| `API_BASE_URL` | 外部 API 基础 URL | `http://example.com/api` |
| `API_TIMEOUT` | API 请求超时时间（秒） | `30` |
| `MAX_CONCURRENT_REQUESTS` | 最大并发请求数 | `5` |
| `DATA_CONFIG_PATH` | 数据配置文件路径 | `config/data.json` |

## API 接口

### 加载本地数据
- **URL**: `/api/load-data`
- **方法**: GET
- **说明**: 从本地 JSON 配置文件加载数据，用于页面初始化展示
- **返回**:
  ```json
  {
    "success": true,
    "data": [...],
    "styles": ["文艺", "网红", "叙事", "自定义"],
    "default_style": "文艺",
    "system_prompt": "..."
  }
  ```

### 并发请求
- **URL**: `/api/concurrent`
- **方法**: POST
- **请求体**:
  ```json
  {
    "userPrompt": "用户自定义提示词",
    "style": "文艺",
    "systemPrompt": "系统提示词内容"
  }
  ```
- **说明**: 并发发送多个 API 请求，从配置文件读取数据项
- **并发控制**: 最大并发数由 `MAX_CONCURRENT_REQUESTS` 配置
- **参数说明**:
  - `userPrompt`: 用户自定义提示词（可选）
  - `style`: 文风选择（来自前端下拉框）
  - `systemPrompt`: 系统提示词（可选，来自配置文件）
- **进度展示**: 实时打印请求进度，包括：
  - 总请求数
  - 已完成请求数
  - 剩余请求数
  - 平均每个请求耗时
  - 总耗时
  - 用户提示词（如果有）
  - 文风（如果有）
  - 系统提示词（如果有）
- **返回**:
  ```json
  {
    "success": true,
    "total": 2,
    "results": [
      {
        "data_id": 1,
        "success": true,
        "result": {
          "text": "原始文案",
          "photos": [{"id": 1, "url": "path/to/photo.jpg"}],
          "generated_text": "API返回的文案"
        }
      },
      {
        "data_id": 2,
        "success": false,
        "error": "错误信息",
        "result": {
          "text": "原始文案",
          "photos": []
        }
      }
    ]
  }
  ```

#### 进度输出示例
```
开始并发请求，总请求数：5, 最大并发数：3
用户提示词：请根据图片内容生成一段描述
文风：文艺
系统提示词：你是一个专业的文案生成助手
==================================================
总请求数：5
已完成：1
剩余：4
平均每个请求耗时：2.50 秒
总耗时：2.50 秒
==================================================
==================================================
总请求数：5
已完成：2
剩余：3
平均每个请求耗时：2.30 秒
总耗时：4.60 秒
==================================================
...

所有请求已完成!
==================================================
总请求数：5
总耗时：15.20 秒
平均每个请求耗时：3.04 秒
==================================================
```

### 导出 Excel
- **URL**: `/api/export-excel`
- **方法**: POST
- **请求体**:
  ```json
  {
    "results": [...]
  }
  ```
- **说明**: 生成包含图片的 Excel 文件
- **功能**:
  - 图片直接嵌入到 Excel 单元格中（80x80 像素）
  - 最多支持 5 张图片
  - 失败时显示错误信息
  - 自动设置行高和列宽以优化显示效果
- **返回**: Excel 文件流，浏览器自动下载

### 图片代理
- **URL**: `/api/photo/<path:filename>`
- **方法**: GET
- **说明**: 代理本地图片文件，解决浏览器本地文件访问限制
- **参数**: `filename` - 图片文件的完整路径
- **返回**: 图片文件流

## 使用说明

### 基本流程

1. **启动项目**: 运行 `python app.py` 启动 Web 服务
2. **访问页面**: 打开浏览器访问 http://localhost:5000
3. **页面加载**: 页面会自动加载本地 JSON 配置文件中的图片和原始文案
4. **选择文风**: 从下拉框选择文风（文艺、网红、叙事、自定义）
5. **输入提示词**: 在提示词输入框中输入自定义提示词（可选）
6. **开始处理**: 点击"开始处理"按钮，系统会并发调用外部 API
7. **查看结果**: 处理完成后，页面会显示 API 返回的文案内容
8. **导出 Excel**: 处理完成后，点击"导出 Excel"按钮可将结果导出为 Excel 文件

### 导出 Excel 格式说明

导出的 Excel 文件包含以下列：

| 列名 | 说明 |
|------|------|
| 数据项ID | 数据项的编号 |
| 状态 | 处理状态（成功/失败） |
| 图片1-图片5 | 图片直接嵌入到单元格中（80x80 像素，最多 5 张） |
| 原始文案 | JSON 配置中的原始文案 |
| 返回文案 | API 返回的生成文案（失败时显示错误信息） |

文件命名格式：`copywriting_result_YYYY-MM-DD.xlsx`

### 自定义文风

选择"自定义"文风时，会显示一个输入框，可以输入自定义的文风描述。

### 进度跟踪

处理过程中，终端会实时显示：
- 总请求数
- 已完成请求数
- 剩余请求数
- 平均每个请求耗时
- 总耗时

## 架构说明

### 后端架构

```
app.py (Flask 应用)
  ├── 路由层
  │   ├── / (首页)
  │   ├── /api/load-data (加载配置)
  │   ├── /api/concurrent (并发请求)
  │   ├── /api/export-excel (导出 Excel)
  │   └── /api/photo/<path> (图片代理)
  └── 服务层
      ├── APIService (API 调用封装)
      └── ConcurrentRequestService (并发请求核心)
```

### 前端架构

```
index.html (主页面)
  ├── 样式 (style.css)
  │   ├── 响应式布局
  │   └── 三列网格布局
  └── 脚本 (main.js)
      ├── 数据加载
      ├── 文风选择
      ├── 并发请求
      ├── 结果渲染
      └── Excel 导出
```

### 并发请求流程

```
1. 前端发送请求 → /api/concurrent
2. 后端读取配置文件
3. 创建信号量控制并发数
4. 异步发送多个 API 请求
5. 实时更新进度
6. 返回结果给前端
7. 前端渲染结果
```

## 配置文件格式

配置文件为 JSON 格式，包含全局配置和数据项。

### 文件位置
`config/data.json`

### JSON 格式定义

```json
{
  "style": ["文艺", "网红", "叙事", "自定义"],
  "default_style": "文艺",
  "system_prompt": "系统提示词内容",
  "data": [
    {
      "id": 1,
      "text": "默认文案内容",
      "photos": [
        {
          "id": 1,
          "url": "/path/to/photo1.jpg"
        },
        {
          "id": 2,
          "url": "/path/to/photo2.jpg"
        }
      ]
    },
    {
      "id": 2,
      "text": "默认文案内容",
      "photos": [
        {
          "id": 1,
          "url": "/path/to/photo3.jpg"
        }
      ]
    }
  ]
}
```

### 字段说明

**根对象**
- `style`: 文风选择数组（字符串数组），前端会动态生成下拉框
- `default_style`: 默认选中的文风（字符串）
- `system_prompt`: 系统提示词（字符串）
- `data`: 数据项数组（M 个数据项）

**数据项 (data 数组中的对象)**
- `id`: 数据项唯一标识（整数）
- `text`: 默认文案（字符串）
- `photos`: 照片数组（N 组照片）

**照片对象 (photos 数组中的对象)**
- `id`: 照片唯一标识（整数）
- `url`: 照片本地文件路径（字符串）

### 示例

```json
{
  "style": ["文艺", "网红", "叙事", "自定义"],
  "default_style": "文艺",
  "system_prompt": "你是一个专业的文案生成助手，请根据用户提供的图片和文案生成合适的推广内容。",
  "data": [
    {
      "id": 1,
      "text": "这是长城的美丽风景照片",
      "photos": [
        {
          "id": 1,
          "url": "E:/photos/great_wall_1.jpg"
        },
        {
          "id": 2,
          "url": "E:/photos/great_wall_2.jpg"
        }
      ]
    },
    {
      "id": 2,
      "text": "城市夜景照片集",
      "photos": [
        {
          "id": 1,
          "url": "E:/photos/city_night.jpg"
        }
      ]
    }
  ]
}
```

## 常见问题

### Q1: 图片无法在网页上显示？
**A**: 这是因为浏览器安全限制，不允许直接访问本地文件。系统已经实现了图片代理功能，确保：
- 图片路径在 `config/data.json` 中配置正确
- 图片文件确实存在于指定路径
- Flask 服务正常运行

### Q2: 导出的 Excel 中看不到图片？
**A**: 请检查：
- 已安装 Pillow 库：`pip install Pillow`
- 图片格式支持：PNG、JPEG、BMP、GIF、TIFF
- 图片文件没有损坏
- 使用 Excel 或 WPS 打开（某些在线编辑器可能不支持）

### Q3: 并发请求超时怎么办？
**A**: 可以调整以下配置：
- 增加 `API_TIMEOUT` 环境变量（默认 30 秒）
- 减少 `MAX_CONCURRENT_REQUESTS` 环境变量（默认 5）
- 检查外部 API 服务是否正常运行

### Q4: 如何修改最大并发数？
**A**: 设置环境变量 `MAX_CONCURRENT_REQUESTS`，例如：
```bash
export MAX_CONCURRENT_REQUESTS=10
```

### Q5: 如何自定义文风选项？
**A**: 编辑 `config/data.json` 文件，修改 `style` 数组：
```json
{
  "style": ["文艺", "网红", "叙事", "自定义", "你的文风"],
  "default_style": "文艺"
}
```

### Q6: 处理失败后如何重试？
**A**: 刷新页面重新加载数据，然后再次点击"开始处理"按钮。

## 故障排除

### 端口被占用
如果 5000 端口被占用，可以修改 `app.py` 最后一行：
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

### 依赖安装失败
如果 `pip install` 失败，尝试：
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### API 请求失败
检查：
- 外部 API 服务是否正常运行
- `API_BASE_URL` 环境变量是否配置正确
- 网络连接是否正常

## 开发说明

### 添加新的 API 接口
在 `app.py` 中添加新的路由：
```python
@app.route('/api/your-endpoint', methods=['POST'])
def your_endpoint():
    # 你的逻辑
    return jsonify({'success': True})
```

### 修改并发逻辑
编辑 `services/concurrent_service.py`，主要方法：
- `send_single_request`: 单个请求逻辑
- `send_concurrent_requests`: 并发请求逻辑
- `print_progress`: 进度打印逻辑

### 自定义前端样式
编辑 `static/css/style.css`，支持响应式布局和自定义主题。

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！
