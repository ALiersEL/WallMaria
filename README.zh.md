# WallMaria 二次元图片搜索引擎
[English](README.md)


欢迎来到WallMaria 二次元图片搜索引擎的代码仓库！本搜索引擎专为动漫、漫画和游戏爱好者定制，提供一种高效直观的方式，帮助用户在网络上查找与二次元相关的图像。

## 特性

- **文本搜索**：使用关键词、短语或描述来查找图像。
- **图像特征搜索**：上传图像并根据视觉内容找到相似的图片。
- **图像文本联合搜索**：上传图像并使用关键词、短语或描述来查找与图像相关的图像。

## 快速开始

按照以下简单步骤，您可以在本地快速启动并运行项目。

### 前提条件

- Python 3.10 或更高版本
- MongoDB
- Redis
- Milvus

### 安装

1. 克隆仓库
   ```sh
   git clone https://github.com/ALiersEL/WallMaria.git
   ```
2. 进入项目目录
   ```sh
   cd WallMaria/wallmaria-backend
   ```
3. 安装所需包
   ```sh
   pip install -r requirements.txt
   ```
4. 根据config.json文件设置环境变量或直接使用配置文件。


### 运行应用

1. 启动后端服务器
   ```sh
   uvicorn main:app --port 8000 --reload
   ```
2. 在浏览器中访问 `http://localhost:8000` 以打开Web界面

## 配置

确保根据config.json文件配置您的服务。示例配置如下所示：
```json
{
  "mongo": {
    "url": "mongodb://root:<your_password>@<your_host>:27017/",
    "database": "wallmaria"
  },
  "milvus": {
    "host": "<your_host>",
    "port": "19530",
    "user": "root",
    "password": "<your_password>"
  },
  "redis": {
    "host": "<your_host>",
    "port": "6379",
    "password": "<your_password>"
  },
  "clip": {
    "path": "checkpoints/<your_checkpoint>.pth"
  }
}
```
请将<your_password>, <your_host>和<your_checkpoint>替换为实际的密码、主机地址和检查点名称。

## 路线图

有关计划的特性和已知问题，请查看[开放问题](https://github.com/ALiersEL/WallMaria/issues)。

## 贡献

开源社区的贡献使其成为一个学习、启发和创造的绝佳场所。非常感谢您做出的任何贡献。

1. Fork项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 发起Pull Request

## 许可证

该项目采用MIT许可证。有关更多信息，请查看`LICENSE`文件。

## 致谢

- [CLIP](https://github.com/openai/clip)
- [GradCache](https://github.com/luyug/GradCache)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Vue.js](https://vuejs.org/)
- [Tailwind CSS](https://tailwindcss.com/)
- [Milvus](https://milvus.io/)
- [MongoDB](https://www.mongodb.com/)
- [Redis](https://redis.io/)
