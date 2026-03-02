# Generate Image by Doubao / 豆包 Seedream (即梦 / Dreamina)

Use the bundled script to generate or edit images via **ByteDance / 字节跳动** image generation models:

- **Doubao / 豆包 Seedream (即梦 / Dreamina)** 系列生图模型
- 支持文生图、图生图、多图参考编辑

Default version: `4.5` → mapped to `doubao-seedream-4-5-251128`.
Default size: `2K`.

## Usage

### Generate

```bash
uv run {baseDir}/scripts/generate_image.py --prompt "你的图片描述" --filename "可爱小狗.jpg"
```

### Image-to-image / reference images (multiple images: URL or local file)

```bash
uv run {baseDir}/scripts/generate_image.py \
  --prompt "将图1的服装换为图2的服装" \
  --filename "换装女孩.jpg" \
  -i "https://ark-project.tos-cn-beijing.volces.com/doc_image/seedream4_imagesToimage_1.png" \
  -i "https://ark-project.tos-cn-beijing.volces.com/doc_image/seedream4_5_imagesToimage_2.png" \
  --size 2K \
  --version 4.5
```

### Local image references (multiple local files)

```bash
uv run {baseDir}/scripts/generate_image.py \
  --prompt "多图融合成一张插画" \
  --filename "多图融合插画.jpg" \
  -i "/path/to/参考图1.jpg" \
  -i "/path/to/参考图2.png" \
  --size 2K \
  --version 4.5
```

## Notes

- **API Key**: Requires `ARK_API_KEY` environment variable.
- **Versions**: `4.0`, `4.5` (default), `5.0`.
- **Sizes**: `1K`, `2K`, `4K` (depending on version).
