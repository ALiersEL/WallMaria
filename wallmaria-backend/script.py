import os
import json
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

client = AsyncIOMotorClient("mongodb://localhost:27017/")
db = client['wallmaria']
collection = db['posts']

async def read_json_files(folder_path):
    for root, dirs, files in os.walk(folder_path):
        json_data = []
        for file_name in files:
            if file_name.endswith('.json'):
                file_path = os.path.join(root, file_name)
                with open(file_path, 'r') as file:
                    data = json.load(file)
                    json_data.append(data)

        await write_json_file(json_data)
        print(f'Inserted {len(json_data)} documents')

async def write_json_file(data):
    await collection.insert_many(data)

async def delete_all_documents():
    print(await collection.delete_many({}))

folder_path = 'D:\Python\DeepLearning\CLIP-fine-tune\data\images_600'
output_file = 'D:\Python\DeepLearning\CLIP-fine-tune\data\images.json'

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
# loop.run_until_complete(delete_all_documents())
loop.run_until_complete(read_json_files(folder_path))
