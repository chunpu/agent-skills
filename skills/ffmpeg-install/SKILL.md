---
name: ffmpeg-install
description: FFmpeg 安装与检查技能，提供跨平台安装方案
license: MIT
user-invocable: true
tags: ["ffmpeg", "install", "setup", "environment"]
---

# FFmpeg 安装与检查技能

> 目标：快速检查和安装 FFmpeg，支持 macOS、Linux、Windows 等主流平台

## 检查 FFmpeg 是否已安装

```bash
# 检查 FFmpeg 命令是否存在
if command -v ffmpeg &> /dev/null; then
    echo "FFmpeg 已安装"
    ffmpeg -version
else
    echo "FFmpeg 未安装，请按下方说明安装"
fi
```

## macOS 安装

```bash
# 使用 Homebrew 安装（推荐）
brew install ffmpeg

# 或者安装完整版（包含更多编解码器）
brew install ffmpeg --with-fdk-aac --with-ffplay --with-freetype --with-libass --with-libquvi --with-libvorbis --with-libvpx --with-opus --with-x265

# 验证安装
ffmpeg -version
```

## Linux 安装

### Ubuntu/Debian
```bash
# 更新软件包列表
sudo apt update

# 安装 FFmpeg
sudo apt install ffmpeg

# 验证安装
ffmpeg -version
```

### CentOS/RHEL
```bash
# 安装 EPEL 源
sudo yum install epel-release

# 安装 FFmpeg
sudo yum install ffmpeg ffmpeg-devel

# 验证安装
ffmpeg -version
```

### Arch Linux
```bash
# 安装 FFmpeg
sudo pacman -S ffmpeg

# 验证安装
ffmpeg -version
```

## Windows 安装

### 方法 1：使用 Chocolatey（推荐）
```powershell
# 安装 Chocolatey（如果未安装）
# 以管理员身份运行 PowerShell，执行：
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# 安装 FFmpeg
choco install ffmpeg

# 验证安装
ffmpeg -version
```

### 方法 2：使用 Scoop
```powershell
# 安装 Scoop（如果未安装）
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
Invoke-RestMethod -Uri https://get.scoop.sh | Invoke-Expression

# 添加 extras 仓库
scoop bucket add extras

# 安装 FFmpeg
scoop install ffmpeg

# 验证安装
ffmpeg -version
```

### 方法 3：手动安装
1. 访问 https://ffmpeg.org/download.html
2. 下载 Windows 版本的 FFmpeg
3. 解压到某个目录（如 `C:\ffmpeg`）
4. 将 `C:\ffmpeg\bin` 添加到系统 PATH 环境变量
5. 重启终端，验证安装：`ffmpeg -version`

## 验证安装

```bash
# 查看 FFmpeg 版本
ffmpeg -version

# 查看 FFmpeg 支持的编解码器
ffmpeg -codecs

# 查看 FFmpeg 支持的格式
ffmpeg -formats

# 运行简单测试
ffmpeg -h
```

## 常见问题

### macOS: brew command not found
```bash
# 安装 Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### Linux: Permission denied
```bash
# 使用 sudo 运行
sudo apt install ffmpeg
```

### Windows: 命令无法识别
- 确保已将 FFmpeg 的 bin 目录添加到 PATH
- 重启终端或命令提示符
- 验证：`echo %PATH%` (Windows) 或 `echo $PATH` (macOS/Linux)
