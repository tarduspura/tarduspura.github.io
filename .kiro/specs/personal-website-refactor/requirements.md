# 需求文档

## 简介

本文档描述了 tarduspura.me 个人网站的重构需求。当前网站基于 Hugo + PaperMod 主题构建，存在主页展示不清晰、笔记不支持 LaTeX、栏目索引混乱、阅读体验欠佳等问题。重构目标是创建一个简约现代的个人展示主页，并将内容按技术栈分离，提升整体用户体验。

## 术语表

- **Landing_Page（主页）**：访问 tarduspura.me 时首先看到的独立个人展示页面
- **Note（笔记）**：技术学习笔记板块，使用 MkDocs 构建，支持 LaTeX 公式渲染
- **Blog（博客）**：包含 Touch（旅行/户外）和 Idea（沉思/创作）内容的博客板块
- **Her（她）**：私人板块，记录与特定人相关的内容，需支持访问限制
- **Project（项目）**：个人项目展示板块
- **About（关于）**：个人介绍页面
- **Link（友链）**：友情链接页面
- **Hugo**：静态网站生成器
- **MkDocs**：基于 Python 的静态文档生成器，原生支持 LaTeX
- **Cloudflare**：CDN 和安全服务提供商，用于添加访问限制

## 需求

### 需求 1：Landing Page（主页）

**用户故事：** 作为访客，我希望访问 tarduspura.me 时看到一个简约现代的个人展示页面，以便快速了解站长并导航到各个板块。

#### 验收标准

1. WHEN 访客访问 tarduspura.me THEN Landing_Page SHALL 显示一个独立的个人展示页面
2. THE Landing_Page SHALL 采用简约、现代的视觉风格
3. THE Landing_Page SHALL 展示个人头像图片
4. THE Landing_Page SHALL 展示背景图片或背景效果
5. THE Landing_Page SHALL 提供导航链接跳转到以下板块：Note、Blog、Project、Her、About、Link
6. THE Landing_Page SHALL 提供外部链接跳转到 GitHub 主页（https://github.com/tarduspura）
7. THE Landing_Page SHALL 提供邮箱联系方式（tarduspura@gmail.com）
8. WHEN 用户点击任意导航链接 THEN Landing_Page SHALL 正确跳转到对应页面

### 需求 2：技术栈分离 - Note 板块

**用户故事：** 作为站长，我希望笔记板块使用 MkDocs 构建，以便获得原生的 LaTeX 公式支持和更好的文档阅读体验。

#### 验收标准

1. THE Note_System SHALL 使用 MkDocs 框架构建
2. THE Note_System SHALL 支持 LaTeX 数学公式的正确渲染
3. THE Note_System SHALL 包含现有 posts 目录下的所有笔记内容
4. THE Note_System SHALL 部署在 tarduspura.me/note 路径下
5. WHEN 用户访问笔记页面 THEN Note_System SHALL 正确显示所有数学公式
6. THE Note_System SHALL 提供站内搜索功能

### 需求 3：技术栈分离 - Blog 板块

**用户故事：** 作为站长，我希望博客板块使用温和、适合文字阅读的主题，以便提供更好的阅读体验。

#### 验收标准

1. THE Blog_System SHALL 使用 Hugo 框架构建
2. THE Blog_System SHALL 采用温和、适合长文阅读的主题风格
3. THE Blog_System SHALL 包含现有 travel（Touch）目录下的所有内容
4. THE Blog_System SHALL 包含现有 contemplate（Idea）目录下的所有内容
5. THE Blog_System SHALL 部署在 tarduspura.me/blog 路径下
6. THE Blog_System SHALL 提供站内搜索功能
7. WHEN 用户浏览博客文章 THEN Blog_System SHALL 提供清晰的分类导航（Touch/Idea）

### 需求 4：Her 板块

**用户故事：** 作为站长，我希望 Her 板块保持独立并支持访问限制，以便保护私人内容。

