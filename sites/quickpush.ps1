param(
    [Parameter(Position = 0)]
    [string]$Message
)

$ErrorActionPreference = "Stop"

function Fail([string]$text) {
    Write-Host "[ERROR] $text" -ForegroundColor Red
    exit 1
}

# Ensure we are in a git repository.
$insideRepo = git rev-parse --is-inside-work-tree 2>$null
if (-not $insideRepo -or $insideRepo.Trim() -ne "true") {
    Fail "Current directory is not a git repository."
}

if (-not $Message -or [string]::IsNullOrWhiteSpace($Message)) {
    $Message = "chore: update content $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
}

# Stage everything.
git add -A

# If there is nothing to commit after staging, stop early.
$status = git status --porcelain
if (-not $status) {
    Write-Host "Nothing to commit. Working tree is clean." -ForegroundColor Yellow
    exit 0
}

# Commit and push.
git commit -m "$Message"

$branch = (git branch --show-current).Trim()
if (-not $branch) {
    Fail "Could not detect current branch."
}

$upstream = git rev-parse --abbrev-ref --symbolic-full-name "@{u}" 2>$null
if ($LASTEXITCODE -ne 0 -or -not $upstream) {
    git push --set-upstream origin $branch
} else {
    git push
}

Write-Host "Done: add + commit + push completed." -ForegroundColor Green
