---
name: generate-image-by-seedream
description: 通过字节跳动火山引擎 Ark 的豆包 Seedream（即梦 / Dreamina）图像模型生成或编辑图片。
homepage: https://www.volcengine.com/product/ark
metadata: {}
---

# 豆包 Seedream 图像生成

使用附带的脚本通过**字节跳动**图像生成模型生成或编辑图片：

- **豆包 Seedream（即梦 / Dreamina）** 系列生图模型
- 支持文生图、图生图、多图参考编辑

默认版本：`4.5` → 对应 `doubao-seedream-4-5-251128`。
默认尺寸：`2K`。

### 模型效果建议

- 效果排序：`4.5` > `5.0` > `4.0`
- 推荐优先使用 `4.5` 版本以获得最佳效果

### 画面比例

- 必须在生图提示词（prompt）中明确指定画面比例，例如：“生成可爱小狗，9:16竖屏比例”

## 文生图

```bash
uv run {baseDir}/scripts/generate_image.py --prompt "你的图片描述" --filename "可爱小狗.jpg"
```

## 使用 YAML 配置文件

可以将所有生图参数写入 YAML 配置文件，然后通过 `--config` 参数使用：

### 文生图配置示例 (`text2image.yaml`)：

```yaml
prompt: 一只可爱的小狗在草地上，9:16竖屏比例
filename: 可爱小狗.jpg
size: 2K
version: 4.5
```

### 图生图配置示例（带参考图列表，`image2image.yaml`）：

```yaml
prompt: 将图1的服装换为图2的服装
filename: 换装女孩.jpg
images:
  - https://ark-project.tos-cn-beijing.volces.com/doc_image/seedream4_imagesToimage_1.png
  - https://ark-project.tos-cn-beijing.volces.com/doc_image/seedream4_5_imagesToimage_2.png
size: 2K
version: 4.5
```

### 本地参考图配置示例 (`local_images.yaml`)：

```yaml
prompt: 多图融合成一张插画
filename: 多图融合插画.jpg
images:
  - /path/to/参考图1.jpg
  - /path/to/参考图2.png
size: 2K
version: 4.5
```

### 使用方法：

```bash
uv run {baseDir}/scripts/generate_image.py --config image2image.yaml
```

### 混合使用配置文件和命令行参数（命令行参数优先级更高）：

```bash
uv run {baseDir}/scripts/generate_image.py --config prompt.yaml --filename "自定义文件名.jpg"
```

### YAML 配置文件支持的所有参数：

- `prompt`: 图片描述
- `filename`: 输出文件名
- `images`: 参考图像列表（可以是 URL 或本地文件路径）
- `size`: 输出尺寸（如 "2K"、"4K"）
- `version`: Seedream 版本（如 "4.5"）
- `model`: 完整的模型名称（高级选项）
- `api_key`: API 密钥

## 图生图 / 参考图像（多张图像：URL 或本地文件）

```bash
uv run {baseDir}/scripts/generate_image.py \
  --prompt "将图1的服装换为图2的服装" \
  --filename "换装女孩.jpg" \
  -i "https://ark-project.tos-cn-beijing.volces.com/doc_image/seedream4_imagesToimage_1.png" \
  -i "https://ark-project.tos-cn-beijing.volces.com/doc_image/seedream4_5_imagesToimage_2.png" \
  --size 2K \
  --version 4.5
```

## 本地参考图像（多张本地文件）

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

### API 密钥

- 你要先自动检测是否有 `ARK_API_KEY` 环境变量，没有需要向用户要或者让用户在火山引擎申请

### 版本选项

- `4.0` → `doubao-seedream-4-0-250828`
- `4.5`（默认）→ `doubao-seedream-4-5-251128`
- `5.0` → `doubao-seedream-5-0-260128`
- 高级选项：仍可通过 `--model doubao-seedream-5-0-lite-260128` 等参数覆盖默认映射。

### 尺寸选项（按版本）

- `4.0`: `1K`, `2K`, `4K`
- `4.5`: `2K`, `4K`
- `5.0`: `2K`, `3K`

### 文件名建议（供调用方参考）

- 不要在文件名里包含 "seedream" 之类的实现细节。
- 文件名语言应与用户 Prompt 语言保持一致，例如中文 Prompt 就用简短中文文件名（如 `可爱小狗.jpg`）。
- 名字要有语义但尽量简短，避免过长句子。

### 关键词提示（供搜索发现）

- "doubao", "豆包", "即梦", "Seedream", "dreamina"
- "ByteDance image model", "字节跳动生图模型"
- "文生图", "图生图", "参考图", "图片生成", "图像生成", "换装", "图片编辑"
