---
name: generate-video-by-seedance
description: 通过字节跳动火山引擎 Ark 的豆包 Seedance 视频模型生成或编辑视频。
homepage: https://www.volcengine.com/product/ark
metadata: {}
---

# 豆包 Seedance 视频生成

使用随技能打包的脚本，通过**字节跳动** Seedance 视频模型在火山引擎 Ark 上生成/编辑视频：

- **豆包 Seedance** 系列视频模型（通过 Ark contents/generations/tasks 接口）
- 支持文生视频、图生视频（单图 / 多图参考）

默认设置：

- 默认模型：`doubao-seedance-1-5-pro-251215`（可用 `--model` 覆盖）
- 默认时长：`5` 秒
- 默认比例：`16:9`

## 文生视频

```bash
uv run {baseDir}/scripts/generate_video.py \
  --prompt "一个在草地上奔跑的小狗视频，阳光明媚，电影感" \
  --filename "奔跑小狗.mp4"
```

## 使用 YAML 配置文件

可以将所有生视频参数写入 YAML 配置文件，然后通过 `--config` 参数使用：

### 文生视频配置示例 (`text2video.yaml`)：

```yaml
prompt: 一个在草地上奔跑的小狗视频，阳光明媚，电影感
filename: 奔跑小狗.mp4
ratio: 16:9
duration: 5
```

### 图生视频配置示例（带 URL 参考图列表，`image2video.yaml`）：

```yaml
prompt: 将图1的表情换为图2的表情，做一个眨眼微笑的短视频
filename: 表情女孩.mp4
images:
  - https://ark-project.tos-cn-beijing.volces.com/doc_image/seedream4_imagesToimage_1.png
  - https://ark-project.tos-cn-beijing.volces.com/doc_image/seedream4_5_imagesToimage_2.png
ratio: 9:16
duration: 5
```

### 本地参考图配置示例（`local_images.yaml`）：

```yaml
prompt: 多图融合成一个动画短片
filename: 多图融合动画.mp4
images:
  - /path/to/参考图1.jpg
  - /path/to/参考图2.png
ratio: 16:9
duration: 8
```

### 使用方法：

```bash
uv run {baseDir}/scripts/generate_video.py --config image2video.yaml
```

### 混合使用配置文件和命令行参数（命令行参数优先级更高）：

```bash
uv run {baseDir}/scripts/generate_video.py --config prompt.yaml --filename "自定义文件名.mp4"
```

### YAML 配置文件支持的所有参数：

- `prompt`: 视频内容描述
- `filename`: 输出文件名
- `images`: 参考图像列表（可以是 URL 或本地文件路径）
- `ratio`: 画面比例（如 "16:9"、"9:16"）
- `duration`: 视频时长（秒）
- `model`: 完整的模型名称（高级选项）
- `api_key`: API 密钥

## 图生视频 / 参考图（URL 或本地文件均可，多图，使用 lite i2v 模型）

```bash
uv run {baseDir}/scripts/generate_video.py \
  --prompt "参考图片中的女孩，做一个挥手微笑的短视频" \
  --filename "挥手女孩.mp4" \
  -i "https://example.com/ref_image_1.png" \
  -i "/path/to/local_ref_2.jpg" \
  --ratio "9:16" \
  --duration 8
```

## 只用参考图（无显式文案提示）

```bash
uv run {baseDir}/scripts/generate_video.py \
  --filename "仅参考图生成视频.mp4" \
  -i "/path/to/ref1.jpg" \
  -i "/path/to/ref2.png"
```

> 提示：至少需要「提示词」或「参考图」其一存在，否则脚本会报错。

## 注意事项

### API 密钥

- 需要设置 `ARK_API_KEY` 环境变量

### 参数说明

- **prompt**：视频内容文案（中文 / 英文均可）
- **image / -i**：
  - URL：直接透传给 Ark（例如公网可访问的图片链接）
  - 本地文件：自动读取并转成 `data:image/...;base64,...` 形式再发送
  - 可多次传入，形成多图参考（多图目前仅在 `doubao-seedance-1-0-lite-i2v-250428` 等 lite i2v 模型下生效）
- **ratio**：画面比例，常用：
  - `"16:9"`（默认）
  - `"9:16"`
  - `"1:1"`
  - `"21:9"`
- **duration**：视频时长（秒），由模型 / Endpoint 实际支持的区间决定
- **model**（可选，高级）：直接指定 Ark Endpoint / 模型 ID，覆盖默认绑定

轮询脚本 `get_video_task_status.py` 额外参数：

- **interval**：轮询间隔（秒），默认 `10`，可根据任务耗时与频率需求自行调整
- **timeout**：最大等待时间（秒），默认 `600`，超过后脚本会报错退出

### 结果与文件输出

- Ark 视频生成通常是**异步任务**：
  - 脚本会调用 `POST /contents/generations/tasks`
  - 成功时优先解析返回的 `id` / `task_id` 作为任务 ID
  - 如果响应体中直接携带 `video_url`，脚本会尝试拉取并将视频保存到本地
- 保存路径规则：
  - 若 `--filename` 未指定目录，则默认保存到本仓库下的 `outputs/` 目录
  - 若文件名无后缀，则默认补上 `.mp4`

若调用成功但后端仅返回任务 ID、尚未生成 `video_url`，脚本会输出任务 ID，可配合轮询脚本一起使用：

```bash
# 1) 先创建任务（可能只返回 TASK_ID）
uv run {baseDir}/scripts/generate_video.py \
  --prompt "一个示例视频" \
  --filename "示例视频.mp4"

# 2) 拿到上一步输出的 TASK_ID 后，轮询直到生成完成并下载视频
uv run {baseDir}/scripts/get_video_task_status.py \
  cgt-20260226184301-4h8v6 \
  --filename "示例视频.mp4" \
  --interval 5
```

轮询脚本会：

- 定期调用 `GET /contents/generations/tasks/{task_id}` 查看任务状态
- 当状态为 `succeeded` / `completed` 且拿到 `video_url` 时，自动下载视频到本地

### 文件名推荐（供调用方参考）

- 不要在文件名里包含具体实现细节（如 "seedance"、"ark" 等）
- 文件名语言建议与 Prompt 语言一致，如中文 Prompt 就用简短中文文件名（如 `挥手女孩.mp4`）
- 文件名要有语义但尽量简短，避免过长句子

### 关键词提示（便于发现 / 搜索命中）

- "doubao", "豆包", "Seedance"
- "ByteDance video model", "字节跳动视频生成"
- "文生视频", "图生视频", "视频生成", "短视频生成"
