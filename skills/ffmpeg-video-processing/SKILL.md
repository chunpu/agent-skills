---
name: ffmpeg-video-processing
description: 基于 FFmpeg 的视频处理技能，提供最实用的日常视频处理命令示例
license: MIT
user-invocable: true
tags: ["ffmpeg", "video", "processing", "conversion", "compression"]
---

# FFmpeg 视频处理技能 · 实用场景示例

> 目标：提供最常用、最实用的 FFmpeg 视频处理命令，覆盖 90% 的日常需求。所有示例均经过验证，可直接复制使用。

## 查看视频信息

```bash
# 查看基本信息（推荐，日常用这个就够了）
ffmpeg -i input.mp4
```

## 视频转码与压缩

```bash
# MKV/AVI/WebM/MOV 转 MP4（H.264 + AAC，所有设备都能播放）
ffmpeg -i input.mkv -c:v libx264 -c:a aac output.mp4

# 1080p 视频压缩（质量优先，适合邮件/微信发送）
ffmpeg -i input.mp4 -c:v libx264 -crf 28 -preset medium output.mp4

# 720p 视频压缩（平衡大小和质量）
ffmpeg -i input.mp4 -vf "scale=1280:720" -c:v libx264 -crf 26 -preset medium output_720p.mp4

# H.265 编码，文件比 H.264 小 30-50%
ffmpeg -i input.mp4 -c:v libx265 -crf 28 -preset medium output_h265.mp4
```

## 视频裁剪与分割

```bash
# 从第 5 秒开始，截取 30 秒
ffmpeg -i input.mp4 -ss 00:00:05 -t 00:00:30 -c copy output.mp4

# 从开始到第 2 分钟
ffmpeg -i input.mp4 -to 00:02:00 -c copy output.mp4

# 从第 1 分 30 秒到结束
ffmpeg -i input.mp4 -ss 00:01:30 -c copy output.mp4

# 精确裁剪（重新编码，更准确）
ffmpeg -i input.mp4 -ss 00:00:10 -to 00:00:40 -c:v libx264 -crf 18 -c:a aac output.mp4

# 将视频分割成多个 10 分钟的片段
ffmpeg -i input.mp4 -c copy -segment_time 00:10:00 -f segment -reset_timestamps 1 output_%03d.mp4

# 按场景变化自动分割视频
ffmpeg -i input.mp4 -filter:v "select='gt(scene,0.4)',showinfo" -f null /dev/null 2>&1 | grep "pts_time:" | cut -d':' -f4 > scenes.txt
```

## 视频速度控制

```bash
# 2倍速播放（音频同时变速）
ffmpeg -i input.mp4 -filter_complex "[0:v]setpts=0.5*PTS[v];[0:a]atempo=2.0[a]" -map "[v]" -map "[a]" output_2x.mp4

# 0.5倍速播放（慢动作）
ffmpeg -i input.mp4 -filter_complex "[0:v]setpts=2.0*PTS[v];[0:a]atempo=0.5[a]" -map "[v]" -map "[a]" output_0.5x.mp4

# 视频和音频都倒放
ffmpeg -i input.mp4 -filter_complex "[0:v]reverse[v];[0:a]areverse[a]" -map "[v]" -map "[a]" output_reversed.mp4

# 视频定格（提取某一帧，循环 3 秒，然后拼接）
ffmpeg -i input.mp4 -ss 00:00:10 -vframes 1 freeze_frame.jpg
ffmpeg -loop 1 -i freeze_frame.jpg -t 3 -c:v libx264 -pix_fmt yuv420p freeze_part.mp4
ffmpeg -i input.mp4 -to 00:00:10 -c copy before.mp4
ffmpeg -i input.mp4 -ss 00:00:10 -c copy after.mp4
echo "file 'before.mp4'" > list.txt
echo "file 'freeze_part.mp4'" >> list.txt
echo "file 'after.mp4'" >> list.txt
ffmpeg -f concat -safe 0 -i list.txt -c copy output_freeze.mp4
```

## 视频拼接与转场

