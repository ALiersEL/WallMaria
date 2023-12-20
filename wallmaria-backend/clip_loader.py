import torch
import clip.model

def load_clip_model(checkpoint_path="checkpoints/latest.pth") -> clip.model.CLIP:
    """
    加载并返回一个预训练的 CLIP 模型。

    参数:
        checkpoint_path (str): 模型权重文件的路径。

    返回:
        model: 加载了预训练权重的 CLIP 模型。
    """
    # 检查 CUDA 是否可用
    device = "cuda" if torch.cuda.is_available() else "cpu"

    # 加载模型和预处理工具
    model, preprocess = clip.load("ViT-L/14", device=device)

    # 加载自定义模型权重
    model.load_state_dict(torch.load(checkpoint_path, map_location=device)['model_state_dict'])
    model.eval()

    return model

# 如果直接运行这个文件，会演示加载模型的过程
if __name__ == "__main__":
    model = load_clip_model()
    print("CLIP model loaded successfully.")
