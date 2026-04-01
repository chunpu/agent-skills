---
name: ffmpeg-image-processing
description: 基于 FFmpeg 的图片处理技能，提供最实用的日常图片处理命令
license: MIT
user-invocable: true
tags: ["ffmpeg", "image", "processing", "conversion", "compression"]
---

# FFmpeg 图片处理技能 · 实用场景示例

> 目标：提供最常用、最实用的 FFmpeg 图片处理命令，按需求频次从高到低排序

## 图片属性查看

```bash
# 查看图片属性
ffmpeg -i input.jpg 2>&1
```

## 图片格式转换（最常用）

```bash
# JPG 转 PNG（无损）
ffmpeg -i input.jpg output.png

# PNG 转 JPG（质量 85）
ffmpeg -i input.png -q:v 2 output.jpg

# JPG 转 WEBP（现代格式，文件更小）
ffmpeg -i input.jpg output.webp

# PNG 转 WEBP
ffmpeg -i input.png output.webp

# WEBP 转 JPG
ffmpeg -i input.webp output.jpg

# 任意格式转 BMP
ffmpeg -i input.jpg output.bmp

# 任意格式转 TIFF
ffmpeg -i input.jpg output.tiff
```

## 图片压缩

```bash
# JPG 压缩（质量 85，推荐）
ffmpeg -i input.jpg -q:v 2 output_compressed.jpg

# JPG 压缩（质量 75，更小体积）
ffmpeg -i input.jpg -q:v 3 output_small.jpg

# JPG 压缩（质量 50，最小体积）
ffmpeg -i input.jpg -q:v 5 output_very_small.jpg

# PNG 压缩（无损）
ffmpeg -i input.png -compression_level 9 output_compressed.png

# WEBP 压缩（质量 80）
ffmpeg -i input.jpg -q:v 80 output.webp

# 批量压缩 JPG
for file in *.jpg; do
    ffmpeg -i "$file" -q:v 2 "compressed_$file"
done
```

## 图片尺寸调整

```bash
# 调整宽度为 1920，高度按比例
ffmpeg -i input.jpg -vf "scale=1920:-1" output.jpg

# 调整高度为 1080，宽度按比例
ffmpeg -i input.jpg -vf "scale=-1:1080" output.jpg

# 固定尺寸 1280x720（可能变形）
ffmpeg -i input.jpg -vf "scale=1280:720" output.jpg

# 固定尺寸并保持比例，不足部分用黑色填充
ffmpeg -i input.jpg -vf "scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2" output.jpg

# 4K 转 1080p
ffmpeg -i input_4k.jpg -vf "scale=1920:1080" output_1080p.jpg

# 缩略图（宽度 400）
ffmpeg -i input.jpg -vf "scale=400:-1" thumbnail.jpg
```

## 图片裁剪

```bash
# 从左上角裁剪 800x600
ffmpeg -i input.jpg -vf "crop=800:600:0:0" output.jpg

# 保留右上角裁剪 800x600
ffmpeg -i input.jpg -vf "crop=800:600:iw-800:0" output.jpg

# 从 (100, 50) 位置裁剪 400x300
ffmpeg -i input.jpg -vf "crop=400:300:100:50" output.jpg

# 裁剪中心区域（800x600）
ffmpeg -i input.jpg -vf "crop=800:600" output.jpg

# 裁剪为正方形（取较短边）
ffmpeg -i input.jpg -vf "crop=w=min(iw\,ih):h=min(iw\,ih)" output_square.jpg
```

## 图片旋转与翻转

```bash
# 顺时针旋转 90 度
ffmpeg -i input.jpg -vf "transpose=1" output.jpg

# 逆时针旋转 90 度
ffmpeg -i input.jpg -vf "transpose=2" output.jpg

# 旋转 180 度
ffmpeg -i input.jpg -vf "transpose=1,transpose=1" output.jpg

# 水平镜像翻转
ffmpeg -i input.jpg -vf "hflip" output.jpg

# 垂直镜像翻转
ffmpeg -i input.jpg -vf "vflip" output.jpg
```

## 图片添加水印

