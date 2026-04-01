#!/usr/bin/env python3
# /// script
# requires-python = ">=3.8"
# dependencies = [
#     "python-docx>=1.1.0",
#     "PyPDF2>=3.0.0",
# ]
# ///
"""
Convert DOC, DOCX, and PDF files to TXT format.

Usage:
    uv run convert.py <input_file> [--output <output_file>]
"""

import argparse
import os
import sys


def extract_from_docx(file_path):
    try:
        from docx import Document
        doc = Document(file_path)
        return '\n'.join([para.text for para in doc.paragraphs])
    except ImportError:
        print("错误: 需要安装 python-docx 库")
        print("运行: uv pip install python-docx")
        sys.exit(1)


def extract_from_pdf(file_path):
    try:
        import PyPDF2
        import re
        text = ''
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text() + '\n'
        
        lines = text.split('\n')
        processed_lines = []
        buffer = ''
        
        for line in lines:
            stripped = line.strip()
            
            if not stripped:
                if buffer:
                    processed_lines.append(buffer)
                    buffer = ''
                processed_lines.append('')
                continue
            
            is_title = stripped.startswith('===') or stripped.endswith('===')
            is_list_item = re.match(r'^[A-Z\u4e00-\u9fa5]+[：:]', stripped)
            is_special_start = (stripped.startswith('「') or stripped.startswith('『') or 
                               stripped.startswith('（') or stripped.startswith('【') or
                               stripped.startswith('《') or re.match(r'^[第【\[\(（]', stripped))
            
            if is_title:
                if buffer:
                    processed_lines.append(buffer)
                    buffer = ''
                processed_lines.append(stripped)
                continue
            
            if buffer:
                prev_last = buffer[-1]
                curr_first = stripped[0]
                
                should_break = (
                    prev_last in '。！？；：,.!?;:' or 
                    is_list_item or
                    is_special_start or
                    (re.match(r'^[A-Z\u4e00-\u9fa5]', curr_first) and len(buffer) < 20)
                )
                
                if should_break:
                    processed_lines.append(buffer)
                    buffer = stripped
                else:
                    buffer += stripped
            else:
                buffer = stripped
        
        if buffer:
            processed_lines.append(buffer)
        
        return '\n'.join(processed_lines)
    except ImportError:
        print("错误: 需要安装 PyPDF2 库")
        print("运行: uv pip install PyPDF2")
        sys.exit(1)


def extract_from_doc(file_path):
    try:
        import textract
        return textract.process(file_path).decode('utf-8')
    except ImportError:
        print("错误: 需要安装 textract 库")
        print("运行: uv pip install textract")
        print("注意: textract 在某些系统上需要额外依赖")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description='Convert DOC, DOCX, PDF to TXT')
    parser.add_argument('input', help='Input file path (.doc, .docx, .pdf)')
    parser.add_argument('--output', help='Output file path (optional)')
    args = parser.parse_args()

    input_path = args.input
    if not os.path.exists(input_path):
        print(f"错误: 文件不存在: {input_path}")
        sys.exit(1)

    ext = os.path.splitext(input_path)[1].lower()

    if ext == '.docx':
        text = extract_from_docx(input_path)
    elif ext == '.pdf':
        text = extract_from_pdf(input_path)
    elif ext == '.doc':
        text = extract_from_doc(input_path)
    else:
        print(f"错误: 不支持的文件格式: {ext}")
        print("支持格式: .doc, .docx, .pdf")
        sys.exit(1)

    if args.output:
        output_path = args.output
    else:
        output_path = os.path.splitext(input_path)[0] + '.txt'

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(text)

    print(f"转换成功: {output_path}")


if __name__ == '__main__':
    main()