```bash
# 快速拼接（不重新编码，格式必须一致）
# 首先创建 filelist.txt：
# file 'video1.mp4'
# file 'video2.mp4'
ffmpeg -f concat -safe 0 -i filelist.txt -c copy output.mp4

# 重新编码拼接（格式不同时使用）
ffmpeg -f concat -safe 0 -i filelist.txt -c:v libx264 -crf 18 -c:a aac output.mp4

# 淡入淡出转场（1秒转场时间）
ffmpeg -i part1.mp4 -i part2.mp4 -filter_complex "xfade=transition=fade:duration=1:offset=4" output_fade.mp4

# 其他转场效果：wipeleft, wiperight, wipeup, wipedown, slideleft, slideright, circlecrop, rectcrop, dissolve
ffmpeg -i part1.mp4 -i part2.mp4 -filter_complex "xfade=transition=wipeleft:duration=1:offset=4" output_wipe.mp4
```

## 音频处理

```bash
# 提取为 MP3（高质量）
ffmpeg -i input.mp4 -q:a 0 -map a output.mp3

# 提取为 WAV（无损，适合编辑）
ffmpeg -i input.mp4 -vn -acodec pcm_s16le -ar 44100 -ac 2 output.wav

# 音量加倍
ffmpeg -i input.mp4 -filter:a "volume=2.0" output.mp4

# 音量减半
ffmpeg -i input.mp4 -filter:a "volume=0.5" output.mp4

# 自动归一化音量（让声音大小一致）
ffmpeg -i input.mp4 -filter:a "loudnorm" output.mp4

# 完全移除音频轨道
ffmpeg -i input.mp4 -c:v copy -an output_no_audio.mp4

# 用新音频替换原视频的音频
ffmpeg -i input.mp4 -i new_audio.mp3 -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 -shortest output.mp4
```

## 添加水印与元素

```bash
# 右下角添加图片水印
ffmpeg -i input.mp4 -i logo.png -filter_complex "overlay=W-w-10:H-h-10" output.mp4

# 左上角添加图片水印
ffmpeg -i input.mp4 -i logo.png -filter_complex "overlay=10:10" output.mp4

# 半透明水印
ffmpeg -i input.mp4 -i logo.png -filter_complex "[1:v]format=rgba,colorchannelmixer=aa=0.5[wm];[0:v][wm]overlay=W-w-10:H-h-10" output.mp4

# 添加文字水印
ffmpeg -i input.mp4 -vf "drawtext=text='Your Name':x=10:y=10:fontsize=24:fontcolor=white" output.mp4

# 动态移动的图片（从左到右移动）
ffmpeg -i input.mp4 -i moving.png -filter_complex "[1:v]format=rgba[wm];[0:v][wm]overlay=x='if(gte(t,2),-w+(t-2)*200,NAN)':y=100" output_moving_element.mp4
```

## 视频特效与调色

```bash
# 黑白效果
ffmpeg -i input.mp4 -vf "format=gray" output_gray.mp4

# 复古/旧电影效果
ffmpeg -i input.mp4 -vf "colorchannelmixer=.3:.4:.3:0:.3:.4:.3:0:.3:.4:.3,eq=gamma=0.8:contrast=1.2" output_vintage.mp4

# 模糊效果
ffmpeg -i input.mp4 -vf "boxblur=5:1" output_blur.mp4

# 锐化效果
ffmpeg -i input.mp4 -vf "unsharp=5:5:1.5" output_sharp.mp4

# 浮雕效果
ffmpeg -i input.mp4 -vf "convolution='-2 -1 0:-1 1 1:0 1 2'" output_emboss.mp4

# 高级调色（亮度、对比度、饱和度、伽马值）
ffmpeg -i input.mp4 -vf "eq=brightness=0.1:contrast=1.2:saturation=1.3:gamma=1.1" output_color.mp4

# 曲线调色（模拟 LUT 效果）
ffmpeg -i input.mp4 -vf "curves=preset=strong_contrast" output_curves.mp4

# 其他曲线预设：color_negative, cross_process, darker, increase_contrast, lighter, linear_contrast, medium_contrast, negative, strong_contrast, vintage

# 动态缩放聚焦（从 1.0 倍缩放到 2.0 倍）
ffmpeg -i input.mp4 -vf "zoompan=z='min(zoom+0.01,2)':d=125" output_zoom.mp4

# 画面稳定（视频防抖）
ffmpeg -i input.mp4 -vf "vidstabdetect=shakiness=10:accuracy=15:result=transforms.trf" -f null /dev/null
ffmpeg -i input.mp4 -vf "vidstabtransform=input=transforms.trf:smoothing=30:optzoom=2" output_stabilized.mp4

# 隐私马赛克（人脸或指定区域打码）
ffmpeg -i input.mp4 -vf "drawbox=x=100:y=100:w=200:h=200:color=black:t=fill" output_box.mp4

# 像素化马赛克效果
ffmpeg -i input.mp4 -vf "crop=200:200:100:100,scale=10:10,scale=200:200:flags=neighbor[mask];[in][mask]overlay=100:100" output_pixelate.mp4
```

