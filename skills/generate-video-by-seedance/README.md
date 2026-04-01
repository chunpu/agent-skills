# 豆包 Seedance 视频生成

使用随技能打包的脚本，通过**字节跳动** Seedance 视频模型在火山引擎 Ark 上生成/编辑视频：

- **豆包 Seedance** 系列视频模型（通过 Ark contents/generations/tasks 接口）
- 支持文生视频、图生视频（单图 / 多图参考）

## 使用方法

### 文生视频

```bash
uv run {baseDir}/scripts/generate_video.py \
  --prompt "一个在草地上奔跑的小狗视频，阳光明媚，电影感" \
  --filename "奔跑小狗.mp4"
```

### 使用 YAML 配置文件

可以将所有生视频参数写入 YAML 配置文件，然后通过 `--config` 参数使用：

#### 文生视频配置示例 (`text2video.yaml`)：

```yaml
prompt: 一个在草地上奔跑的小狗视频，阳光明媚，电影感
filename: 奔跑小狗.mp4
ratio: 16:9
duration: 5
```

#### 图生视频配置示例（带 URL 参考图列表，`image2video.yaml`）：

```yaml
prompt: 将图1的表情换为图2的表情，做一个眨眼微笑的短视频
filename: 表情女孩.mp4
images:
  - https://ark-project.tos-cn-beijing.volces.com/doc_image/seedream4_imagesToimage_1.png
  - https://ark-project.tos-cn-beijing.volces.com/doc_image/seedream4_5_imagesToimage_2.png
ratio: 9:16
duration: 5
```

#### 本地参考图配置示例（`local_images.yaml`）：

```yaml
prompt: 多图融合成一个动画短片
filename: 多图融合动画.mp4
images:
  - /path/to/参考图1.jpg
  - /path/to/参考图2.png
ratio: 16:9
duration: 8
```

#### 使用方法：

```bash
uv run {baseDir}/scripts/generate_video.py --config image2video.yaml
```

#### 混合使用配置文件和命令行参数（命令行参数优先级更高）：

```bash
uv run {baseDir}/scripts/generate_video.py --config prompt.yaml --filename "自定义文件名.mp4"
```

#### YAML 配置文件支持的所有参数：

- `prompt`: 视频内容描述
- `filename`: 输出文件名
- `images`: 参考图像列表（可以是 URL 或本地文件路径）
- `ratio`: 画面比例（如 "16:9"、"9:16"）
- `duration`: 视频时长（秒）
- `model`: 完整的模型名称（高级选项）
- `api_key`: API 密钥

### 图生视频 / 参考图

```bash
uv run {baseDir}/scripts/generate_video.py \
  --prompt "参考图片中的女孩，做一个挥手微笑的短视频" \
  --filename "挥手女孩.mp4" \
  -i "https://example.com/ref_image_1.png" \
  -i "/path/to/local_ref_2.jpg" \
  --ratio "9:16" \
  --duration 8
```

### 只用参考图（无显式文案提示）

```bash
uv run {baseDir}/scripts/generate_video.py \
  --filename "仅参考图生成视频.mp4" \
  -i "/path/to/ref1.jpg" \
  -i "/path/to/ref2.png"
```

## 注意事项

- **API 密钥**：需要设置 `ARK_API_KEY` 环境变量。
- **比例**：`"16:9"`（默认）、`"9:16"`、`"1:1"`、`"21:9"`。
- **时长**：视频时长（秒）。
