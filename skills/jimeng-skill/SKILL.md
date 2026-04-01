---
name: jimeng-skill
description: 使用即梦 Dreamina CLI 生成图片或视频。Invoke when user needs to generate images or videos using Jimeng (Dreamina).
---

# 即梦 Skill

使用即梦 CLI 生成图片或视频
【重要并发限制】：即梦最多只能并行三个排队或生成中的任务！

## 默认值偏好顺序

始终用户要求优先，用户没要求时使用以下默认偏好顺序

### 生图
- 模型偏好顺序(model_version)：4.6 > 4.5 > 5.0 > 4.0
- 分辨率(resolution_type)：2k

### 生视频
- 模型偏好顺序(model_version)：seedance2.0 > seedance2.0fast
- 分辨率(video_resolution)：720p

### 通用（生图+生视频）
- 比例(ratio)偏好顺序：16:9 > 9:16 > 1:1

## 初始化

### 1. 先检查状态和积分

```bash
dreamina user_credit
```

如果命令未找到，先安装：

```bash
curl -fsSL https://jimeng.jianying.com/cli | bash
```

如果未登录，需要执行 `dreamina login` 登录，这个命令会拉起本地浏览器获取登录凭证。

### 2. 查看所有功能

```bash
dreamina --help
```

## 生图

生图相对较快，直接生成：

```bash
dreamina text2image --prompt "你的提示词" --ratio 16:9
```

生成完成后直接下载到本地即可。

## 生视频（异步任务 + 轮询进度）

视频生成通常需要较长时间，提交任务后会返回 `submit_id`，需要通过定时轮询获取任务进度和排队情况。

### 1. 提交生视频任务

查看具体子命令帮助：

```bash
dreamina multimodal2video --help
# 或
dreamina text2video --help
```

提交任务后会返回 `submit_id` 和当前排队位置，请记录 `submit_id` 用于后续轮询查询进度。

### 2. 查询任务状态和轮询

使用以下命令定时查询任务状态：

```bash
dreamina query_result --submit_id <submit_id>
```

该命令会返回：
- 当前任务状态
- 排队位置/排队进度
- 如果已完成，会返回生成结果的下载 URL

### 3. 定时轮询流程

由于生成视频时间较长，需要每分钟轮询一次：

```bash
# 每分钟查询一次状态
while true; do
  echo "=== $(date) ==="
  dreamina query_result --submit_id <submit_id>
  echo
  sleep 60
done
```

任务完成后，从返回结果中提取下载 URL，使用 curl 下载并指定语义化的文件名：

```bash
curl -o "output.mp4" "<download_url>"
```

### 4. 排队进度与等待时间估算

根据队列实际消耗速度估算：

- 记录每次轮询的时间差和排队位置变化
- 计算出**每分钟队列平均前进多少位**
- 用当前剩余排队位置除以前进速度，得到**预估排队结束还需要多少分钟**
- 将这两个信息告诉用户即可

## 万能参考

生图和生视频支持多参考输入

按照生成参数资源传入的顺序来引用参考图像：引用的方式是在提示词写 图1，图2，音频1，视频1 这种，例如

```txt
提取图1、图2、图3的相机,把背景换成白色,相机在一个白色桌子上,然后以相机为主体360°缓慢旋转,晰展示相机的正面侧面以及背面。
```

## 从本地文本提示词文件生成

所有生图和生视频命令都支持从本地文本文件读取提示词：ina multimodal2video --prompt "$(cat prompt.txt)"
```

## 从本地文本提示词文件生成

所有生图和生视频命令都支持从本地文本文件读取提示词：

```bash
dreamina text2image --prompt "$(cat prompt.txt)" --ratio 16:9
dreamina text2video --prompt "$(cat prompt.txt)"
```

## 本地提示词 + 多参考生视频

命令行举例：

```bash
dreamina multimodal2video --image ./角色A.jpg --image ./角色B.jpg --image ./场景1.jpg --prompt "角色A参考图1，角色B参考图2，场景1参考图3。 $(cat prompt.txt)"
```

## 常用子命令（优先使用这几个）

- `dreamina text2image`：根据提示词生成图片
- `dreamina image2image`：多参考图像生成图片
- `dreamina text2video`：文生视频
- `dreamina multimodal2video`：全能参考生视频（支持图片参考 + 文字提示）
- `dreamina query_result`：查询异步任务状态（生视频必须使用）
- `dreamina list_task`：列出已提交任务及其状态
- `dreamina user_credit`：查看剩余积分

## 下载资源

- 使用 `curl` 下载并指定语义化的文件名：

例如

```bash
curl -o "semantic-filename.mp4" "<download_url>"
```

## 错误处理

如果遇到生成错误，你要把具体错误信息告诉用户，引导用户解决错误。