## 字幕处理

```bash
# 添加 SRT 字幕文件到视频（硬编码字幕，所有播放器都能显示）
ffmpeg -i input.mp4 -vf "subtitles=subtitle.srt" output_with_subs.mp4

# 添加 ASS 字幕文件（支持更丰富的样式）
ffmpeg -i input.mp4 -vf "ass=subtitle.ass" output_with_ass.mp4

# 从视频中提取字幕流
ffmpeg -i input.mp4 -map 0:s:0 -c:s copy subtitle.srt

# 内嵌字幕到视频（软字幕，可开关）
ffmpeg -i input.mp4 -i subtitle.srt -c copy -c:s mov_text output_with_softsubs.mp4

# 调整字幕样式（字体、大小、颜色）
ffmpeg -i input.mp4 -vf "subtitles=subtitle.srt:force_style='FontName=Arial,FontSize=24,PrimaryColour=&Hffffff&'" output_styled_subs.mp4
```

## 画面变换

```bash
# 4K 转 1080p
ffmpeg -i input_4k.mp4 -vf "scale=1920:1080" output_1080p.mp4

# 1080p 转 720p
ffmpeg -i input.mp4 -vf "scale=1280:720" output_720p.mp4

# 固定宽度，高度按比例（宽度 1280）
ffmpeg -i input.mp4 -vf "scale=1280:-1" output.mp4

# 固定高度，宽度按比例（高度 720）
ffmpeg -i input.mp4 -vf "scale=-1:720" output.mp4

# 改为 30 fps
ffmpeg -i input.mp4 -r 30 output.mp4

# 改为 60 fps（插帧，更流畅）
ffmpeg -i input.mp4 -vf "minterpolate=fps=60" output_60fps.mp4

# 顺时针旋转 90 度
ffmpeg -i input.mp4 -vf "transpose=1" output.mp4

# 逆时针旋转 90 度
ffmpeg -i input.mp4 -vf "transpose=2" output.mp4

# 旋转 180 度
ffmpeg -i input.mp4 -vf "transpose=1,transpose=1" output.mp4

# 水平镜像翻转
ffmpeg -i input.mp4 -vf "hflip" output.mp4

# 垂直镜像翻转
ffmpeg -i input.mp4 -vf "vflip" output.mp4

# 淡入效果
ffmpeg -i input.mp4 -vf "fade=in:start_frame=0:nb_frames=30" output_fadein.mp4

# 淡出效果
ffmpeg -i input.mp4 -vf "fade=out:start_frame=100:nb_frames=30" output_fadeout.mp4
```

## 导出与生成

