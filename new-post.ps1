# 快速创建新文章脚本
# 用法: .\new-post.ps1 -type posts -name "文章标题"
# 类型: posts, travel, her, contemplate, projects, guide

param(
    [Parameter(Mandatory=$true)]
    [ValidateSet("posts", "travel", "her", "contemplate", "projects", "guide")]
    [string]$type,
    
    [Parameter(Mandatory=$true)]
    [string]$name,
    
    [string]$subfolder = ""
)

$date = Get-Date -Format "yyyy-MM-dd"
$datetime = Get-Date -Format "yyyy-MM-ddTHH:mm:sszzz"

# 生成文件名（移除特殊字符）
$filename = $name -replace '[^\w\s-]', '' -replace '\s+', '-'
$filename = "$date-$filename.md"

# 构建路径
if ($subfolder) {
    $path = "content/$type/$subfolder/$filename"
} else {
    $path = "content/$type/$filename"
}

# 根据类型设置不同的模板
$template = @"
---
title: "$name"
date: $datetime
draft: false
"@

switch ($type) {
    "posts" {
        $template += @"

tags: []
categories: []
math: false
---

"@
    }
    "travel" {
        $template += @"

location: ""
---

"@
    }
    "her" {
        $template += @"

---

"@
    }
    default {
        $template += @"

---

"@
    }
}

# 创建目录（如果不存在）
$dir = Split-Path $path -Parent
if (!(Test-Path $dir)) {
    New-Item -ItemType Directory -Path $dir -Force | Out-Null
}

# 创建文件
$template | Out-File -FilePath $path -Encoding utf8

Write-Host "✅ 创建成功: $path" -ForegroundColor Green
Write-Host "📝 现在可以编辑文章了！" -ForegroundColor Cyan
