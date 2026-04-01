#!/usr/bin/env python3
import argparse
import sys


def get_novel_info(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
            lines = content.split('\n')
            char_count = len(content)
            line_count = len(lines)
            non_empty_lines = sum(1 for line in lines if line.strip())
            print(f'总字符数: {char_count}')
            print(f'总行数: {line_count}')
            print(f'非空行数: {non_empty_lines}')
    except Exception as e:
        print(f'Error: {e}', file=sys.stderr)
        sys.exit(1)


def read_novel_segment(filepath, start):
    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
            total = len(content)
            segment = content[start:start + 3000]
            end = min(start + 3000, total)
            count = len(segment)
            progress = (end / total * 100) if total > 0 else 0
            print(segment)
            print(f'[start:{start}, end:{end}, count:{count}, progress:{progress:.2f}%]')
    except Exception as e:
        print(f'Error: {e}', file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description='Read novel from specified position or get novel info')
    parser.add_argument('filepath', help='Path to the novel file')
    parser.add_argument('--info', action='store_true', help='Get novel information (character count, line count, etc.)')
    parser.add_argument('--start', type=int, default=0, help='Start position (character index, 0-based, default: 0)')
    
    args = parser.parse_args()
    
    if args.info:
        get_novel_info(args.filepath)
    else:
        read_novel_segment(args.filepath, args.start)


if __name__ == '__main__':
    main()
