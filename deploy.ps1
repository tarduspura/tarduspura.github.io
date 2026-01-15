# 一键部署脚本 (Windows PowerShell)
# 用法: .\deploy.ps1 "提交信息"
# 示例: .\deploy.ps1 "新增文章"

param(
    [Parameter(Mandatory=$true)]
    [string]$message
)

Write-Host "添加所有更改..." -ForegroundColor Cyan
git add .

Write-Host "提交: $message" -ForegroundColor Cyan
git commit -m $message

Write-Host "推送到远程..." -ForegroundColor Cyan
git push

Write-Host "部署完成！" -ForegroundColor Green
