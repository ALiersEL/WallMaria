# WallMaria ACG Image Search Engine

[中文](README.zh.md)

Welcome to the code repository for WallMaria, an ACG image search engine designed specifically for anime, manga, and game enthusiasts! This search engine provides an efficient and intuitive way to help users find ACG-related images on the internet.

## Features

- **Text Search**: Search for images using keywords, phrases, or descriptions.
- **Image Feature Search**: Upload an image and find similar pictures based on visual content.
- **Image Text Joint Search**: Upload an image and use keywords, phrases, or descriptions to find images related to the image.

## Quick Start

By following these simple steps, you can quickly start and run the project locally.

### Clone the repository

```sh
git clone https://github.com/ALiersEL/WallMaria.git
```

### Backend Setup

To save time, we have deployed a backend server for you to use. You can skip the backend setup and go directly to the [frontend setup](#frontend-setup). However, if you want to run the backend locally, please follow the steps below.

#### Prerequisites

- Python 3.10 or higher
- MongoDB
- Redis
- Milvus

#### Backend Installation

1. Navigate to the backend directory within the WallMaria project
   ```sh
   cd WallMaria/wallmaria-backend
   ```
2. Install the required packages
   ```sh
   pip install -r requirements.txt
   ```

#### Backend Configuration

Create a `config.json` file in the `wallmaria-backend` directory.
Ensure your services are configured according to the config.json file. An example configuration is shown below:
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
Please replace <your_password>, <your_host>, and <your_checkpoint> with your actual password, host address, and checkpoint name.

#### Run the Backend Application

1. Start the backend server
   ```sh
   uvicorn main:app --port 8000 --reload
   ```
2. Visit `http://localhost:8000` in your browser to open the web interface

### Frontend Setup

#### Prerequisites

- Node.js 14 or higher
- npm (comes with Node.js) or Yarn

#### Frontend Installation

1. Navigate to the frontend directory within the WallMaria project
   ```sh
   cd WallMaria/wallmaria-frontend
   ```
2. Install the dependencies
   ```sh
   npm install
   ```
   or if you are using Yarn
   ```sh
   yarn install
   ```

#### Frontend Configuration

The frontend application is pre-configured to connect with a deployed backend server. The default backend URL is already set in the `.env` file located in the `wallmaria-frontend` directory.

Default `.env` configuration:
```sh
VITE_APP_BACKEND_URL=http://wallrose.huox3.cn:7000
```

If you wish to use your own backend server or if you have a different URL for the backend, you can update the `VITE_APP_BACKEND_URL` environment variable in the `.env` file accordingly.

To connect to a custom backend server, modify the `.env` file with your backend server's URL:

Example for custom backend URL:
```sh
VITE_APP_BACKEND_URL=http://localhost:8000
```

After updating the `.env` file, restart the frontend server to apply the changes.

#### Run the Frontend Application

1. Serve the application with hot reload at localhost
   ```sh
   npm run serve
   ```
   or if you are using Yarn
   ```sh
   yarn serve
   ```

2. Open `http://localhost:5173` in your web browser to view and interact with the frontend.(You can change the port in the `vite.config.ts` file.)

#### Building for Production

To build the frontend for production, use the build script. This will create a `dist` folder with all the files optimized for deployment.

```sh
npm run build
```
or if you are using Yarn
```sh
yarn build
```

After building, you can deploy the `dist` folder to any static file server or frontend hosting service.

## Roadmap

For planned features and known issues, see the [open issues](https://github.com/ALiersEL/WallMaria/issues).

## Contribution

The contributions of the open-source community make it an excellent place to learn, inspire, and create. Any contributions you make are greatly appreciated.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License. For more information, please see the `LICENSE` file.

## Acknowledgments

- [CLIP](https://github.com/openai/clip)
- [GradCache](https://github.com/luyug/GradCache)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Vue.js](https://vuejs.org/)
- [Tailwind CSS](https://tailwindcss.com/)
- [Milvus](https://milvus.io/)
- [MongoDB](https://www.mongodb.com/)
- [Redis](https://redis.io/)
