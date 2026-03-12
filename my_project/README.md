# My Project

一个基于 Flask 的 Web 应用项目

## 项目结构

```
my_project/
├── app.py                      # Flask 应用主文件
├── config.py                   # 配置文件
├── requirements.txt            # Python 依赖
├── config/                     # 数据配置目录
│   └── data.json               # 照片数据配置
├── templates/                  # HTML 模板
│   └── index.html
├── static/                     # 静态资源
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
└── services/                   # 服务层
    ├── __init__.py
    ├── api_service.py          # API 调用服务
    └── concurrent_service.py   # 并发请求服务
```

## 安装依赖

```bash
pip install -r requirements.txt
```

## 运行项目

```bash
python app.py
```

访问 http://localhost:5000

## 环境变量

- `FLASK_DEBUG`: 调试模式 (默认：True)
- `SECRET_KEY`: Flask 密钥
- `API_BASE_URL`: 外部 API 基础 URL
- `API_TIMEOUT`: API 请求超时时间 (默认：30 秒)
- `MAX_CONCURRENT_REQUESTS`: 最大并发请求数 (默认：5)
- `DATA_CONFIG_PATH`: 数据配置文件路径 (默认：config/data.json)

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

## 使用说明

1. **启动项目**: 运行 `python app.py` 启动 Web 服务
2. **访问页面**: 打开浏览器访问 http://localhost:5000
3. **页面加载**: 页面会自动加载本地 JSON 配置文件中的图片和原始文案
4. **输入提示词**: 在提示词输入框中输入自定义提示词（可选）
5. **开始处理**: 点击"开始处理"按钮，系统会并发调用外部 API
6. **查看结果**: 处理完成后，页面会显示 API 返回的文案内容

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
