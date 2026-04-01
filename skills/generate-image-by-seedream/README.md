# 豆包 Seedream 图像生成

使用附带的脚本通过**字节跳动**图像生成模型生成或编辑图片：

- **豆包 Seedream（即梦 / Dreamina）** 系列生图模型
- 支持文生图、图生图、多图参考编辑

默认版本：`4.5` → 对应 `doubao-seedream-4-5-251128`。
默认尺寸：`2K`。

## 使用方法

### 文生图

```bash
uv run {baseDir}/scripts/generate_image.py --prompt "你的图片描述" --filename "可爱小狗.jpg"
```

### 使用 YAML 配置文件

可以将所有生图参数写入 YAML 配置文件，然后通过 `--config` 参数使用：

#### 文生图配置示例 (`text2image.yaml`)：
```yaml
prompt: 一只可爱的小狗在草地上，9:16竖屏比例
filename: 可爱小狗.jpg
size: 2K
version: 4.5
```

#### 图生图配置示例（带参考图列表，`image2image.yaml`）：
```yaml
prompt: 将图1的服装换为图2的服装
filename: 换装女孩.jpg
images:
  - https://ark-project.tos-cn-beijing.volces.com/doc_image/seedream4_imagesToimage_1.png
  - https://ark-project.tos-cn-beijing.volces.com/doc_image/seedream4_5_imagesToimage_2.png
size: 2K
version: 4.5
```

#### 本地参考图配置示例 (`local_images.yaml`)：
```yaml
prompt: 多图融合成一张插画
filename: 多图融合插画.jpg
images:
  - /path/to/参考图1.jpg
  - /path/to/参考图2.png
size: 2K
version: 4.5
```

#### 使用方法：
```bash
uv run {baseDir}/scripts/generate_image.py --config image2image.yaml
```

#### 混合使用配置文件和命令行参数（命令行参数优先级更高）：
```bash
uv run {baseDir}/scripts/generate_image.py --config prompt.yaml --filename "自定义文件名.jpg"
```

#### YAML 配置文件支持的所有参数：
- `prompt`: 图片描述
- `filename`: 输出文件名
- `images`: 参考图像列表（可以是 URL 或本地文件路径）
- `size`: 输出尺寸（如 "2K"、"4K"）
- `version`: Seedream 版本（如 "4.5"）
- `model`: 完整的模型名称（高级选项）
- `api_key`: API 密钥

### 图生图 / 参考图像（多张图像：URL 或本地文件）

```bash
uv run {baseDir}/scripts/generate_image.py \
  --prompt "将图1的服装换为图2的服装" \
  --filename "换装女孩.jpg" \
  -i "https://ark-project.tos-cn-beijing.volces.com/doc_image/seedream4_imagesToimage_1.png" \
  -i "https://ark-project.tos-cn-beijing.volces.com/doc_image/seedream4_5_imagesToimage_2.png" \
  --size 2K \
  --version 4.5
```

### 本地参考图像（多张本地文件）

```bash
uv run {baseDir}/scripts/generate_image.py \
  --prompt "多图融合成一张插画" \
  --filename "多图融合插画.jpg" \
  -i "/path/to/参考图1.jpg" \
  -i "/path/to/参考图2.png" \
  --size 2K \
  --version 4.5
```

## 注意事项

- **API 密钥**：需要设置 `ARK_API_KEY` 环境变量。
- **版本**：`4.0`、`4.5`（默认）、`5.0`。
- **尺寸**：`1K`、`2K`、`4K`（取决于版本）。