#### 验收标准

1. THE Her_System SHALL 保留现有 her 目录下的所有内容
2. THE Her_System SHALL 部署在 tarduspura.me/her 路径下
3. THE Her_System SHALL 提供站内搜索功能
4. THE Her_System SHALL 支持通过 Cloudflare 添加访问限制的能力
5. WHEN Cloudflare 访问限制启用后 THEN Her_System SHALL 仅允许授权用户访问

### 需求 5：Project、About、Link 板块

**用户故事：** 作为站长，我希望项目、关于、友链页面有合适的展示方式，以便访客了解我的项目和联系方式。

#### 验收标准

1. THE Project_Page SHALL 展示现有 projects 目录下的所有项目内容
2. THE About_Page SHALL 展示现有 about.md 的个人介绍内容
3. THE Link_Page SHALL 展示现有 links.md 的友链内容
4. THE Project_Page SHALL 部署在 tarduspura.me/project 路径下
5. THE About_Page SHALL 部署在 tarduspura.me/about 路径下
6. THE Link_Page SHALL 部署在 tarduspura.me/link 路径下

### 需求 6：内容迁移与图片引用

**用户故事：** 作为站长，我希望重构后所有文章的图片引用关系保持正确，以便内容正常显示。

#### 验收标准

1. WHEN 内容迁移完成后 THEN System SHALL 保持所有文章与图片的引用关系
2. THE System SHALL 确保 static/images 目录下的所有图片在新架构中可正常访问
3. WHEN 用户浏览任意文章 THEN System SHALL 正确渲染所有引用的图片
4. IF 图片引用路径需要调整 THEN System SHALL 自动更新文章中的图片路径

### 需求 7：搜索功能

**用户故事：** 作为访客，我希望在 Blog、Note、Her 板块内能够搜索内容，以便快速找到感兴趣的文章。

#### 验收标准

1. THE Blog_System SHALL 提供全文搜索功能
2. THE Note_System SHALL 提供全文搜索功能
3. THE Her_System SHALL 提供全文搜索功能
4. WHEN 用户输入搜索关键词 THEN System SHALL 返回匹配的文章列表
5. THE Search_Results SHALL 显示文章标题和内容摘要

### 需求 8：部署架构

**用户故事：** 作为站长，我希望网站能够正确部署并通过统一域名访问，以便访客获得一致的访问体验。

#### 验收标准

1. THE System SHALL 将 Landing_Page 部署为 tarduspura.me 的根路径
2. THE System SHALL 支持以下 URL 结构：
   - tarduspura.me/ → Landing Page
   - tarduspura.me/note → Note 板块
   - tarduspura.me/blog → Blog 板块
   - tarduspura.me/her → Her 板块
   - tarduspura.me/project → Project 页面
   - tarduspura.me/about → About 页面
   - tarduspura.me/link → Link 页面
3. THE System SHALL 支持通过 GitHub Pages 或类似静态托管服务部署
4. WHEN 用户访问任意有效 URL THEN System SHALL 返回正确的页面内容

### 需求 9：渐进式重构

**用户故事：** 作为站长，我希望重构按步骤进行，每完成一部分都能看到成果，以便及时发现和解决问题。

#### 验收标准

1. THE Refactor_Process SHALL 按以下顺序进行：
   - 第一步：创建 Landing Page
   - 第二步：搭建 Note 板块（MkDocs）
   - 第三步：搭建 Blog 板块
   - 第四步：迁移 Her 板块
   - 第五步：完成 Project、About、Link 页面
   - 第六步：配置部署和 URL 路由
2. WHEN 每个步骤完成后 THEN System SHALL 向用户汇报完成情况
3. IF 遇到不确定的问题 THEN System SHALL 先询问用户再继续
4. THE System SHALL 在适当位置提示用户自定义照片（头像、背景图）的放置位置
