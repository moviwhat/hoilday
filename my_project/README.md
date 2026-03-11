# My Project

一个基于Flask的Web应用项目

## 项目结构

```
my_project/
├── app.py                      # Flask应用主文件
├── config.py                   # 配置文件
├── requirements.txt            # Python依赖
├── config/                     # 数据配置目录
│   └── data.json               # 照片数据配置
├── templates/                  # HTML模板
│   └── index.html
├── static/                     # 静态资源
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
└── services/                   # 服务层
    ├── __init__.py
    ├── api_service.py          # API调用服务
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

- `FLASK_DEBUG`: 调试模式 (默认: True)
- `SECRET_KEY`: Flask密钥
- `API_BASE_URL`: 外部API基础URL
- `API_TIMEOUT`: API请求超时时间 (默认: 30秒)
- `MAX_CONCURRENT_REQUESTS`: 最大并发请求数 (默认: 5)
- `DATA_CONFIG_PATH`: 数据配置文件路径 (默认: config/data.json)

## API接口

### 并发请求
- **URL**: `/api/concurrent`
- **方法**: POST
- **说明**: 并发发送多个API请求，从配置文件读取数据项
- **并发控制**: 最大并发数由 `MAX_CONCURRENT_REQUESTS` 配置

## 配置文件格式

配置文件为JSON格式，包含M个数据项，每个数据项包含N组照片。

### 文件位置
`config/data.json`

### JSON格式定义

```json
{
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
- `data`: 数据项数组（M个数据项）

**数据项 (data数组中的对象)**
- `id`: 数据项唯一标识（整数）
- `text`: 默认文案（字符串）
- `photos`: 照片数组（N组照片）

**照片对象 (photos数组中的对象)**
- `id`: 照片唯一标识（整数）
- `url`: 照片本地文件路径（字符串）

### 示例

```json
{
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
