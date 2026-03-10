# Tardus Pura 个人网站

## 网站架构

```
tarduspura.me/           → Landing Page (静态HTML)
├── /about/              → 关于页面
├── /project/            → 项目展示
├── /link/               → 友情链接
├── /note/               → 笔记站点 (MkDocs)
├── /blog/               → 博客站点 (Hugo + PaperMod)
├── /her/                → Her站点 (Hugo + Blowfish)
```

## 目录结构

```
personal-site/
├── .github/workflows/deploy.yml    # GitHub Actions 自动部署
├── sites/
│   ├── landing/                    # 主页 + About/Project/Link
│   │   ├── index.html              # 主页
│   │   ├── about/                  # 关于页面
│   │   ├── project/                # 项目页面
│   │   └── link/                   # 友链页面
│   ├── note/                       # MkDocs 笔记站点
│   │   ├── mkdocs.yml              # MkDocs 配置
│   │   └── docs/                   # 笔记内容
│   ├── blog/                       # Hugo 博客站点
│   │   ├── config.toml             # Hugo 配置
│   │   └── content/posts/          # 博客文章
│   └── her/                        # Hugo Her站点
│       ├── hugo.toml               # Hugo 配置
│       └── content/                # Her内容
└── shared/images/                  # 共享图片资源
```

---

## 如何编写新内容

### 📝 Note (笔记)

笔记使用 MkDocs，内容位于 `sites/note/docs/`

**创建新笔记：**
```
sites/note/docs/
├── index.md                    # 首页
├── 分类名/                     # 创建分类文件夹
│   ├── index.md               # 分类首页（可选）
│   └── 笔记名.md              # 笔记文件
```

**笔记格式：**
```markdown
# 笔记标题

正文内容...

## 二级标题

更多内容...
```

**图片使用：**
- 图片放在 `sites/note/docs/images/` 或对应分类下的 `images/` 文件夹
- 引用方式：`![描述](images/图片名.jpg)` 或 `![描述](../images/图片名.jpg)`

**导航配置：**
编辑 `sites/note/mkdocs.yml` 中的 `nav` 部分添加新页面

---

### 📖 Blog (博客)

博客使用 Hugo + PaperMod 主题，内容位于 `sites/blog/content/posts/`

**创建新文章：**
```
sites/blog/content/posts/
├── 分类名/
│   ├── _index.md              # 分类首页
│   └── 文章名.md              # 文章文件
```

**文章格式（Front Matter）：**
```markdown
---
title: "文章标题"
date: 2026-03-11
draft: false
tags: ["标签1", "标签2"]
categories: ["分类名"]
summary: "文章摘要"
---

正文内容...
```

**图片使用：**
- 图片放在 `sites/blog/static/images/` 或 `shared/images/`
- 引用方式：`![描述](/images/图片名.jpg)`

---

### 💕 Her

Her站点使用 Hugo + Blowfish 主题，内容位于 `sites/her/content/`

**目录结构：**
```
sites/her/content/
├── location/                   # 东西南北（去过的地方）
│   ├── _index.md              # 分类配置
│   └── 文章名.md
├── restaurant/                 # 探店ing（吃过的店）
│   ├── _index.md
│   └── 文章名.md
└── things/                     # 冥王星的石碑（做过的事）
    ├── _index.md
    └── 文章名.md
```

**文章格式：**
```markdown
---
title: "标题"
date: 2026-03-11
draft: false
---

正文内容...
```

**图片使用：**
- 图片放在 `sites/her/static/images/` 或 `shared/images/`
- 引用方式：`![描述](/her/images/图片名.jpg)` 或使用共享图片

---

## 图片管理

每个站点的图片都放在各自的目录中，构建时会自动处理到正确的路径：

| 站点 | 图片存放位置 | 引用方式 |
|------|-------------|---------|
| Note | `sites/note/docs/images/` | `![描述](../../images/图片名.jpg)` (相对路径) |
| Blog | `sites/blog/static/images/` | `![描述](/blog/images/图片名.jpg)` |
| Her | `sites/her/static/images/` | `![描述](/her/images/图片名.jpg)` |
| Landing | `sites/landing/assets/` | `<img src="assets/图片名.jpg">` |

---

## 本地预览

**Note站点：**
```bash
cd sites/note
mkdocs serve
# 访问 http://127.0.0.1:8000
```

**Blog站点：**
```bash
cd sites/blog
hugo server
# 访问 http://localhost:1313
```

**Her站点：**
```bash
cd sites/her
hugo server
# 访问 http://localhost:1313
```

---

## 部署

推送到 `main` 分支后，GitHub Actions 会自动构建并部署到 GitHub Pages。

```bash
git add -A
git commit -m "更新内容"
git push origin main
```
