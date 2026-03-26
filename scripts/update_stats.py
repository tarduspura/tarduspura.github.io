#!/usr/bin/env python3
"""自动更新 Note 站点统计信息和时间线"""

import os
from pathlib import Path
import re
import subprocess
from datetime import datetime

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

def get_git_file_changes(project_root):
    """从 git log 获取最近的文件变更"""
    try:
        result = subprocess.run(
            ['git', 'log', '--diff-filter=AM', '--name-only',
             '--pretty=format:%H|%ai|%s', '-30', '--', 'sites/note/docs/'],
            capture_output=True, text=True, cwd=project_root, encoding='utf-8', errors='replace'
        )
        if result.returncode != 0:
            return []
        entries = []
        current_commit = None
        for line in result.stdout.strip().split('\n'):
            if '|' in line and not line.startswith('sites/'):
                parts = line.split('|', 2)
                if len(parts) == 3:
                    current_commit = {
                        'date': parts[1].strip()[:10],
                        'msg': parts[2].strip(),
                        'files': []
                    }
            elif line.startswith('sites/note/docs/') and line.endswith('.md'):
                if current_commit and line not in ('sites/note/docs/index.md', 'sites/note/docs/changelog.md'):
                    current_commit['files'].append(line)
                    if current_commit not in entries:
                        entries.append(current_commit)
        return entries
    except Exception:
        return []

def generate_changelog(docs_dir, project_root):
    """自动生成时间线"""
    entries = get_git_file_changes(project_root)
    if not entries:
        return

    lines = [
        '---',
        'title: 更新时间线',
        'hide:',
        '  - navigation',
        '  - toc',
        '---',
        '',
        '# 更新时间线',
        '',
        '<div class="tp-timeline">',
        ''
    ]

    seen_dates = set()
    for entry in entries:
        date = entry['date']
        msg = entry['msg']
        if date in seen_dates:
            continue
        seen_dates.add(date)

        file_names = [os.path.basename(f).replace('.md', '') for f in entry['files'][:3]]
        desc = ', '.join(file_names) if file_names else ''

        lines.append(f'<div class="tp-timeline__item">')
        lines.append(f'<div class="tp-timeline__date">{date}</div>')
        lines.append(f'<div class="tp-timeline__content">')
        lines.append(f'<h3>{msg}</h3>')
        if desc:
            lines.append(f'<p>{desc}</p>')
        lines.append(f'</div>')
        lines.append(f'</div>')
        lines.append('')

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
