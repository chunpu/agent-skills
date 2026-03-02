# Generate Video by Doubao / 豆包 Seedance

使用随技能打包的脚本，通过 **ByteDance / 字节跳动** Seedance 视频模型在 **Volcengine Ark** 上生成 / 编辑视频：

- **Doubao / 豆包 Seedance** 系列视频模型（通过 Ark contents/generations/tasks 接口）
- 支持文生视频、图生视频（单图 / 多图参考）

## Usage

### Generate Video from Text

```bash
uv run {baseDir}/scripts/generate_video.py \
  --prompt "一个在草地上奔跑的小狗视频，阳光明媚，电影感" \
  --filename "奔跑小狗.mp4"
```

### Image-to-Video / Reference Images

```bash
uv run {baseDir}/scripts/generate_video.py \
  --prompt "参考图片中的女孩，做一个挥手微笑的短视频" \
  --filename "挥手女孩.mp4" \
  -i "https://example.com/ref_image_1.png" \
  -i "/path/to/local_ref_2.jpg" \
  --ratio "9:16" \
  --duration 8
```

### Reference Images Only

```bash
uv run {baseDir}/scripts/generate_video.py \
  --filename "仅参考图生成视频.mp4" \
  -i "/path/to/ref1.jpg" \
  -i "/path/to/ref2.png"
```

## Notes

- **API Key**: Requires `ARK_API_KEY` environment variable.
- **Ratio**: `"16:9"` (default), `"9:16"`, `"1:1"`, `"21:9"`.
- **Duration**: Video duration in seconds.
