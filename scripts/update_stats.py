#!/usr/bin/env python3
"""自动更新 Note 站点统计信息"""

import os
from pathlib import Path
import re
from datetime import datetime

def count_markdown_files(docs_dir):
    """统计 markdown 文件数量（排除 index.md）"""
    count = 0
    for root, dirs, files in os.walk(docs_dir):
        for file in files:
            if file.endswith('.md') and file != 'index.md':
                count += 1
    return count

def count_categories(docs_dir):
    """统计分类数量（一级目录）"""
    categories = set()
    for item in os.listdir(docs_dir):
        item_path = os.path.join(docs_dir, item)
        if os.path.isdir(item_path) and not item.startswith('.'):
            categories.add(item)
    return len(categories)

def count_total_words(docs_dir):
    """统计总字数（中文字符 + 英文单词）"""
    total_words = 0
    for root, dirs, files in os.walk(docs_dir):
        for file in files:
            if file.endswith('.md') and file != 'index.md':
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # 移除 front matter
                    content = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)
                    # 统计中文字符
                    chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', content))
                    # 统计英文单词
                    english_words = len(re.findall(r'\b[a-zA-Z]+\b', content))
                    total_words += chinese_chars + english_words
    return total_words

def update_index_stats(index_path, note_count, category_count, total_words):
    """更新 index.md 中的统计信息"""
    with open(index_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 计算预计阅读时间（假设每分钟阅读 300 字）
    reading_time = round(total_words / 300)
    
    # 更新统计表格
    stats_pattern = r'(## 站点统计\n\n\| 指标 \| 数值 \|\n\|:-----|:-----\|\n)\| 笔记总数 \| \d+ 篇 \|\n\| 分类数量 \| \d+ 个 \|'
    stats_replacement = f'\\1| 笔记总数 | {note_count} 篇 |\n| 分类数量 | {category_count} 个 |\n| 总字数 | {total_words:,} 字 |\n| 预计阅读 | {reading_time} 分钟 |'
    
    content = re.sub(stats_pattern, stats_replacement, content)
    
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✓ 统计信息已更新:")
    print(f"  - 笔记总数: {note_count} 篇")
    print(f"  - 分类数量: {category_count} 个")
    print(f"  - 总字数: {total_words:,} 字")
    print(f"  - 预计阅读: {reading_time} 分钟")

def main():
    # 获取项目根目录
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    docs_dir = project_root / 'sites' / 'note' / 'docs'
    index_path = docs_dir / 'index.md'
    
    if not docs_dir.exists():
        print(f"错误: 找不到目录 {docs_dir}")
        return
    
    if not index_path.exists():
        print(f"错误: 找不到文件 {index_path}")
        return
    
    # 统计信息
    note_count = count_markdown_files(docs_dir)
    category_count = count_categories(docs_dir)
    total_words = count_total_words(docs_dir)
    
    # 更新 index.md
    update_index_stats(index_path, note_count, category_count, total_words)

if __name__ == '__main__':
    main()
