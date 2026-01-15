#!/bin/bash
# 一键部署脚本 (WSL/Linux)
# 用法: ./deploy.sh "提交信息"
# 示例: ./deploy.sh "新增文章"

if [ -z "$1" ]; then
    echo "❌ 请提供提交信息"
    echo "用法: ./deploy.sh \"提交信息\""
    exit 1
fi

echo "📦 添加所有更改..."
git add .

echo "📝 提交: $1"
git commit -m "$1"

echo "🚀 推送到远程..."
git push

echo "✅ 部署完成！"
