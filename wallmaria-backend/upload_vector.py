import json
from datetime import datetime
from PIL import Image

import torch
from torch.utils.data import Dataset, DataLoader
from clip.model import CLIP

from pymilvus import connections, Collection

from utils import _transform
from clip_loader import load_clip_model

class CustomDataset(Dataset):
    def __init__(self, index_path='D:\\Python\\DeepLearning\\CLIP-fine-tune\\data\\dataset_index.json', transform=_transform(224)):
        with open(index_path, 'r') as f:
            index_data = json.load(f)
        self.prefix = index_data["prefix"]
        self.pairs = index_data["pairs"]
        self.transform = transform
        print(f"Dataset loaded successfully. {len(self)} pairs found.")

    def __len__(self):
        return len(self.pairs)

    def __getitem__(self, idx):
        pair_path = self.prefix + self.pairs[idx]
        image_path = pair_path + ".jpg"
        json_path = pair_path + ".json"

        with open(json_path, 'r') as f:
            data = json.load(f)

        image = Image.open(image_path)

        if self.transform:
            image = self.transform(image)

        return image, data
    
def extract_feature_vectors(model, images, device="cuda"):
    images_input = images.to(device)
    with torch.no_grad():
        feature_vectors = model.encode_image(images_input)
    return feature_vectors.cpu().numpy()

def insert_into_milvus(collection, dataloader, model):
    for images, datas in dataloader:
        feature_vectors = extract_feature_vectors(model, images)

        # Prepare data for Milvus
        to_insert = [
            [data["id"] for data in datas],
            [data["rating"] for data in datas],
            [data["score"] for data in datas],
            [int(datetime.strptime(data["created_at"], "%Y-%m-%dT%H:%M:%S.%f%z").timestamp()) for data in datas],
            feature_vectors.tolist()
        ]

        # print("Data to insert:", to_insert)

        # Insert data and log the response
        insert_response = collection.upsert(to_insert)
        print("Insert response:", insert_response)

connections.connect(
    alias='default',
    host='58.37.44.136',
    port='19530',
    user='root',
    password='Milvus',
)
collection = Collection(name="posts")
print(f"Collection {collection.name} loaded successfully. {collection.num_entities}")

# Load model and create collection
model = load_clip_model("checkpoints/latest_1219_21.pth")

def custom_collate_fn(batch):
    # Separate images and metadata
    images = [item[0] for item in batch]  # Assuming the image is the first element
    metadata = [item[1] for item in batch]  # Assuming the metadata is the second element

    # Convert list of images to a tensor
    images_tensor = torch.stack(images)

    return images_tensor, metadata

# Create DataLoader
dataset = CustomDataset()
dataloader = DataLoader(dataset, batch_size=64, shuffle=False, collate_fn=custom_collate_fn)

# Insert data into Milvus
insert_into_milvus(collection, dataloader, model)