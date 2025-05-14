# 图像特征向量提取工具

这个项目提供了一个简单的Python工具，用于从图片中提取特征向量（图片的向量表示），支持多种预训练模型和输出格式。

## 功能特点

- 支持多种预训练模型提取图像特征
- 提供不同输出格式（JSON、文件保存、二进制等）
- 支持向量压缩以减少数据大小
- 可作为Python模块导入到其他项目中使用

## 安装依赖

```bash
pip install -r requirements.txt
```

## 命令行使用方法

### 基本用法

```bash
python vector_extractor.py --image 图片路径
```

### 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| --image | 图片路径（必需） | - |
| --model | 使用的预训练模型 | resnet50 |
| --output | 输出文件路径(使用file输出格式时有效) | 图片名称_vector.npy |
| --format | 输出格式 | json |
| --compress | 是否压缩向量数据 | false |
| --precision | 压缩时保留的小数位数 | 4 |

### 支持的模型

- resnet50（默认）
- resnet18
- vgg16

### 支持的输出格式

- `json`: 直接输出JSON格式数据
- `file`: 保存为.npy文件
- `binary`: 输出二进制数据
- `db_json`: 数据库JSON列格式
- `db_binary`: 数据库BLOB列格式

### 示例

提取图片向量并保存为文件：
```bash
python vector_extractor.py --image path/to/image.jpg --format file --output my_vector.npy
```

使用不同模型并输出JSON格式：
```bash
python vector_extractor.py --image path/to/image.jpg --model vgg16 --format json
```

压缩向量并输出数据库格式：
```bash
python vector_extractor.py --image path/to/image.jpg --compress --precision 3 --format db_json
```

## 作为模块导入

您也可以在其他Python脚本中导入这个模块使用：

```python
from vector_extractor import extract_vector_from_image

# 提取图片向量
vector = extract_vector_from_image("path/to/image.jpg", model_name="resnet50", compress=True)

# 使用向量进行后续处理
print(vector.shape)
```

## 许可证

本项目采用MIT许可证 