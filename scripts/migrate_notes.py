#!/usr/bin/env python3
"""
笔记内容迁移脚本
将 content/posts/ 目录下的笔记迁移到 sites/note/docs/
"""

import os
import shutil
import re
from pathlib import Path

# 源目录和目标目录
SOURCE_DIR = Path("content/posts")
TARGET_DIR = Path("sites/note/docs")

# 需要跳过的文件
SKIP_FILES = {"_index.md"}

def update_image_paths(content: str) -> str:
    """更新图片引用路径"""
    # 将 /images/xxx.jpg 替换为 /images/xxx.jpg (保持不变，因为会部署到根目录)
    # MkDocs 中使用绝对路径
    return content

def update_frontmatter(content: str) -> str:
    """更新 front matter 格式以适配 MkDocs"""
    # Hugo 的 front matter 格式基本兼容 MkDocs
    # 移除 Hugo 特有的字段
    content = re.sub(r'^ShowToc:\s*true\s*$', '', content, flags=re.MULTILINE)
    content = re.sub(r'^draft:\s*false\s*$', '', content, flags=re.MULTILINE)
    return content

def migrate_file(src_path: Path, dst_path: Path):
    """迁移单个文件"""
    print(f"  迁移: {src_path} -> {dst_path}")
    
    # 确保目标目录存在
    dst_path.parent.mkdir(parents=True, exist_ok=True)
    
    # 读取源文件
    with open(src_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 更新内容
    content = update_image_paths(content)
    content = update_frontmatter(content)
    
    # 写入目标文件
    with open(dst_path, 'w', encoding='utf-8') as f:
        f.write(content)

def migrate_directory(src_dir: Path, dst_dir: Path):
    """递归迁移目录"""
    if not src_dir.exists():
        print(f"源目录不存在: {src_dir}")
        return
    
    for item in src_dir.iterdir():
        if item.name in SKIP_FILES:
            continue
            
        if item.is_file() and item.suffix == '.md':
            # 迁移 markdown 文件
            dst_path = dst_dir / item.name
            migrate_file(item, dst_path)
        elif item.is_dir():
            # 递归处理子目录
            migrate_directory(item, dst_dir / item.name)

def create_index_files():
    """创建各分类的索引文件"""
    categories = {
        "Article": "文章",
        "Courses": "课程笔记", 
        "Tech": "技术",
        "Others": "其他"
    }
    
    for eng_name, cn_name in categories.items():
        index_path = TARGET_DIR / eng_name / "index.md"
        index_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 获取该目录下的所有 md 文件
        files = []
        dir_path = TARGET_DIR / eng_name
        if dir_path.exists():
            for f in dir_path.iterdir():
                if f.is_file() and f.suffix == '.md' and f.name != 'index.md':
                    files.append(f.stem)
        
        content = f"""---
title: {cn_name}
---

# {cn_name}

"""
        if files:
            for f in files:
                content += f"- [{f}]({f}.md)\n"
        else:
            content += "暂无内容\n"
        
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  创建索引: {index_path}")

def main():
    print("开始迁移笔记内容...")
    print(f"源目录: {SOURCE_DIR}")
    print(f"目标目录: {TARGET_DIR}")
    print()
    
    # 确保目标目录存在
    TARGET_DIR.mkdir(parents=True, exist_ok=True)
    
    # 迁移内容
    migrate_directory(SOURCE_DIR, TARGET_DIR)
    
    # 创建索引文件
    print("\n创建索引文件...")
    create_index_files()
    
    print("\n迁移完成!")

if __name__ == "__main__":
    main()
