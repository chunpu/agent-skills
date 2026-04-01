---
name: ffmpeg-audio-processing
description: 基于 FFmpeg 的音频处理技能，提供最实用的日常音频处理命令
license: MIT
user-invocable: true
tags: ["ffmpeg", "audio", "processing", "conversion", "compression"]
---

# FFmpeg 音频处理技能 · 实用场景示例

> 目标：提供最常用、最实用的 FFmpeg 音频处理命令，按需求频次从高到低排序

## 音频属性查看

```bash
# 查看音频属性
ffmpeg -i input.mp3 2>&1
```

## 音频格式转换（最常用）

```bash
# MP3 转 WAV（无损）
ffmpeg -i input.mp3 output.wav

# WAV 转 MP3（高质量，VBR 0）
ffmpeg -i input.wav -q:a 0 output.mp3

# WAV 转 MP3（中等质量，192kbps CBR）
ffmpeg -i input.wav -b:a 192k output.mp3

# 任意格式转 AAC（适合视频配音）
ffmpeg -i input.mp3 -c:a aac -b:a 256k output.m4a

# 任意格式转 OGG（开源格式）
ffmpeg -i input.mp3 -c:a libvorbis -q:a 4 output.ogg

# 任意格式转 FLAC（无损压缩）
ffmpeg -i input.wav -c:a flac output.flac
```

## 音频压缩

```bash
# MP3 压缩（VBR 2，平衡质量与大小）
ffmpeg -i input.mp3 -q:a 2 output_compressed.mp3

# MP3 压缩（VBR 4，更小体积）
ffmpeg -i input.mp3 -q:a 4 output_small.mp3

# AAC 压缩（128kbps，适合网络传输）
ffmpeg -i input.m4a -c:a aac -b:a 128k output_compressed.m4a

# 批量压缩 MP3
for file in *.mp3; do
    ffmpeg -i "$file" -q:a 2 "compressed_$file"
done
```

## 音频裁剪

```bash
# 从第 30 秒开始，截取 1 分钟
ffmpeg -i input.mp3 -ss 00:00:30 -t 00:01:00 -c copy output.mp3

# 从开始到第 2 分钟
ffmpeg -i input.mp3 -to 00:02:00 -c copy output.mp3

# 从第 1 分钟到结束
ffmpeg -i input.mp3 -ss 00:01:00 -c copy output.mp3

# 精确裁剪（重新编码，更准确）
ffmpeg -i input.mp3 -ss 00:00:10 -to 00:00:40 -c:a libmp3lame -q:a 0 output.mp3
```

## 音频拼接

```bash
# 快速拼接（不重新编码，格式必须一致）
# 首先创建 filelist.txt：
# file 'audio1.mp3'
# file 'audio2.mp3'
# file 'audio3.mp3'
ffmpeg -f concat -safe 0 -i filelist.txt -c copy output.mp3

# 重新编码拼接（格式不同时使用）
ffmpeg -f concat -safe 0 -i filelist.txt -c:a libmp3lame -q:a 0 output.mp3
```

## 音量调整

```bash
# 音量加倍
ffmpeg -i input.mp3 -filter:a "volume=2.0" output.mp3

# 音量减半
ffmpeg -i input.mp3 -filter:a "volume=0.5" output.mp3

# 音量增加 3dB
ffmpeg -i input.mp3 -filter:a "volume=3dB" output.mp3

# 音量降低 6dB
ffmpeg -i input.mp3 -filter:a "volume=-6dB" output.mp3

# 自动归一化音量（让声音大小一致）
ffmpeg -i input.mp3 -filter:a "loudnorm" output.mp3

# 查看当前音量最大值
ffmpeg -i input.mp3 -filter:a "volumedetect" -f null /dev/null
```

## 从视频提取音频

```bash
# 提取为 MP3（高质量）
ffmpeg -i video.mp4 -q:a 0 -map a audio.mp3

# 提取为 WAV（无损，适合编辑）
ffmpeg -i video.mp4 -vn -acodec pcm_s16le -ar 44100 -ac 2 audio.wav

# 提取为 AAC
ffmpeg -i video.mp4 -c:a aac -b:a 256k audio.m4a

# 只提取某段音频（从第 10 秒到第 30 秒）
ffmpeg -i video.mp4 -ss 00:00:10 -to 00:00:30 -q:a 0 audio.mp3
```

## 音频混音

```bash
# 两个音频混合（背景音乐 + 人声）
ffmpeg -i background.mp3 -i voice.mp3 -filter_complex "amix=inputs=2:duration=longest" output.mp3

# 两个音频混合，调整音量（背景音乐 0.3，人声 1.0）
ffmpeg -i background.mp3 -i voice.mp3 -filter_complex "[0:a]volume=0.3[a0];[1:a]volume=1.0[a1];[a0][a1]amix=inputs=2:duration=longest" output.mp3
```

