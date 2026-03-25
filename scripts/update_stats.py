#!/usr/bin/env python3
"""自动更新 Note 站点统计信息"""

import os
from pathlib import Path
import re

def count_markdown_files(docs_dir):
    count = 0
    for root, dirs, files in os.walk(docs_dir):
        dirs[:] = [d for d in dirs if d not in ('stylesheets', 'javascripts', 'images')]
        for f in files:
            if f.endswith('.md') and f not in ('index.md', 'changelog.md'):
                count += 1
    return count

def count_total_words(docs_dir):
    total = 0
    for root, dirs, files in os.walk(docs_dir):
        dirs[:] = [d for d in dirs if d not in ('stylesheets', 'javascripts', 'images')]
        for f in files:
            if f.endswith('.md') and f not in ('index.md', 'changelog.md'):
                path = os.path.join(root, f)
                with open(path, 'r', encoding='utf-8') as fh:
                    content = fh.read()
                    content = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)
                    chinese = len(re.findall(r'[\u4e00-\u9fff]', content))
                    english = len(re.findall(r'\b[a-zA-Z]+\b', content))
                    total += chinese + english
    return total

def format_word_count(count):
    if count >= 10000:
        return f"{count / 10000:.1f}w"
    elif count >= 1000:
        return f"{count / 1000:.1f}k"
    return str(count)

def update_main_html(overrides_dir, note_count, word_count_str):
    main_html = os.path.join(overrides_dir, 'main.html')
    if not os.path.exists(main_html):
        print(f"⚠ 找不到 {main_html}")
        return
    with open(main_html, 'r', encoding='utf-8') as f:
        content = f.read()
    # 更新笔记数
    content = re.sub(
        r'(<span class="tp-stats__number">)\d+k?w?(</span>\s*<span class="tp-stats__label">篇笔记)',
        rf'\g<1>{note_count}\2',
        content
    )
    # 更新字数
    content = re.sub(
        r'(<span class="tp-stats__number">)[\d.]+k?w?(</span>\s*<span class="tp-stats__label">总字数)',
        rf'\g<1>{word_count_str}\2',
        content
    )
    with open(main_html, 'w', encoding='utf-8') as f:
        f.write(content)

def main():
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    docs_dir = project_root / 'sites' / 'note' / 'docs'
    overrides_dir = project_root / 'sites' / 'note' / 'overrides'

    if not docs_dir.exists():
        print(f"错误: 找不到目录 {docs_dir}")
        return

    note_count = count_markdown_files(docs_dir)
    word_count = count_total_words(docs_dir)
    word_count_str = format_word_count(word_count)

    update_main_html(overrides_dir, note_count, word_count_str)

    print(f"✓ 统计信息已更新:")
    print(f"  - 笔记总数: {note_count} 篇")
    print(f"  - 总字数: {word_count:,} 字 ({word_count_str})")

if __name__ == '__main__':
    main()
