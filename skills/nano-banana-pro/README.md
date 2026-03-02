# Nano Banana Pro (Gemini 3 Pro Image)

Generate or edit images via Gemini 3 Pro Image (Nano Banana Pro).

## Usage

### Generate

```bash
uv run {baseDir}/scripts/generate_image.py --prompt "your image description" --filename "output.png" --resolution 1K
```

### Edit (single image)

```bash
uv run {baseDir}/scripts/generate_image.py --prompt "edit instructions" --filename "output.png" -i "/path/in.png" --resolution 2K
```

### Multi-image composition (up to 14 images)

```bash
uv run {baseDir}/scripts/generate_image.py --prompt "combine these into one scene" --filename "output.png" -i img1.png -i img2.png -i img3.png
```

## Notes

- **API Key**: Requires `GEMINI_API_KEY` environment variable.
- **Resolutions**: `1K` (default), `2K`, `4K`.
