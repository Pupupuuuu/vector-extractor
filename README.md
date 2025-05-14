# 图像特征向量提取工具

这个项目提供了一个简单的Python工具，用于从图片中提取特征向量（图片的向量表示），支持多种预训练模型和输出格式。

## 功能特点

- 支持多种预训练模型提取图像特征
- 提供不同输出格式（JSON、文件保存、二进制等）
- 支持向量压缩以减少数据大小
- 可作为Python模块导入到其他项目中使用
- 可打包为独立的可执行文件

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

## 打包为可执行文件

本项目可以打包为独立的可执行文件，无需安装Python和依赖库即可运行。

### 打包步骤

使用提供的Python打包脚本:

```bash
# 交互式打包（带有更多选项）
python package.py

# 或使用简化的打包脚本（自动完成所有步骤）
python package_simple.py
```

打包完成后，可执行文件会生成在`dist`目录下。

### 使用可执行文件

打包后的可执行文件与原始Python脚本有相同的命令行参数:

```bash
vector_extractor.exe --image path/to/image.jpg --model resnet50 --format json
```

## 许可证

本项目采用MIT许可证 