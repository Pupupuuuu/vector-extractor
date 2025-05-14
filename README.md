# 图像特征向量提取工具

这个项目提供了一个简单的Python脚本，用于从图片中提取特征向量（图片的向量表示）。

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

基本用法:

```bash
python image_to_vector.py --image 图片路径
```

指定不同的预训练模型:

```bash
python image_to_vector.py --image 图片路径 --model resnet18
```

支持的模型选项:
- resnet50 (默认)
- resnet18
- vgg16

## 输出结果

脚本会输出以下内容：
1. 提取的特征向量的维度
2. 向量的前10个元素作为预览
3. 将完整的特征向量保存为NPY文件（可用numpy加载）

## 作为模块导入

您也可以在其他Python脚本中导入这个模块：

```python
from image_to_vector import get_image_vector

# 提取图片向量
vector = get_image_vector("path/to/image.jpg", model_name="resnet50")

# 使用向量进行后续处理
print(vector.shape)
``` 