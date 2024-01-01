import json
import pymongo
from pymongo import MongoClient
from tqdm import tqdm

class CustomDataset:
    def __init__(self, index_path):
        with open(index_path, 'r') as f:
            self.index_data = json.load(f)
        self.prefix = self.index_data["prefix"]
        self.pairs = self.index_data["pairs"]

    def __len__(self):
        return len(self.pairs)

    def batch_generator(self, batch_size=1000):
        for i in tqdm(range(0, len(self), batch_size)):
            yield [self._load_json(idx) for idx in self.pairs[i:i + batch_size]]

    def _load_json(self, idx):
        pair_path = self.prefix + idx
        json_path = pair_path + ".json"
        with open(json_path, 'r') as f:
            return json.load(f)

def batch_insert_to_mongodb(batch_data):
    client = MongoClient('mongodb://localhost:27017/')
    db = client['wallmaria']
    collection = db['posts']
    
    try:
        collection.insert_many(batch_data, ordered=False)
    except pymongo.errors.BulkWriteError as e:
        # 处理除唯一键重复之外的其他错误
        for error in e.details['writeErrors']:
            if error['code'] != 11000:  # 11000 是 MongoDB 的唯一键重复错误代码
                print(f"Error: {error['errmsg']}")

dataset = CustomDataset('/home/yhzx/桌面/WallMaria/data/dataset_index_absolute.json')
for batch in dataset.batch_generator():
    batch_insert_to_mongodb(batch)