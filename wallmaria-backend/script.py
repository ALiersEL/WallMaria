import os
import json

def read_json_files(folder_path):
    json_data = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.json'):
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, 'r') as file:
                data = json.load(file)
                json_data.append(data)
    return json_data

def write_json_file(data, output_file):
    with open(output_file, 'w') as file:
        json.dump(data, file, separators=(',', ':'))

folder_path = 'D:\Python\DeepLearning\CLIP-fine-tune\data\images_600'
output_file = 'D:\Python\DeepLearning\CLIP-fine-tune\data\images.json'

json_data = read_json_files(folder_path)
write_json_file(json_data, output_file)
