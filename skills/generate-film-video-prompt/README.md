# Generate Film Video Prompt

Inspired by github.com/Emily2040/seedance-2.0

## Description

通用影视视频提示词核心速查：五层结构、镜头与运动、灯光与风格、角色与特效、音频与反废话。写短剧/广告/动作/氛围片时的统一 skill，本skill只是用于写提示词指导，无法直接生成视频。

## Usage

This skill helps you write executable and measurable film prompts for video generation models.

### 1. 总体结构：五层 + 两条铁律

**铁律 1：前 20–30 个字必须是「主体 + 核心动作」**
**铁律 2：每个 clip 只允许 1 个主动作（动词）**

推荐结构（六件事）：

1. **SHOT**：景别/构图（远景/中景/近景/特写…）
2. **SUBJECT**：谁（角色、物体）、外形特征
3. **ACTION**：做什么（1 个主动作 + 简短物理/节奏）
4. **CAMERA**：镜头 framing + 运动 + 速度 + 视角
5. **STYLE / LIGHT**：风格与基调（镜头语言+灯光，而不是形容词）
6. **SOUND**：环境音 + SFX + 音乐/静音 决策

### 2. @Tag 使用：所有资源都要“有职位”

请根据你所用平台/模型的**资源限制**（图片/视频/音频的数量与大小）来规划输入。

**每个 @Tag 必须说明角色：**

- `@Image1 作为主角形象参考`
- `@Image2 作为场景/环境参考`
- `@Video1 的运镜作为整个片子的镜头风格参考`

### 3. 镜头（Camera）：四要素合同

每个镜头都要给出这 4 项：

- **Framing**
- **Movement**
- **Speed / Duration**
- **Angle**

### 4. 运动（Motion）：节奏与时间语言

- 4–6s：1 个明显变化
- 8–10s：1–2 个变化
- 12–15s：2–3 个变化
