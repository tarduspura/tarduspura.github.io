#!/usr/bin/env python3
"""自动更新 Note 站点统计信息和时间线"""

import os
from pathlib import Path
import re
import subprocess

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
        return
    with open(main_html, 'r', encoding='utf-8') as f:
        content = f.read()
    content = re.sub(
        r'<span class="tp-hero__stat">\d+\S* 篇笔记</span>',
        f'<span class="tp-hero__stat">{note_count} 篇笔记</span>',
        content
    )
    content = re.sub(
        r'<span class="tp-hero__stat">[\d.]+\S* 字</span>',
        f'<span class="tp-hero__stat">{word_count_str} 字</span>',
        content
    )
    with open(main_html, 'w', encoding='utf-8') as f:
        f.write(content)

def generate_changelog(docs_dir, project_root):
    """从 git log 自动生成时间线"""
    try:
        result = subprocess.run(
            ['git', 'log', '--pretty=format:%ai|%s', '-50'],
            capture_output=True, text=True, cwd=project_root,
            encoding='utf-8', errors='replace'
        )
        if result.returncode != 0:
            print("⚠ git log 失败，跳过时间线生成")
            return
    except Exception as e:
        print(f"⚠ git 命令异常: {e}")
        return

    lines = [
        '---', 'title: 更新时间线', 'hide:', '  - navigation', '  - toc',
        '---', '', '# 更新时间线', '', '<div class="tp-timeline">', ''
    ]

    seen = set()
    for raw_line in result.stdout.strip().split('\n'):
        if '|' not in raw_line:
            continue
        parts = raw_line.split('|', 1)
        if len(parts) != 2:
            continue
        date = parts[0].strip()[:10]
        msg = parts[1].strip()

        # 跳过无意义的 commit
        if not msg or msg.startswith('Merge') or msg.startswith('Initial'):
            continue

        key = f"{date}:{msg}"
        if key in seen:
            continue
        seen.add(key)

        lines.append('<div class="tp-timeline__item">')
        lines.append(f'<div class="tp-timeline__date">{date}</div>')
        lines.append(f'<div class="tp-timeline__content">')
        lines.append(f'<h3>{msg}</h3>')
        lines.append('</div>')
        lines.append('</div>')
        lines.append('')

        if len(seen) >= 20:
            break

    lines.append('</div>')

    changelog_path = os.path.join(docs_dir, 'changelog.md')
    with open(changelog_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

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
    generate_changelog(docs_dir, project_root)

    print(f"✓ 统计: {note_count} 篇, {word_count:,} 字 ({word_count_str})")
    print(f"✓ 时间线已自动生成")

if __name__ == '__main__':
    main()