```bash
# 视频转 GIF（简单转换，适合小视频）
ffmpeg -i input.mp4 -vf "fps=10,scale=480:-1:flags=lanczos" -c:v gif output.gif

# 高质量 GIF 转换（两步法，推荐）
ffmpeg -i input.mp4 -vf "fps=10,scale=480:-1:flags=lanczos,palettegen" palette.png
ffmpeg -i input.mp4 -i palette.png -filter_complex "fps=10,scale=480:-1:flags=lanczos[x];[x][1:v]paletteuse" output.gif

# 提取第一帧
ffmpeg -i input.mp4 -vframes 1 first_frame.jpg

# 提取最后一帧（推荐方法）
# -sseof -1 从结束前 1 秒开始，-update 1 不断更新最终只保留最后一帧
ffmpeg -sseof -1 -i input.mp4 -update 1 -q:v 1 last_frame.jpg

# 从第 5 秒获取一帧作为缩略图
ffmpeg -i input.mp4 -ss 00:00:05 -vframes 1 thumbnail.jpg

# 生成 10 张缩略图（均匀分布）
ffmpeg -i input.mp4 -vf "select='not(mod(n\,floor(N/10)))'" -vframes 10 thumbnail_%04d.jpg

# 提取所有关键帧
ffmpeg -i input.mp4 -vf "select='eq(pict_type,PICT_TYPE_I)'" -vsync vfr keyframe_%04d.jpg

# 图片转视频（单张图片循环 10 秒）
ffmpeg -loop 1 -i image.jpg -t 10 -c:v libx264 -pix_fmt yuv420p -r 30 output_image_to_video.mp4

# 多张图片序列转视频（image_001.jpg, image_002.jpg...）
ffmpeg -framerate 24 -i image_%03d.jpg -c:v libx264 -pix_fmt yuv420p output_sequence.mp4

# 图片淡入淡出效果（2秒淡入，2秒淡出）
ffmpeg -loop 1 -i image.jpg -t 10 -vf "fade=in:0:60,fade=out:240:60" -c:v libx264 -pix_fmt yuv420p output_fade_image.mp4
```

## 批量处理

```bash
# 批量转换为 MP4
for file in *.mkv *.avi *.webm *.mov; do
    if [ -f "$file" ]; then
        ffmpeg -i "$file" -c:v libx264 -c:a aac "${file%.*}.mp4"
    fi
done

# 批量压缩
for file in *.mp4; do
    ffmpeg -i "$file" -c:v libx264 -crf 28 -preset medium "compressed_$file"
done

# 批量生成缩略图
for file in *.mp4; do
    ffmpeg -i "$file" -ss 00:00:05 -vframes 1 "${file%.mp4}_thumb.jpg"
done
```

## 常见问题修复

```bash
# 音视频不同步，重新排序时间戳
ffmpeg -i input.mp4 -c copy -fflags +genpts output.mp4

# 修复损坏的视频
ffmpeg -i input.mp4 -c copy -avoid_negative_ts 1 output.mp4
```

## 参数速查表

### 常用编码参数

| 参数 | 说明 |
|------|------|
| `-c:v libx264` | H.264 视频编码（兼容性最好） |
| `-c:v libx265` | H.265/HEVC 视频编码（文件更小） |
| `-c:a aac` | AAC 音频编码 |
| `-crf 18-28` | 恒定质量因子（18=最好，28=较小） |
| `-preset medium` | 编码速度预设 |
| `-c copy` | 直接复制流，不重新编码 |

### 常用滤镜参数

| 滤镜 | 说明 |
|------|------|
| `scale=w:h` | 调整分辨率 |
| `crop=w:h:x:y` | 裁剪画面 |
| `transpose=1/2` | 旋转视频 |
| `hflip/vflip` | 水平/垂直翻转 |
| `drawtext` | 添加文字 |
| `overlay` | 叠加图片/视频 |
| `setpts=0.5*PTS` | 视频变速 |
| `atempo=2.0` | 音频变速 |
| `reverse` | 视频倒放 |
| `areverse` | 音频倒放 |
| `subtitles=file.srt` | 添加字幕 |
| `eq=brightness=x:contrast=y` | 调色 |
| `curves=preset=xxx` | 曲线调色 |
| `boxblur=5:1` | 模糊效果 |
| `unsharp=5:5:1.5` | 锐化效果 |
| `format=gray` | 黑白效果 |
| `fade=in/out` | 淡入淡出 |
| `xfade=transition=xxx` | 转场效果 |
| `zoompan` | 缩放聚焦 |
| `vidstabdetect/transform` | 画面稳定 |
| `select='eq(pict_type,PICT_TYPE_I)'` | 提取关键帧 |
