---
name: doc-to-txt
description: Convert DOC, DOCX, and PDF files to TXT format. Invoke when user wants to extract text from these document types.
metadata:
  {
    "openclaw":
      {
        "emoji": "📄",
        "requires": { "bins": ["uv"] },
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

# Doc to TXT 文档转换

将 DOC、DOCX、PDF 文件转换为 TXT 纯文本格式。

## 使用方法

```bash
uv run {baseDir}/scripts/convert.py <输入文件路径> [--output <输出文件路径>]
```

## 参数说明

| 参数 | 说明 |
|------|------|
| `<输入文件路径>` | 要转换的文档文件（支持 .doc, .docx, .pdf） |
| `--output` | 可选，输出 txt 文件路径（默认同目录同名 .txt） |

## 示例

转换 PDF 到 TXT：
```bash
uv run skills/doc-to-txt/scripts/convert.py document.pdf
```

指定输出文件：
```bash
uv run skills/doc-to-txt/scripts/convert.py report.docx --output output.txt
```
