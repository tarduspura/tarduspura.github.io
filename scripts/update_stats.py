#!/usr/bin/env python3
"""自动更新 Note 站点统计信息"""

import os
from pathlib import Path
import re

def count_markdown_files(docs_dir):
    count = 0
    for root, dirs, files in os.walk(docs_dir):
        # 排除非内容目录
        dirs[:] = [d for d in dirs if d not in ('stylesheets', 'javascripts', 'images')]
        for f in files:
            if f.endswith('.md') and f != 'index.md':
                count += 1
    return count

def count_total_words(docs_dir):
    total = 0
    for root, dirs, files in os.walk(docs_dir):
        dirs[:] = [d for d in dirs if d not in ('stylesheets', 'javascripts', 'images')]
        for f in files:
            if f.endswith('.md') and f != 'index.md':
                path = os.path.join(root, f)
                with open(path, 'r', encoding='utf-8') as fh:
                    content = fh.read()
                    content = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)
                    chinese = len(re.findall(r'[\u4e00-\u9fff]', content))
                    english = len(re.findall(r'\b[a-zA-Z]+\b', content))
                    total += chinese + english
    return total

def create_stats_override(overrides_dir, note_count, word_count):
    """创建 overrides/partials/meta.html 注入统计 meta 标签"""
    partials_dir = os.path.join(overrides_dir, 'partials')
    os.makedirs(partials_dir, exist_ok=True)
    # 不覆盖 meta.html，而是创建一个 hooks 可用的文件
    # 直接更新 home-stats.js 中的数据
    pass

def update_home_stats_js(docs_dir, note_count, word_count):
    """更新 home-stats.js 中的 fallback 数据"""
    js_path = os.path.join(docs_dir, 'javascripts', 'home-stats.js')
    content = f"""// 主页统计数据（由 update_stats.py 在构建时自动更新）
document.addEventListener('DOMContentLoaded', function() {{
  var noteEl = document.getElementById('tp-note-count');
  var wordEl = document.getElementById('tp-word-count');
  if (noteEl) noteEl.textContent = '{note_count}';
  if (wordEl) wordEl.textContent = '{word_count:,}';
}});
"""
    with open(js_path, 'w', encoding='utf-8') as f:
        f.write(content)

def main():
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    docs_dir = project_root / 'sites' / 'note' / 'docs'

    if not docs_dir.exists():
        print(f"错误: 找不到目录 {docs_dir}")
        return

    note_count = count_markdown_files(docs_dir)
    word_count = count_total_words(docs_dir)

    update_home_stats_js(docs_dir, note_count, word_count)

    print(f"✓ 统计信息已更新:")
    print(f"  - 笔记总数: {note_count} 篇")
    print(f"  - 总字数: {word_count:,} 字")

if __name__ == '__main__':
    main()
