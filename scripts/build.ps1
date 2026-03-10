# 多站点构建脚本 (PowerShell)
# 将 Landing Page、Note、Blog、Her 站点合并到 public/ 目录

$ErrorActionPreference = "Stop"

Write-Host "🚀 开始构建多站点..." -ForegroundColor Cyan

# 清理旧的构建目录
if (Test-Path "public") {
    Remove-Item -Recurse -Force "public"
}
New-Item -ItemType Directory -Path "public" -Force | Out-Null

# 1. 构建 Landing Page（复制静态文件到根目录）
Write-Host "📄 构建 Landing Page..." -ForegroundColor Yellow
Copy-Item -Recurse -Path "sites/landing/*" -Destination "public/" -Force
# 移除不需要的文件
Remove-Item -Path "public/assets/README.md" -ErrorAction SilentlyContinue

# 2. 构建 Note 站点（MkDocs）
Write-Host "📚 构建 Note 站点..." -ForegroundColor Yellow
Push-Location "sites/note"
try {
    mkdocs build --site-dir "../../public/note"
} finally {
    Pop-Location
}

# 3. 构建 Blog 站点（Hugo）
Write-Host "✍️ 构建 Blog 站点..." -ForegroundColor Yellow
Push-Location "sites/blog"
try {
    hugo --minify --baseURL "/blog/" -d "../../public/blog"
} finally {
    Pop-Location
}

# 4. 构建 Her 站点（Hugo）
Write-Host "💕 构建 Her 站点..." -ForegroundColor Yellow
Push-Location "sites/her"
try {
    hugo --minify --baseURL "/her/" -d "../../public/her"
} finally {
    Pop-Location
}

# 5. 复制共享资源
Write-Host "🖼️ 复制共享资源..." -ForegroundColor Yellow
if (Test-Path "shared/images") {
    Copy-Item -Recurse -Path "shared/images" -Destination "public/images" -Force -ErrorAction SilentlyContinue
}

# 6. 创建 CNAME 文件（如果需要自定义域名）
"tarduspura.me" | Out-File -FilePath "public/CNAME" -Encoding ASCII -NoNewline

Write-Host ""
Write-Host "✅ 构建完成！输出目录: public/" -ForegroundColor Green
Write-Host ""
Write-Host "目录结构:" -ForegroundColor Cyan
Write-Host "  public/           - Landing Page (根目录)"
Write-Host "  public/note/      - Note 站点 (MkDocs)"
Write-Host "  public/blog/      - Blog 站点 (Hugo)"
Write-Host "  public/her/       - Her 站点 (Hugo)"
