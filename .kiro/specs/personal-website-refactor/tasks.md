# 实现计划: 个人网站重构

## 概述

本计划将 tarduspura.me 从单一 Hugo 站点重构为多站点架构，包括独立的 Landing Page、MkDocs 笔记站点、Hugo 博客站点等。按渐进式步骤实施，每完成一部分即可验证成果。

## 任务列表

- [x] 1. 创建项目目录结构和基础配置
  - [x] 1.1 创建新的项目目录结构
    - 创建 `sites/` 目录，包含 `landing/`、`note/`、`blog/`、`her/` 子目录
    - 创建 `scripts/` 目录用于存放构建和迁移脚本
    - 创建 `shared/` 目录用于存放共享资源（图片等）
    - _需求: 8.1, 8.2_
  
  - [x] 1.2 复制共享图片资源
    - 将 `static/images/` 复制到 `shared/images/`
    - _需求: 6.2_

- [x] 2. 创建 Landing Page
  - [x] 2.1 创建 Landing Page HTML 结构
    - 创建 `sites/landing/index.html`
    - 包含头像、背景、导航链接、社交链接
    - 导航链接：Note、Blog、Project、Her、About、Link
    - 社交链接：GitHub、Email
    - _需求: 1.1, 1.3, 1.4, 1.5, 1.6, 1.7_
  
  - [x] 2.2 创建 Landing Page 样式
    - 创建 `sites/landing/css/style.css`
    - 实现简约现代的视觉风格
    - 实现响应式布局
    - _需求: 1.2_
  
  - [x] 2.3 添加占位图片和说明
    - 创建 `sites/landing/assets/` 目录
    - 添加 README 说明用户需要放置 `avatar.jpg` 和 `background.jpg`
    - _需求: 9.4_

- [x] 3. 检查点 - Landing Page 完成
  - 确保 Landing Page 可以在本地预览
  - 确认所有导航链接结构正确
  - 询问用户是否有问题

- [x] 4. 搭建 Note 站点（MkDocs）
  - [x] 4.1 初始化 MkDocs 项目
    - 创建 `sites/note/mkdocs.yml` 配置文件
    - 配置 Material for MkDocs 主题
    - 配置 LaTeX 支持（pymdownx.arithmatex + MathJax）
    - 配置中文搜索
    - _需求: 2.1, 2.2, 2.6_
  
  - [x] 4.2 创建内容迁移脚本
    - 创建 `scripts/migrate_notes.py`
    - 迁移 `content/posts/` 到 `sites/note/docs/`
    - 保持目录结构（Article、Courses、Tech、Others）
    - 更新图片引用路径
    - _需求: 2.3, 6.1, 6.4_
  
  - [ ]* 4.3 编写内容迁移完整性测试
    - **Property 1: 内容迁移完整性**
    - **验证: 需求 2.3, 3.3, 3.4, 4.1**
  
  - [x] 4.4 创建 Note 站点首页
    - 创建 `sites/note/docs/index.md`
    - 添加笔记分类导航
    - _需求: 2.4_

- [x] 5. 检查点 - Note 站点完成
  - 运行 `mkdocs serve` 验证站点
  - 确认 LaTeX 公式正确渲染
  - 确认搜索功能正常
  - 询问用户是否有问题

- [x] 6. 搭建 Blog 站点（Hugo）
  - [x] 6.1 初始化 Hugo 项目
    - 创建 `sites/blog/` Hugo 项目结构
    - 创建 `config.toml` 配置文件
    - 配置 baseURL 为 `/blog`
    - 配置搜索功能
    - _需求: 3.1, 3.6_
  
  - [x] 6.2 安装和配置主题
    - 添加 hugo-paper 或 hugo-theme-stack 主题
    - 配置温和的阅读风格
    - _需求: 3.2_
  
  - [x] 6.3 创建 Blog 内容迁移脚本
    - 创建 `scripts/migrate_blog.py`
    - 迁移 `content/travel/` 到 `sites/blog/content/touch/`
    - 迁移 `content/contemplate/` 到 `sites/blog/content/idea/`
    - 更新图片引用路径
    - _需求: 3.3, 3.4, 6.1, 6.4_
  
  - [x] 6.4 创建分类导航
    - 创建 Touch 和 Idea 分类索引页
    - 配置菜单导航
    - _需求: 3.7_
  
  - [x] 6.5 迁移静态页面
    - 迁移 `content/about.md` 到 `sites/blog/content/about.md`
    - 迁移 `content/links.md` 到 `sites/blog/content/link.md`
    - 迁移 `content/projects/` 到 `sites/blog/content/project.md`
    - _需求: 5.1, 5.2, 5.3_

- [x] 7. 检查点 - Blog 站点完成
  - 运行 `hugo server` 验证站点
  - 确认 Touch 和 Idea 分类正确显示
  - 确认搜索功能正常
  - 询问用户是否有问题

- [x] 8. 搭建 Her 站点（Hugo）
  - [x] 8.1 初始化 Her Hugo 项目
    - 创建 `sites/her/` Hugo 项目结构
    - 复用 Blog 站点的主题配置
    - 配置 baseURL 为 `/her`
    - 配置搜索功能
    - _需求: 4.2, 4.3_
  
  - [x] 8.2 创建 Her 内容迁移脚本
    - 创建 `scripts/migrate_her.py`
    - 迁移 `content/her/` 到 `sites/her/content/`
    - 保持子目录结构（location、restaurant、things）
    - 更新图片引用路径
    - _需求: 4.1, 6.1, 6.4_
  
  - [x] 8.3 添加 Cloudflare 访问限制说明
    - 创建 `sites/her/CLOUDFLARE_ACCESS.md`
    - 说明如何配置 Cloudflare Access 保护该路径
    - _需求: 4.4_

- [x] 9. 检查点 - Her 站点完成
  - 运行 `hugo server` 验证站点
  - 确认所有内容正确迁移
  - 确认搜索功能正常
  - 询问用户是否有问题

- [x] 10. 创建构建和部署配置
  - [x] 10.1 创建主构建脚本
    - 创建 `scripts/build.sh`
    - 按顺序构建所有站点
    - 合并输出到 `public/` 目录
    - 复制共享图片资源
    - _需求: 8.1, 8.2_
  
  - [x] 10.2 创建 GitHub Actions 工作流
    - 创建 `.github/workflows/deploy.yml`
    - 配置 Python 环境（MkDocs）
    - 配置 Hugo 环境
    - 配置 GitHub Pages 部署
    - _需求: 8.3_
  
  - [ ]* 10.3 编写图片引用完整性测试
    - **Property 2: 图片引用完整性**
    - **验证: 需求 6.1, 6.2, 6.3, 6.4**
  
  - [ ]* 10.4 编写导航链接有效性测试
    - **Property 3: 导航链接有效性**
    - **验证: 需求 1.5, 1.8, 8.2, 8.4**

- [x] 11. 最终检查点 - 完整构建测试
  - 运行完整构建脚本
  - 验证 `public/` 目录结构正确
  - 验证所有 URL 路径可访问
  - 验证图片资源正确加载
  - 询问用户是否准备部署

## 注意事项

- 标记 `*` 的任务为可选测试任务，可跳过以加快 MVP 进度
- 每个检查点都会暂停并询问用户反馈
- 用户需要自行准备头像图片（avatar.jpg）和背景图片（background.jpg），放置在 `sites/landing/assets/` 目录
- Her 站点的 Cloudflare 访问限制需要用户在 Cloudflare 控制台手动配置