```bash
# 右下角添加图片水印
ffmpeg -i input.jpg -i logo.png -filter_complex "overlay=W-w-10:H-h-10" output.jpg

# 左上角添加图片水印
ffmpeg -i input.jpg -i logo.png -filter_complex "overlay=10:10" output.jpg

# 半透明水印（透明度 0.5）
ffmpeg -i input.jpg -i logo.png -filter_complex "[1:v]format=rgba,colorchannelmixer=aa=0.5[wm];[0:v][wm]overlay=W-w-10:H-h-10" output.jpg

# 居中添加图片水印
ffmpeg -i input.jpg -i logo.png -filter_complex "overlay=(W-w)/2:(H-h)/2" output.jpg

# 添加文字水印
ffmpeg -i input.jpg -vf "drawtext=text='Your Name':x=10:y=10:fontsize=36:fontcolor=white" output.jpg

# 添加半透明文字水印
ffmpeg -i input.jpg -vf "drawtext=text='Your Name':x=10:y=10:fontsize=36:fontcolor=white@0.5" output.jpg

# 文字描边
ffmpeg -i input.jpg -vf "drawtext=text='Your Name':x=10:y=10:fontsize=36:fontcolor=white:borderw=3:bordercolor=black" output.jpg

# 文字阴影
ffmpeg -i input.jpg -vf "drawtext=text='Your Name':x=12:y=12:fontsize=36:fontcolor=black,drawtext=text='Your Name':x=10:y=10:fontsize=36:fontcolor=white" output.jpg
```

## 6.1 剪切蒙版与形状

```bash
# 圆形剪切蒙版
ffmpeg -i input.jpg -vf "format=rgba,geq=r='r(X,Y)':g='g(X,Y)':b='b(X,Y)':a='if(gt(pow((X-W/2)/(W/2),2)+pow((Y-H/2)/(H/2),2),1),0,255)'" output.png

# 绘制红色矩形
ffmpeg -i input.jpg -vf "drawbox=x=100:y=100:w=200:h=150:color=red:t=5" output.jpg

# 绘制实心蓝色圆形
ffmpeg -i input.jpg -vf "drawcircle=x=300:y=200:r=50:color=blue" output.jpg

# 绘制红色箭头（使用矩形和三角形组合）
ffmpeg -i input.jpg -vf "drawbox=x=100:y=195:w=150:h=10:color=red:t=fill,drawpolygon=x=250:y=200:230:y=180:230:y=220:color=red" output.jpg
```

## 图片特效

```bash
# 黑白效果
ffmpeg -i input.jpg -vf "format=gray" output.jpg

# 复古效果
ffmpeg -i input.jpg -vf "colorchannelmixer=.3:.4:.3:0:.3:.4:.3:0:.3:.4:.3,eq=gamma=0.8:contrast=1.2" output.jpg

# 模糊效果
ffmpeg -i input.jpg -vf "boxblur=5:1" output.jpg

# 锐化效果
ffmpeg -i input.jpg -vf "unsharp=5:5:1.5" output.jpg

# 浮雕效果
ffmpeg -i input.jpg -vf "convolution='-2 -1 0:-1 1 1:0 1 2'" output.jpg

# 边缘检测
ffmpeg -i input.jpg -vf "edgedetect=mode=canny" output.jpg

# 负片效果
ffmpeg -i input.jpg -vf "curves=preset=negative" output.jpg

# 高对比度
ffmpeg -i input.jpg -vf "curves=preset=strong_contrast" output.jpg

# 调整亮度、对比度、饱和度
ffmpeg -i input.jpg -vf "eq=brightness=0.1:contrast=1.2:saturation=1.3" output.jpg

# 调整伽马值
ffmpeg -i input.jpg -vf "eq=gamma=1.2" output.jpg

# HSL 调色（调整色相、饱和度、亮度）
ffmpeg -i input.jpg -vf "hue=h=10:s=1.2:b=0.1" output.jpg
```

## 画质修复

```bash
# 去噪（轻量）
ffmpeg -i input.jpg -vf "hqdn3d=1.5:1.5:6:6" output.jpg

# 去噪（强力）
ffmpeg -i input.jpg -vf "nlmeans=s=5:p=3" output.jpg

# 人像磨皮
ffmpeg -i input.jpg -vf "hqdn3d=2:2:8:8,unsharp=3:3:-1.5:3:3:1.5" output.jpg
```

## 图片拼接

```bash
# 水平拼接两张图片
ffmpeg -i input1.jpg -i input2.jpg -filter_complex "hstack" output.jpg

# 垂直拼接两张图片
ffmpeg -i input1.jpg -i input2.jpg -filter_complex "vstack" output.jpg

# 水平拼接多张图片
ffmpeg -i input1.jpg -i input2.jpg -i input3.jpg -filter_complex "[0:v][1:v][2:v]hstack=inputs=3" output.jpg

# 2x2 网格拼接
ffmpeg -i input1.jpg -i input2.jpg -i input3.jpg -i input4.jpg -filter_complex "[0:v][1:v]hstack[top];[2:v][3:v]hstack[bottom];[top][bottom]vstack" output.jpg

# 三张图垂直等距分布（间距 20px）
ffmpeg -i input1.jpg -i input2.jpg -i input3.jpg -filter_complex "[0:v]pad=iw:ih+20[top];[top][1:v]vstack[mid];[mid]pad=iw:ih+20[mid2];[mid2][2:v]vstack" output.jpg
```

