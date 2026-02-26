---
name: generate-image-by-seedream
description: Generate or edit images via Doubao Seedream 5.0 on Volcengine Ark.
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

# Generate Image by Seedream (Doubao Seedream)

Use the bundled script to generate or edit images via Volcengine Ark Seedream.

Default model: `doubao-seedream-4-5-251128`

Generate

```bash
uv run {baseDir}/scripts/generate_image.py --prompt "你的图片描述" --filename "output.png" --size 2K
```

Image-to-image / reference images (multiple URLs)

```bash
uv run {baseDir}/scripts/generate_image.py \
  --prompt "将图1的服装换为图2的服装" \
  --filename "output.png" \
  -i "https://ark-project.tos-cn-beijing.volces.com/doc_image/seedream4_imagesToimage_1.png" \
  -i "https://ark-project.tos-cn-beijing.volces.com/doc_image/seedream4_5_imagesToimage_2.png" \
  --size 2K
```

API key

- `ARK_API_KEY` env var
- Or set `skills."generate-image-by-seedream".apiKey` / `skills."generate-image-by-seedream".env.ARK_API_KEY` in `~/.openclaw/openclaw.json`

Notes

- Size options depend on the Seedream model; recommended: `2K` (default), `4K`.
- Use timestamps in filenames: `yyyy-mm-dd-hh-mm-ss-name.png`.
- The script prints a `MEDIA:` line for OpenClaw to auto-attach on supported chat providers.
- The script downloads the first image URL returned by Ark and saves it locally as PNG.