## 音频淡入淡出

```bash
# 开头 3 秒淡入
ffmpeg -i input.mp3 -af "afade=t=in:st=0:d=3" output.mp3

# 结尾 3 秒淡出
ffmpeg -i input.mp3 -af "afade=t=out:st=57:d=3" output.mp3

# 开头 3 秒淡入，结尾 3 秒淡出（总长 60 秒）
ffmpeg -i input.mp3 -af "afade=t=in:st=0:d=3,afade=t=out:st=57:d=3" output.mp3
```

## 音频声道处理

```bash
# 立体声转单声道
ffmpeg -i input.mp3 -ac 1 output_mono.mp3

# 单声道转立体声
ffmpeg -i input.mp3 -ac 2 output_stereo.mp3

# 交换左右声道
ffmpeg -i input.mp3 -af "channelmap=channel_layout=stereo:map=FL-FR|FR-FL" output_swapped.mp3

# 只保留左声道
ffmpeg -i input.mp3 -af "pan=mono|c0=FL" output_left.mp3

# 只保留右声道
ffmpeg -i input.mp3 -af "pan=mono|c0=FR" output_right.mp3
```

## 音频采样率调整

```bash
# 改为 44100 Hz（CD 质量）
ffmpeg -i input.mp3 -ar 44100 output.mp3

# 改为 48000 Hz（视频常用）
ffmpeg -i input.mp3 -ar 48000 output.mp3

# 改为 22050 Hz（降低采样率，减小体积）
ffmpeg -i input.mp3 -ar 22050 output.mp3
```

## 音频静音检测与移除

```bash
# 检测静音部分
ffmpeg -i input.mp3 -af "silencedetect=n=-50dB:d=1" -f null /dev/null

# 移除开头静音
ffmpeg -i input.mp3 -af "silenceremove=start_periods=1:start_duration=1:start_threshold=-50dB" output.mp3

# 移除结尾静音
ffmpeg -i input.mp3 -af "silenceremove=stop_periods=1:stop_duration=1:stop_threshold=-50dB" output.mp3

# 移除开头和结尾静音
ffmpeg -i input.mp3 -af "silenceremove=start_periods=1:start_duration=1:start_threshold=-50dB:stop_periods=1:stop_duration=1:stop_threshold=-50dB" output.mp3
```

## 音频去噪降噪

```bash
# 基础降噪（afftdn，频域降噪，适合大多数场景）
ffmpeg -i input.mp3 -af "afftdn" output.mp3

# 强力降噪（afftdn 调整参数）
ffmpeg -i input.mp3 -af "afftdn=nf=-20:tn=-15" output.mp3

# 高通滤波（去除低频噪音，如电流声、嗡嗡声）
ffmpeg -i input.mp3 -af "highpass=f=80" output.mp3

# 低通滤波（去除高频噪音，如嘶嘶声）
ffmpeg -i input.mp3 -af "lowpass=f=10000" output.mp3

# 带通滤波（只保留人声频率范围 300-3400Hz）
ffmpeg -i input.mp3 -af "bandpass=f=1850:width=3100" output.mp3

# 组合降噪（高通 + afftdn，效果更好）
ffmpeg -i input.mp3 -af "highpass=f=80,afftdn" output.mp3

# 降噪强度调节（0-1，0.5 为中等强度）
ffmpeg -i input.mp3 -af "afftdn=nr=0.5" output.mp3

# 去除齿音（deesser，适合人声）
ffmpeg -i input.mp3 -af "deesser" output.mp3

# 强力去齿音（调整参数）
ffmpeg -i input.mp3 -af "deesser=i=0.5:m=0.8" output.mp3
```

## 去呼吸声与去回声

```bash
# 减少呼吸声（使用 compand 动态压缩）
ffmpeg -i input.mp3 -af "compand=attacks=0.3:decays=1:points=-80/-80|-20/-20|0/-20" output.mp3

# 去除轻微回声（使用 aecho 滤镜反向处理）
ffmpeg -i input.mp3 -af "aecho=0.8:0.88:60:0.4" output.mp3

# 减少房间混响（使用 afftdn 的降噪特性）
ffmpeg -i input.mp3 -af "afftdn=tn=-10" output.mp3

# 组合处理：去呼吸 + 去齿音 + 降噪
ffmpeg -i input.mp3 -af "compand=attacks=0.3:decays=1:points=-80/-80|-20/-20|0/-20,deesser,afftdn" output.mp3
```

## 音高修正与变速变调

