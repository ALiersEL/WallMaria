# WallMaria 二次元图片搜索引擎

[English](README.md)


欢迎来到WallMaria 二次元图片搜索引擎的代码仓库！本搜索引擎专为动漫、漫画和游戏爱好者定制，提供一种高效直观的方式，帮助用户在网络上查找与二次元相关的图像。

## 特性

- **文本搜索**：使用关键词、短语或描述来查找图像。
- **图像特征搜索**：上传图像并根据视觉内容找到相似的图片。
- **图像文本联合搜索**：上传图像并使用关键词、短语或描述来查找与图像相关的图像。

## 快速开始

按照以下简单步骤，您可以在本地快速启动并运行项目。

### 克隆仓库

```sh
git clone https://github.com/ALiersEL/WallMaria.git
```

### 后端设置

为节省时间，我们已经为您部署了一个后端服务器供您使用。您可以跳过后端设置，直接转到[前端设置](#前端设置)。但是，如果您想在本地运行后端，请按照以下步骤操作。

#### 前提条件

- Python 3.10 或更高版本
- MongoDB
- Redis
- Milvus

#### 后端安装

1. 在WallMaria项目中导航至后端目录
   ```sh
   cd WallMaria/wallmaria-backend
   ```
2. 安装所需包
   ```sh
   pip install -r requirements.txt
   ```

#### 后端配置

在 `wallmaria-backend` 目录下创建一个 `config.json` 文件。
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

#### 运行后端应用程序

1. 启动后端服务器
   ```sh
   uvicorn main:app --port 8000 --reload
   ```
2. 在浏览器中访问 `http://localhost:8000` 以打开Web界面

### 前端设置

#### 前提条件

- Node.js 14 或更高版本
- npm（随Node.js一起提供）或 Yarn

#### 前端安装

1. 在WallMaria项目中导航至前端目录
   ```sh
   cd WallMaria/wallmaria-frontend
   ```
2. 安装依赖项
   ```sh
   npm install
   ```
   或者如果您使用Yarn
   ```sh
   yarn install
   ```

#### 前端配置

前端应用程序预配置为连接到已部署的后端服务器。默认的后端URL已经在位于 `wallmaria-frontend` 目录的 `.env` 文件中设置。

默认的 `.env` 配置：
```sh
VITE_APP_BACKEND_URL=http://wallrose.huox3.cn:7000
```

如果您希望使用自己的后端服务器，或者如果您有一个不同的后端URL，您可以相应地更新 `.env` 文件中的 `VITE_APP_BACKEND_URL` 环境变量。

要连接到自定义后端服务器，请修改 `.env` 文件中的后端服务器URL：

自定义后端URL的示例：
```sh
VITE_APP_BACKEND_URL=http://localhost:8000
```

更新 `.env` 文件后，重启前端服务器以应用更改。

#### 运行前端应用程序

1. 在localhost上提供热重载的服务
   ```sh
   npm run serve
   ```
   或者如果您使用Yarn
   ```sh
   yarn serve
   ```

2. 在您的网络浏览器中打开 `http://localhost:5173` 查看并与前端交互。（您可以在 `vite.config.ts` 文件中更改端口。）

#### 构建生产环境

要为生产环境构建前端，请使用构建脚本。这将创建一个包含所有优化用于部署的文件的 `dist` 文件夹。

```sh
npm run build
```
或者如果您使用Yarn
```sh
yarn build
```

构建完成后，您可以将 `dist` 文件夹部署到任何静态文件服务器或前端托管服务。

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
