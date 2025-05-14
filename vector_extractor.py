import torch
import torchvision.models as models
from torchvision.models import ResNet50_Weights, ResNet18_Weights, VGG16_Weights
import torchvision.transforms as transforms
from PIL import Image
import numpy as np
import argparse
import os
import json
import sys
import base64
import pickle
import io

def load_image(image_path):
    """加载图片并应用预处理"""
    transform = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    
    image = Image.open(image_path).convert("RGB")
    image_tensor = transform(image).unsqueeze(0)  # 添加批次维度
    return image_tensor

def get_image_vector(image_path, model_name="resnet50"):
    """提取图片的特征向量"""
    # 选择并加载预训练模型
    if model_name == "resnet50":
        model = models.resnet50(weights=ResNet50_Weights.IMAGENET1K_V1)
    elif model_name == "resnet18":
        model = models.resnet18(weights=ResNet18_Weights.IMAGENET1K_V1)
    elif model_name == "vgg16":
        model = models.vgg16(weights=VGG16_Weights.IMAGENET1K_V1)
    else:
        raise ValueError(f"不支持的模型: {model_name}")
    
    # 移除最后的全连接层以获取特征向量
    if model_name.startswith("resnet"):
        model = torch.nn.Sequential(*list(model.children())[:-1])
    elif model_name == "vgg16":
        model = torch.nn.Sequential(*list(model.children())[:-1])
    
    model.eval()
    
    # 加载图片
    img_tensor = load_image(image_path)
    
    # 提取特征
    with torch.no_grad():
        features = model(img_tensor)
    
    # 将特征向量展平并转换为numpy数组
    features = features.squeeze().numpy()
    
    return features

def compress_vector(vector, precision=4):
    """压缩向量，减少数据大小"""
    return np.round(vector, precision)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="从图片中提取特征向量")
    parser.add_argument("--image", type=str, required=True, help="图片路径")
    parser.add_argument("--model", type=str, default="resnet50", 
                        choices=["resnet18", "resnet50", "vgg16"], 
                        help="要使用的预训练模型")
    parser.add_argument("--output", type=str, default="", 
                        help="输出文件路径(使用file输出格式时有效)")
    parser.add_argument("--format", type=str, default="json", 
                        choices=["json", "file", "binary", "db_json", "db_binary"], 
                        help="输出格式:\n" + 
                             "json: 直接输出JSON格式数据\n" +
                             "file: 保存为.npy文件\n" +
                             "binary: 输出二进制数据\n" +
                             "db_json: 数据库JSON列格式\n" +
                             "db_binary: 数据库BLOB列格式")
    parser.add_argument("--compress", action="store_true", 
                        help="压缩向量数据以减小大小")
    parser.add_argument("--precision", type=int, default=4,
                        help="使用压缩时保留的小数位数")
    
    args = parser.parse_args()
    
    # 获取图片向量
    vector = get_image_vector(args.image, args.model)
    
    # 如果需要压缩向量
    if args.compress:
        vector = compress_vector(vector, args.precision)
    
    # 提取文件名（不含路径和扩展名）用于输出
    base_filename = os.path.basename(args.image)
    base_filename = os.path.splitext(base_filename)[0]
    
    # 根据输出格式处理
    if args.format == "json":
        # 输出JSON格式的向量数据
        result = {
            "vector": vector.tolist(),
            "dimensions": vector.shape[0],
            "model": args.model
        }
        print(json.dumps(result))
    
    elif args.format == "binary":
        # 输出二进制数据，适合直接传输
        # 为避免终端显示问题，使用base64编码
        binary_data = pickle.dumps(vector)
        encoded_data = base64.b64encode(binary_data).decode('utf-8')
        print(encoded_data)
    
    elif args.format == "db_json":
        # 数据库JSON列格式，包含更多元数据和压缩格式
        result = {
            "vector_data": vector.tolist(),
            "metadata": {
                "model": args.model,
                "dimensions": int(vector.shape[0]),
                "image": base_filename,
                "compressed": args.compress,
                "precision": args.precision if args.compress else None,
                "created_at": __import__('datetime').datetime.now().isoformat()
            }
        }
        print(json.dumps(result))
    
    elif args.format == "db_binary":
        # 数据库BLOB列格式，二进制数据
        metadata = {
            "model": args.model,
            "dimensions": int(vector.shape[0]),
            "compressed": args.compress
        }
        
        # 将元数据和向量数据一起序列化
        data_with_metadata = {
            "metadata": metadata,
            "vector": vector
        }
        
        # 序列化并base64编码
        binary_data = pickle.dumps(data_with_metadata)
        encoded_data = base64.b64encode(binary_data).decode('utf-8')
        print(encoded_data)
    
    else:  # format == "file"
        # 输出文件格式
        print(f"图片向量维度: {vector.shape}")
        print(f"向量的前10个元素: {vector[:10]}")
        
        # 如果没有指定输出路径，则使用当前目录
        if not args.output:
            output_path = f"{base_filename}_vector.npy"
        else:
            output_path = args.output
            
        # 保存向量
        np.save(output_path, vector)
        print(f"向量已保存为: {output_path}")

# 可以作为模块导入，提供向量提取功能
def extract_vector_from_image(image_path, model_name="resnet50", compress=False, precision=4):
    vector = get_image_vector(image_path, model_name)
    if compress:
        vector = compress_vector(vector, precision)
    return vector 