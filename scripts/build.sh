#!/bin/bash
# 多站点构建脚本
# 将 Landing Page、Note、Blog、Her 站点合并到 public/ 目录

set -e

echo "🚀 开始构建多站点..."

# 清理旧的构建目录
rm -rf public
mkdir -p public

# 1. 构建 Landing Page（复制静态文件到根目录）
echo "📄 构建 Landing Page..."
cp -r sites/landing/* public/
# 移除不需要的文件
rm -f public/assets/README.md 2>/dev/null || true

# 2. 构建 Note 站点（MkDocs）
echo "📚 构建 Note 站点..."
cd sites/note
mkdocs build --site-dir ../../public/note
cd ../..

# 3. 构建 Blog 站点（Hugo）
echo "✍️ 构建 Blog 站点..."
cd sites/blog
hugo --minify --baseURL "/blog/" -d ../../public/blog
cd ../..

# 4. 构建 Her 站点（Hugo）
echo "💕 构建 Her 站点..."
cd sites/her
hugo --minify --baseURL "/her/" -d ../../public/her
cd ../..

# 5. 复制共享资源
echo "🖼️ 复制共享资源..."
if [ -d "shared/images" ]; then
  cp -r shared/images public/images 2>/dev/null || true
fi

# 6. 创建 CNAME 文件（如果需要自定义域名）
echo "tarduspura.me" > public/CNAME

echo "✅ 构建完成！输出目录: public/"
echo ""
echo "目录结构:"
echo "  public/           - Landing Page (根目录)"
echo "  public/note/      - Note 站点 (MkDocs)"
echo "  public/blog/      - Blog 站点 (Hugo)"
echo "  public/her/       - Her 站点 (Hugo)"
