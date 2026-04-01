# Novel Reader - 智能长文本小说阅读器

智能读取和分析长文本小说，解决 LLM 上下文窗口有限的问题。

## 功能特性

- 📖 **分段读取**：每次读取固定字数或按章节分段，避免超出上下文窗口限制
- 📝 **智能摘要**：每读完一章生成一句话摘要，维护整体大纲和前情提要
- 📊 **进度追踪**：记录阅读百分比、已读字数、总字数
- 🎯 **资产管理**：自动识别并记录新出现的角色、道具、场景，更新资产信息

## 安装

无需特殊依赖，只需要 Python 3.6+。

```bash
chmod +x scripts/novel_reader.py
```

## 使用方法

### 基本用法

```bash
python scripts/novel_reader.py /path/to/novel.txt
```

### 命令行参数

- `--chunk-size` - 每次读取的字数（默认：5000）
- `--chapter-detector` - 章节检测模式（`regex` 或 `heuristic`，默认：`regex`）
- `--force-restart` - 强制重新开始阅读，忽略已保存的进度

### 示例

1. 开始阅读一本小说：
```bash
python scripts/novel_reader.py /Users/bytedance/books/my_novel.txt
```

2. 自定义每次读取的字数：
```bash
python scripts/novel_reader.py /Users/bytedance/books/my_novel.txt --chunk-size 8000
```

3. 强制重新开始：
```bash
python scripts/novel_reader.py /Users/bytedance/books/my_novel.txt --force-restart
```

## 数据文件

脚本会在小说目录下自动创建以下文件：

- `{小说名}_outline.md` - 整体大纲，包含每章摘要
- `{小说名}_progress.json` - 阅读进展，包含前情提要和进度统计
- `{小说名}_assets.json` - 资产信息，包含角色、道具、场景

## 工作原理

1. 从上次中断的位置继续阅读
2. 读取固定字数或检测到下一章标题时停止
3. 生成当前章节的一句话摘要
4. 提取并记录新出现的角色、道具、场景
5. 更新阅读进度、大纲和资产信息
6. 显示当前阅读状态和内容预览

## 章节检测

支持两种章节检测模式：
- `regex`：使用正则表达式匹配常见的章节标题格式（中文和英文）
- `heuristic`：启发式检测（待实现）

### 支持的章节标题格式

#### 中文格式
- `第一章`、`第二回`、`第三卷`、`第四部`、`第五篇`
- `第6集`、`第7幕`、`第8话`、`第9节`
- `第一百二十章`、`第三千零五十回`
- `第1章：标题`、`第2回 - 标题`
- `【第一章】标题`、`[第二章] 标题`
- `  第3章`（支持前导空格）

#### 英文格式
- `Chapter 1`、`CHAPTER 2`、`Chapter Three`
- `Ep. 3`、`Episode 4`、`EPISODE 5`
- `Part 6`、`PART 7`、`Act 8`、`ACT 9`
- `Scene 10`、`SCENE 11`

#### 数字格式
- `1. 标题`、`2) 标题`、`3、标题`

## 许可证

MIT
