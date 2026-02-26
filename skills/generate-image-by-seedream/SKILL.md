---
name: generate-image-by-seedream
description: Generate or edit images via Doubao / 豆包 Seedream (即梦 / Dreamina) ByteDance / 字节跳动 image models on Volcengine Ark.
homepage: https://www.volcengine.com/product/ark
metadata:
  {
    "openclaw":
      {
        "emoji": "🌊",
        "requires": { "bins": ["uv"], "env": ["ARK_API_KEY"] },
        "primaryEnv": "ARK_API_KEY",
        "install":
          [
            {
              "id": "uv-brew",
              "kind": "brew",
              "formula": "uv",
              "bins": ["uv"],
              "label": "Install uv (brew)",
            },
          ],
      },
  }
---

# Generate Image by Doubao / 豆包 Seedream (即梦 / Dreamina)

Use the bundled script to generate or edit images via **ByteDance / 字节跳动** image generation models:

- **Doubao / 豆包 Seedream (即梦 / Dreamina)** 系列生图模型
- 支持文生图、图生图、多图参考编辑

Default version: `4.5` → mapped to `doubao-seedream-4-5-251128`.
Default size: `2K`.

Generate

```bash
uv run {baseDir}/scripts/generate_image.py --prompt "你的图片描述" --filename "可爱小狗.jpg"
```

Image-to-image / reference images (multiple URLs)

```bash
uv run {baseDir}/scripts/generate_image.py \
  --prompt "将图1的服装换为图2的服装" \
  --filename "换装女孩.jpg" \
  -i "https://ark-project.tos-cn-beijing.volces.com/doc_image/seedream4_imagesToimage_1.png" \
  -i "https://ark-project.tos-cn-beijing.volces.com/doc_image/seedream4_5_imagesToimage_2.png" \
  --size 2K \
  --version 4.5
```

API key

- `ARK_API_KEY` env var
- Or set `skills."generate-image-by-seedream".apiKey` / `skills."generate-image-by-seedream".env.ARK_API_KEY` in `~/.openclaw/openclaw.json`

Notes

- Version options (user-facing):
  - `4.0` → `doubao-seedream-4-0-250828`
  - `4.5` (default) → `doubao-seedream-4-5-251128`
  - `5.0` → `doubao-seedream-5-0-260128`
- Advanced: you can still pass `--model doubao-seedream-5-0-lite-260128` etc. to override the mapping.
- Size options per version:
  - `4.0`: `1K`, `2K`, `4K`
  - `4.5`: `2K`, `4K`
  - `5.0`: `2K`, `3K`
- Use timestamps in filenames: `yyyy-mm-dd-hh-mm-ss-name.jpg`.
- The script prints a `MEDIA:` line for OpenClaw to auto-attach on supported chat providers.
- The script downloads the first image URL returned by Ark and saves it locally as JPEG.

Filename recommendation (for agents / 调用方):

- 不要在文件名里包含 "seedream" 之类的实现细节。
- 文件名语言应与用户 Prompt 语言保持一致，例如中文 Prompt 就用简短中文文件名（如 `可爱小狗.jpg`）。
- 名字要有语义但尽量简短，避免过长句子。

Keyword hints (for discovery / 命中搜索):

- "doubao", "豆包", "即梦", "Seedream", "dreamina"
- "ByteDance image model", "字节跳动生图模型"
- "文生图", "图生图", "参考图", "图片生成", "图像生成", "换装", "图片编辑"