```bash
# 使用 rubberband 变速不变调（推荐，音质最好）
# 2倍速，音调不变
ffmpeg -i input.mp3 -af "rubberband=tempo=2.0" output.mp3

# 0.5倍速，音调不变
ffmpeg -i input.mp3 -af "rubberband=tempo=0.5" output.mp3

# 变调不变速（升调 2 个半音）
ffmpeg -i input.mp3 -af "rubberband=pitch=2.0" output.mp3

# 变调不变速（降调 3 个半音）
ffmpeg -i input.mp3 -af "rubberband=pitch=-3.0" output.mp3

# 同时变速和变调（1.5倍速，升调 1 个半音）
ffmpeg -i input.mp3 -af "rubberband=tempo=1.5:pitch=1.0" output.mp3

# 使用 asetrate 简单变速（会同时变调）
# 2倍速（音调也会升高）
ffmpeg -i input.mp3 -af "asetrate=44100*2,aresample=44100" output.mp3

# 降调不变速（使用 atempo + asetrate 组合）
# 降调 1 个半音，速度不变
ffmpeg -i input.mp3 -filter_complex "[0:a]asetrate=44100*0.94387[a];[a]atempo=1/0.94387" output.mp3

# 音高修正模式（rubberband 的不同模式）
# 音乐模式（默认）
ffmpeg -i input.mp3 -af "rubberband=pitch=2.0:formants=crisp" output.mp3
# 人声模式
ffmpeg -i input.mp3 -af "rubberband=pitch=2.0:formants=shifted" output.mp3
```

## 音频倒放

```bash
# 音频倒放
ffmpeg -i input.mp3 -filter:a "areverse" output_reversed.mp3
```

## 音频变速

```bash
# 2倍速播放
ffmpeg -i input.mp3 -filter:a "atempo=2.0" output_2x.mp3

# 0.5倍速播放（慢放）
ffmpeg -i input.mp3 -filter:a "atempo=0.5" output_0.5x.mp3

# 1.5倍速播放
ffmpeg -i input.mp3 -filter:a "atempo=1.5" output_1.5x.mp3
```

## 音频分割

```bash
# 将音频分割成多个 5 分钟的片段
ffmpeg -i input.mp3 -c copy -segment_time 00:05:00 -f segment -reset_timestamps 1 output_%03d.mp3

# 按指定时间点分割
ffmpeg -i input.mp3 -t 00:05:00 -c copy part1.mp3
ffmpeg -i input.mp3 -ss 00:05:00 -c copy part2.mp3
```

## 批量处理

```bash
# 批量转换为 MP3
for file in *.wav *.flac *.m4a; do
    if [ -f "$file" ]; then
        ffmpeg -i "$file" -q:a 0 "${file%.*}.mp3"
    fi
done

# 批量压缩
for file in *.mp3; do
    ffmpeg -i "$file" -q:a 2 "compressed_$file"
done

# 批量提取音频（从视频）
for file in *.mp4 *.mkv *.avi; do
    if [ -f "$file" ]; then
        ffmpeg -i "$file" -q:a 0 "${file%.*}.mp3"
    fi
done
```

## 参数速查表

### 常用音频编码参数

| 参数 | 说明 |
|------|------|
| `-q:a 0` | MP3 VBR 最高质量 |
| `-q:a 2` | MP3 VBR 高质量 |
| `-q:a 4` | MP3 VBR 中等质量 |
| `-b:a 192k` | 192kbps CBR |
| `-c:a aac` | AAC 编码 |
| `-c:a libmp3lame` | MP3 编码 |
| `-c:a flac` | FLAC 无损编码 |
| `-c:a copy` | 直接复制流，不重新编码 |

### 常用音频滤镜参数

| 滤镜 | 说明 |
|------|------|
| `volume=2.0` | 音量加倍 |
| `loudnorm` | 自动归一化音量 |
| `afade=t=in:st=0:d=3` | 3秒淡入 |
| `afade=t=out:st=57:d=3` | 3秒淡出 |
| `atempo=2.0` | 2倍速 |
| `areverse` | 音频倒放 |
| `amix=inputs=2` | 混合两个音频 |
| `silencedetect` | 检测静音 |
| `silenceremove` | 移除静音 |
| `afftdn` | 频域降噪（基础） |
| `afftdn=nf=-20:tn=-15` | 强力降噪 |
| `highpass=f=80` | 高通滤波（去低频噪音） |
| `lowpass=f=10000` | 低通滤波（去高频噪音） |
| `bandpass=f=1850:width=3100` | 带通滤波（人声范围） |
| `deesser` | 去齿音 |
| `compand` | 动态压缩（去呼吸声） |
| `rubberband=tempo=2.0` | 变速不变调 |
| `rubberband=pitch=2.0` | 变调不变速 |
| `asetrate=44100*2` | 变速（同时变调） |
