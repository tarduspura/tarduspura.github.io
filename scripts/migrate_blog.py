#!/usr/bin/env python3
"""
Blog 内容迁移脚本
将 content/travel/ 迁移到 sites/blog/content/touch/
将 content/contemplate/ 迁移到 sites/blog/content/idea/
"""

import os
import shutil
import re
from pathlib import Path

# 项目根目录
ROOT_DIR = Path(__file__).parent.parent

# 源目录和目标目录映射
MIGRATIONS = [
    {
        'source': ROOT_DIR / 'content' / 'travel',
        'target': ROOT_DIR / 'sites' / 'blog' / 'content' / 'touch',
        'name': 'Touch (旅行&户外)'
    },
    {
        'source': ROOT_DIR / 'content' / 'contemplate',
        'target': ROOT_DIR / 'sites' / 'blog' / 'content' / 'idea',
        'name': 'Idea (沉思)'
    }
]

def update_image_paths(content: str) -> str:
    """更新图片路径，确保使用 /images/ 前缀"""
    # 图片路径已经是 /images/xxx.jpg 格式，保持不变
    return content

def migrate_file(src_file: Path, dst_file: Path):
    """迁移单个文件"""
    # 确保目标目录存在
    dst_file.parent.mkdir(parents=True, exist_ok=True)
    
    # 读取源文件
    with open(src_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 更新图片路径
    content = update_image_paths(content)
    
    # 写入目标文件
    with open(dst_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"  ✓ {src_file.name} -> {dst_file}")

def migrate_directory(source: Path, target: Path, name: str):
    """迁移整个目录"""
    print(f"\n迁移 {name}:")
    print(f"  源: {source}")
    print(f"  目标: {target}")
    
    if not source.exists():
        print(f"  ⚠ 源目录不存在，跳过")
        return
    
    # 遍历源目录
    for src_path in source.rglob('*.md'):
        # 计算相对路径
        rel_path = src_path.relative_to(source)
        dst_path = target / rel_path
        
        # 跳过 _index.md（我们已经手动创建了）
        if src_path.name == '_index.md' and src_path.parent == source:
            print(f"  - 跳过根 _index.md（已手动创建）")
            continue
        
        migrate_file(src_path, dst_path)

def main():
    print("=" * 50)
    print("Blog 内容迁移脚本")
    print("=" * 50)
    
    for migration in MIGRATIONS:
        migrate_directory(
            migration['source'],
            migration['target'],
            migration['name']
        )
    
    print("\n" + "=" * 50)
    print("迁移完成！")
    print("=" * 50)

if __name__ == '__main__':
    main()
