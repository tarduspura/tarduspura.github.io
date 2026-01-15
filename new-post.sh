#!/bin/bash
# 快速创建新文章脚本 (Linux/WSL 版本)
# 用法: ./new-post.sh <类型> <标题> [子目录]
# 类型: posts, travel, her, contemplate, projects, guide
# 示例: ./new-post.sh posts "我的新文章"
# 示例: ./new-post.sh posts "密码学笔记" "Courses/crypto"

if [ $# -lt 2 ]; then
    echo "用法: ./new-post.sh <类型> <标题> [子目录]"
    echo "类型: posts, travel, her, contemplate, projects, guide"
    echo "示例: ./new-post.sh posts \"我的新文章\""
    exit 1
fi

TYPE=$1
TITLE=$2
SUBFOLDER=${3:-""}

DATE=$(date +%Y-%m-%d)
DATETIME=$(date +%Y-%m-%dT%H:%M:%S%z)

# 生成文件名
FILENAME=$(echo "$TITLE" | sed 's/[^a-zA-Z0-9\u4e00-\u9fa5 -]//g' | sed 's/ /-/g')
FILENAME="$DATE-$FILENAME.md"

# 构建路径
if [ -n "$SUBFOLDER" ]; then
    FILEPATH="content/$TYPE/$SUBFOLDER/$FILENAME"
    mkdir -p "content/$TYPE/$SUBFOLDER"
else
    FILEPATH="content/$TYPE/$FILENAME"
    mkdir -p "content/$TYPE"
fi

# 创建文章
cat > "$FILEPATH" << EOF
---
title: "$TITLE"
date: $DATETIME
draft: false
---

EOF

echo "✅ 创建成功: $FILEPATH"
echo "📝 现在可以编辑文章了！"