## 图片序列转视频

```bash
# 图片序列转视频（image_001.jpg, image_002.jpg...）
ffmpeg -framerate 24 -i image_%03d.jpg -c:v libx264 -pix_fmt yuv420p output.mp4

# 单张图片转视频（循环 10 秒）
ffmpeg -loop 1 -i image.jpg -t 10 -c:v libx264 -pix_fmt yuv420p -r 30 output.mp4

# 图片淡入淡出效果（2秒淡入，2秒淡出）
ffmpeg -loop 1 -i image.jpg -t 10 -vf "fade=in:0:60,fade=out:240:60" -c:v libx264 -pix_fmt yuv420p output.mp4
```

## 图片添加边框

```bash
# 添加黑色边框（上下左右各 20 像素）
ffmpeg -i input.jpg -vf "pad=w=iw+40:h=ih+40:x=20:y=20:color=black" output.jpg

# 添加白色边框（上下左右各 30 像素）
ffmpeg -i input.jpg -vf "pad=w=iw+60:h=ih+60:x=30:y=30:color=white" output.jpg

# 添加红色边框
ffmpeg -i input.jpg -vf "pad=w=iw+40:h=ih+40:x=20:y=20:color=red" output.jpg

# 画面框移动（向左移动 10 像素，右侧填充黑色）
ffmpeg -i input.jpg -vf "pad=w=iw+10:h=ih:x=10:y=0:color=black,crop=iw-10:ih:10:0" output.jpg
```

## 图片圆角

```bash
# 圆角效果（半径 50 像素）
ffmpeg -i input.jpg -vf "format=rgba,geq=r='X/W*r(X,Y)':g='X/W*g(X,Y)':b='X/W*b(X,Y)':a='if(gt(abs(X-W/2),W/2-50)*gt(abs(Y-H/2),H/2-50),0,255)'" output.png

# 更简单的方法：使用圆形遮罩
ffmpeg -i input.jpg -f lavfi -i color=c=black:s=200x200,format=gray,geq=lum='128+127*cos(2*PI*((X/W-0.5)^2+(Y/H-0.5)^2)^0.5)' -filter_complex "[1:v]scale=iw:ih[mask];[0:v][mask]alphamerge" output.png
```

## 图片批量处理

```bash
# 批量转换为 JPG
for file in *.png *.webp *.bmp; do
    if [ -f "$file" ]; then
        ffmpeg -i "$file" -q:v 2 "${file%.*}.jpg"
    fi
done

# 批量压缩
for file in *.jpg; do
    ffmpeg -i "$file" -q:v 2 "compressed_$file"
done

# 批量调整尺寸（宽度 1920）
for file in *.jpg; do
    ffmpeg -i "$file" -vf "scale=1920:-1" "resized_$file"
done

# 批量添加水印
for file in *.jpg; do
    ffmpeg -i "$file" -i logo.png -filter_complex "overlay=W-w-10:H-h-10" "watermarked_$file"
done
```

## 图片信息查看

```bash
# 查看图片基本信息
ffmpeg -i input.jpg

## 图片去除背景（简单方法）

```bash
# 使用 chromakey 去除绿色背景
ffmpeg -i input.jpg -vf "chromakey=0x00FF00:0.1:0.1" -c:v png output.png

# 使用 chromakey 去除蓝色背景
ffmpeg -i input.jpg -vf "chromakey=0x0000FF:0.1:0.1" -c:v png output.png
```

## 参数速查表

### 常用图片编码参数

| 参数 | 说明 |
|------|------|
| `-q:v 2` | JPG 高质量 |
| `-q:v 3` | JPG 中等质量 |
| `-q:v 5` | JPG 低质量 |
| `-compression_level 9` | PNG 最高压缩 |
| `-c:v copy` | 直接复制流，不重新编码 |

### 常用图片滤镜参数

| 滤镜 | 说明 |
|------|------|
| `scale=w:h` | 调整尺寸 |
| `crop=w:h:x:y` | 裁剪 |
| `transpose=1/2` | 旋转 |
| `hflip/vflip` | 翻转 |
| `overlay=x:y` | 叠加水印 |
| `drawtext` | 添加文字 |
| `format=gray` | 黑白 |
| `boxblur=5:1` | 模糊 |
| `unsharp=5:5:1.5` | 锐化 |
| `eq=brightness=x:contrast=y` | 调色 |
| `hue=h:s:b` | HSL 调色 |
| `pad=w:h:x:y:color=c` | 添加边框 |
| `hstack/vstack` | 拼接 |
| `hqdn3d` | 去噪 |
| `nlmeans` | 强力去噪 |
| `drawbox` | 绘制矩形 |
| `drawcircle` | 绘制圆形 |
| `drawpolygon` | 绘制多边形 |
