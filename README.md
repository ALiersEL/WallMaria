# WallMaria ACG Image Search Engine
[中文](README.zh.md)

Welcome to the code repository for WallMaria, an ACG image search engine designed specifically for anime, manga, and game enthusiasts! This search engine provides an efficient and intuitive way to help users find ACG-related images on the internet.

## Features

- **Text Search**: Search for images using keywords, phrases, or descriptions.
- **Image Feature Search**: Upload an image and find similar pictures based on visual content.
- **Image Text Joint Search**: Upload an image and use keywords, phrases, or descriptions to find images related to the image.

## Quick Start

By following these simple steps, you can quickly start and run the project locally.

### Prerequisites

- Python 3.10 or higher
- MongoDB
- Redis
- Milvus

### Installation

1. Clone the repository
   ```sh
   git clone https://github.com/ALiersEL/WallMaria.git
   ```
2. Enter the project directory
   ```sh
   cd WallMaria/wallmaria-backend
   ```
3. Install the required packages
   ```sh
   pip install -r requirements.txt
   ```
4. Set environment variables according to the config.json file or use the configuration file directly.


### Run the Application

1. Start the backend server
   ```sh
   uvicorn main:app --port 8000 --reload
   ```
2. Visit `http://localhost:8000` in your browser to open the web interface

## Configuration

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
