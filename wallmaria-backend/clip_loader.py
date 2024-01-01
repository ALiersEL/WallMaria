import torch
import clip.model

def load_clip_model(checkpoint_path="checkpoints/latest.pth", device="cuda") -> clip.model.CLIP:
    """
    加载并返回一个预训练的 CLIP 模型。

    参数:
        checkpoint_path (str): 模型权重文件的路径。

    返回:
        model: 加载了预训练权重的 CLIP 模型。
    """

    # 加载模型和预处理工具
    model, preprocess = clip.load("ViT-L/14", device=device)

    # 加载自定义模型权重
    model.load_state_dict(torch.load(checkpoint_path, map_location=device))
    model.eval()

    return model

def extract_image_features(model, images, device="cuda"):
    """
    提取图片的特征向量。

    参数:
        model: 加载了预训练权重的 CLIP 模型。
        images (torch.Tensor): 图片的 Tensor。
        device (str): 运行模型的设备。

    返回:
        numpy.ndarray: 图片的特征向量。
    """

    images_input = torch.stack(images).to(device)
    with torch.no_grad():
        feature_vectors = model.encode_image(images_input)
    return feature_vectors.cpu().numpy()

def extract_text_features(model, texts, device="cuda"):
    """
    提取文本的特征向量。

    参数:
        model: 加载了预训练权重的 CLIP 模型。
        texts (list[str]): 文本列表。
        device (str): 运行模型的设备。

    返回:
        numpy.ndarray: 文本的特征向量。
    """

    text_inputs = clip.tokenize(texts, truncate=True).to(device)
    with torch.no_grad():
        text_features = model.encode_text(text_inputs)
    return text_features.cpu().numpy()

# 如果直接运行这个文件，会演示加载模型的过程
if __name__ == "__main__":
    model = load_clip_model()
    print("CLIP model loaded successfully.")