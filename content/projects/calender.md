---
title: "Calender"
date: 2026-02-12T22:36:52+08:00
draft: false
ShowToc: true
---

# 医院排班系统项目综述

## 一、项目背景与目标
本项目是一个面向本地使用场景的医院门诊排班编辑工具，核心目标是：
- 快速录入并维护一周（周一到周日）上午/下午排班信息；
- 在单页可视化编辑中完成拖拽调整、修改与删除；
- 一键导出高分辨率排班图片，便于院内发布与传播；
- 提供 Windows 端桌面应用形态，降低非技术用户使用门槛。

项目在功能上强调“高效编辑 + 高质量导出 + 本地可分发”。

---

## 二、技术路线与开发环境

### 1. 技术选型详解

本项目采用 **Electron + Vue 3 + TypeScript** 的现代桌面应用技术栈，每个技术选型都有明确的问题导向：

#### 核心框架层

**Electron v39.5.2**
- **作用**：将 Web 技术（HTML/CSS/JS）封装为跨平台桌面应用的运行时框架
- **为什么选它**：需要本地文件读写能力、系统托盘、窗口管理等桌面特性，同时希望复用前端技术栈快速开发
- **核心价值**：一套代码可同时打包为 Windows/macOS/Linux 应用，且能调用 Node.js 能力（本项目用于本地数据持久化）
- **替代方案对比**：Tauri（更轻量但生态较新）、NW.js（配置复杂度高）

**Vue 3（Composition API）**
- **作用**：构建用户界面的渐进式 JavaScript 框架
- **为什么选它**：响应式数据绑定简化状态-视图同步；Composition API 让逻辑复用更清晰（如本项目的 `useWheelZoom` 自定义滚轮缩放逻辑）
- **核心特性应用**：
  - `ref/reactive`：管理缩放级别、拖拽状态、模态框状态
  - `computed`：自动计算周日期范围显示文本
  - 生命周期钩子：`onMounted` 初始化数据、绑定键盘事件
- **替代方案对比**：React（生态更大但学习曲线陡）、Svelte（编译时框架，Bundle 更小但生态较小）

**TypeScript v5.9.3**
- **作用**：JavaScript 的超集，提供静态类型检查
- **为什么选它**：排班数据结构复杂（医生、科室、时段等 8+ 字段），类型约束能在编译期拦截字段拼写错误、类型不匹配等低级 bug
- **实践收益**：定义 `Shift` 接口后，IDE 可自动提示所有可用字段，重构时能准确追踪影响范围
- **学习要点**：接口定义、泛型使用、类型推导

#### 状态与交互层

**Pinia v3.0.4**
- **作用**：Vue 官方推荐的新一代状态管理库（Vuex 的继任者）
- **为什么选它**：比 Vuex 更轻量，TypeScript 支持更友好，无需 mutations 概念（直接修改 state）
- **本项目应用**：
  - 集中管理 `shifts` 数组（所有排班数据）
  - 提供 `addShift`、`updateShift`、`removeShift` 等操作方法
  - 每次状态变更自动触发持久化到本地存储
- **学习要点**：Store 定义、组合式 API 风格（`defineStore` + `ref`）、跨组件状态共享

**vuedraggable v4.1.0**
- **作用**：基于 Sortable.js 的 Vue 拖拽组件库
- **为什么选它**：需要在同一时段列内拖拽调整医生顺序，该库提供开箱即用的拖拽排序能力
- **实践细节**：
  - 通过 `handle` 属性指定拖拽手柄（避免整个卡片都可拖拽，防止误触）
  - `@change` 事件捕获排序变化，立即同步到 Pinia Store
  - 配置 `ghost-class` 实现拖拽时的视觉反馈
- **学习要点**：双向绑定列表数组、事件处理、样式定制

#### 样式与工程化层

**Tailwind CSS v3.4.17 + PostCSS + Autoprefixer**
- **作用组合**：
  - Tailwind CSS：原子化 CSS 框架，通过工具类快速构建样式
  - PostCSS：CSS 转换工具，处理 Tailwind 指令、变量等
  - Autoprefixer：自动添加浏览器前缀（如 `-webkit-`）
- **为什么选这套方案**：
  - 避免手写大量 CSS 类名和样式规则
  - 所有样式内联在模板中，修改时无需在文件间跳转
  - 生产构建时自动清除未使用的样式（PurgeCSS），最终 CSS 体积小
- **实践技巧**：
  - 使用 `text-6xl`、`rounded-[2rem]` 等超大尺寸类匹配导出图场景
  - 通过 `group/card` 和 `group-hover/card:opacity-100` 实现父子联动效果
  - 自定义颜色透明度（如 `bg-orange-50/70`）营造层次感
- **学习要点**：工具类命名规则、响应式前缀、状态变体（hover/focus/active）

**html2canvas v1.4.1**
- **作用**：将 DOM 元素渲染为 Canvas 并导出图片
- **为什么选它**：需要"所见即所得"导出排班视图为高清图片，该库无需后端参与
- **实践难点与解决**：
  - **问题**：导出时若保留 CSS `transform: scale()`，图片会模糊
  - **解决**：设置 `isExporting` 状态，导出前临时移除缩放，确保以 1:1 比例渲染
  - **优化**：指定高 `scale` 参数提升导出分辨率
- **学习要点**：Canvas API、异步处理、样式状态管理

**electron-builder v26.7.0**
- **作用**：Electron 应用打包与分发工具
- **为什么选它**：支持生成安装包（NSIS）、便携版、自动更新配置等，是 Electron 生态最成熟的打包方案
- **配置文件**：`electron-builder.yml`（定义应用 ID、产物命名、图标、发布平台等）
- **学习要点**：打包目标配置、ASAR 归档、代码签名（本项目因权限问题禁用）

### 2. 工程化工具链深度解析

#### electron-vite v5.0.0
**定位**：专为 Electron 项目设计的构建工具，基于 Vite 封装

**核心能力**：
- 自动管理 Electron 的三进程（Main / Preload / Renderer）构建配置
- 开发模式下提供热重载（HMR）：修改代码后无需重启整个应用
- 生产构建时自动优化（代码分割、Tree Shaking、压缩）

**为什么不直接用 Vite**：Vite 原生只支持 Web 应用，需手动配置多入口、Node 环境等；`electron-vite` 开箱即用，降低配置成本

**开发体验**：执行 `npm run dev` 后，修改 Vue 组件立即在窗口中更新，无需刷新

#### Vite v7.2.6
**定位**：下一代前端构建工具

**核心优势**：
- **开发模式**：基于 ES Modules 的即时编译，启动速度极快（相比 Webpack 快 10-100 倍）
- **生产构建**：使用 Rollup 打包，输出高度优化的代码
- **插件生态**：通过 `@vitejs/plugin-vue` 处理 `.vue` 单文件组件

**本项目应用**：渲染进程（界面部分）通过 Vite 构建，支持 Vue 3、TypeScript、Tailwind 等

#### 类型检查体系

**vue-tsc v3.1.6**：Vue 单文件组件的 TypeScript 类型检查器  
**tsc（TypeScript Compiler）**：Node.js 代码（主进程/预加载脚本）的类型检查器

**构建流程**：
```bash
npm run build
  ↓
1. vue-tsc 检查 .vue 文件类型（编译前拦截类型错误）
2. tsc 检查 .ts 文件类型
3. electron-vite build 编译所有代码到 out/ 目录
```

**学习价值**：体验"类型安全"开发流程，理解编译期错误检查的价值

#### 代码质量工具

**ESLint v9.39.1 + eslint-plugin-vue**
- **作用**：静态代码分析工具，检查语法错误、代码风格、潜在 bug
- **配置**：`eslint.config.mjs`（使用 Flat Config 新格式）
- **实际收益**：自动发现未使用的变量、缺失的类型标注、不符合 Vue 最佳实践的写法

**Prettier v3.7.4**
- **作用**：代码格式化工具（自动统一缩进、引号、换行等）
- **配合 ESLint**：ESLint 负责代码质量，Prettier 负责代码风格
- **开发习惯**：保存文件时 VSCode 自动格式化，团队协作时无需争论格式问题

### 3. 开发流程与命令实践

#### 日常开发命令

```bash
# 启动开发服务器（带热重载）
npm run dev
  → electron-vite 同时启动三个进程的构建
  → 自动打开 Electron 窗口
  → 修改代码后实时更新界面

# 代码格式化
npm run format
  → Prettier 统一格式化所有文件

# 代码检查
npm run lint
  → ESLint 检查潜在问题

# 类型检查（生产构建前必做）
npm run typecheck
  → 先检查 Node.js 代码 (tsconfig.node.json)
  → 再检查 Vue 代码 (tsconfig.web.json)
```

#### 打包发布流程

**标准打包命令**：
```bash
npm run build:win
  → 执行 npm run build（类型检查 + 编译）
  → 调用 electron-builder 生成 Windows 安装包
```

**实际遇到的打包问题与解决方案**：

**问题现象**：Windows 环境打包时报错 `cannot create symbolic link: 客户端没有所需的特权`

**原因分析**：
- `electron-builder` 下载 `winCodeSign` 工具时尝试解压符号链接文件
- 普通用户权限下 Windows 默认禁止创建符号链接
- 该工具用于代码签名，但本项目未购买签名证书

**解决方案**（禁用签名相关功能）：
```powershell
$env:CSC_IDENTITY_AUTO_DISCOVERY='false'
npm run build
npx electron-builder --win nsis --config.win.signAndEditExecutable=false
```

**参数说明**：
- `CSC_IDENTITY_AUTO_DISCOVERY='false'`：禁用自动查找签名证书
- `--win nsis`：仅打包 Windows NSIS 安装包
- `--config.win.signAndEditExecutable=false`：跳过可执行文件签名编辑步骤

**学习要点**：理解桌面应用打包流程、代码签名概念、权限问题排查思路

---

## 三、架构设计与数据流

### 1. Electron 进程模型详解

Electron 应用采用**多进程架构**，类似 Chrome 浏览器，本项目涉及三类进程：

#### Main 进程（主进程）
**文件位置**：`src/main/index.ts`

**职责**：
- 管理应用生命周期（启动、退出、窗口创建）
- 调用 Node.js API（文件系统、系统托盘等）
- 通过 IPC（进程间通信）响应渲染进程请求

**本项目实际应用**：
- 创建主窗口并加载渲染进程页面
- 响应"保存排班数据"请求，写入本地文件
- 响应"读取排班数据"请求，返回已保存内容

#### Preload 脚本（预加载脚本）
**文件位置**：`src/preload/index.ts`

**职责**：
- 在渲染进程加载前执行
- 通过 `contextBridge` 安全地暴露 API 给网页
- 充当主进程与渲染进程的"翻译层"

**为什么需要它**：
- Electron 默认禁止渲染进程直接访问 Node.js（安全考虑）
- Preload 可以精确控制暴露哪些能力

**代码示例**：
```typescript
// preload/index.ts
import { contextBridge, ipcRenderer } from 'electron'

contextBridge.exposeInMainWorld('api', {
  saveShifts: (data) => ipcRenderer.invoke('save-shifts', data),
  getShifts: () => ipcRenderer.invoke('get-shifts')
})
```

渲染进程中可通过 `window.api.saveShifts()` 调用

#### Renderer 进程（渲染进程）
**文件位置**：`src/renderer/`（Vue 应用所在目录）

**职责**：
- 渲染用户界面（HTML/CSS/JS）
- 处理用户交互（点击、拖拽、输入）
- 调用 Preload 暴露的 API 与主进程通信

**本项目核心文件**：
- `App.vue`：主界面，包含排班表格、工具栏、导出逻辑
- `components/AddModal.vue`：新增/编辑医生信息的模态框
- `stores/scheduleStore.ts`：Pinia Store，管理排班状态
- `composables/useWheelZoom.ts`：滚轮缩放的复用逻辑

### 2. 数据流与状态管理

#### Pinia Store 设计

**核心数据结构**：
```typescript
interface Shift {
  id: string           // 唯一标识（UUID）
  day: string          // 星期（"周一" ~ "周日"）
  slot: "上午" | "下午" // 时段
  doctor: string       // 医生姓名
  title: string        // 职称（主任医师、副主任医师等）
  dept: string         // 科室
  hospital: string     // 所属医院
  timeStr: string      // 具体时间（如 "08:00-12:00"）
  room: string         // 诊室号
}
```

**状态管理方法**：
```typescript
const store = useScheduleStore()

// 新增排班
store.addShift({ id: uuid(), day: '周一', slot: '上午', ... })

// 更新排班（如修改医生姓名）
store.updateShift(shiftId, { doctor: '新姓名' })

// 删除排班
store.removeShift(shiftId)

// 批量设置（如拖拽后重新排序）
store.setShifts([...newOrderedList])
```

**持久化机制**：
- 每次状态变更自动调用 `save()` 方法
- 通过 IPC 将数据发送到主进程
- 主进程使用 `electron-store` 保存到本地 JSON 文件
- 应用重启时从本地读取并恢复状态

### 3. 用户交互流程

```
用户操作                   → 前端状态变化              → 数据持久化
─────────────────────────────────────────────────────────
设置起始日期              → store.startDate 更新     → 保存到本地
                          ↓
                    自动计算周一~周日日期
                          ↓
点击"添加医生"            → 打开 AddModal 组件
填写表单并提交            → store.addShift()        → 保存到本地
                          ↓
                    界面实时显示新卡片
                          ↓
拖拽卡片调整顺序          → vuedraggable 触发 @change
                          → store.setShifts()       → 保存到本地
                          ↓
点击"导出排班图片"        → isExporting = true（移除缩放）
                          → html2canvas 渲染 DOM
                          → 生成图片并下载
                          → isExporting = false（恢复缩放）
```

**学习要点**：理解单向数据流、组件通信方式、状态持久化策略

---

## 四、样式设计与视觉规范（重点）

本项目的样式策略是“信息密度高，但阅读层级清晰”，以便在大尺寸排班图中保持可读性。

### 1. 视觉风格定位
- 主风格：医疗场景下的“稳重 + 清晰 + 对比明确”；
- 色彩基调：以蓝灰中性色为主，上午与下午使用暖色/冷色做语义区分；
- 信息优先级：标题 > 星期 > 日期 > 医生姓名 > 辅助信息（科室/医院/时段/诊室）。

### 2. 布局与网格
- 使用大画布（宽屏）承载周排班信息，保证导出图清晰；
- 主体采用 `grid` 组织：左侧时段标识 + 7 天列布局；
- 每天分上午/下午两个容器，结构一致，降低认知成本；
- 卡片内部使用纵向分组（姓名、职称、标签、时间与诊室），阅读路径明确。

### 3. 字体与层级
- 标题与关键信息使用粗体（`font-black`）突出主视觉；
- 星期与日期采用大字号，确保在导出后仍可远距离阅读；
- 辅助文字使用较浅对比与较小字号，避免抢占主信息注意力。

### 4. 组件状态与反馈
- 卡片 hover 增强边框与阴影，提示可编辑；
- 拖拽手柄常驻，删除按钮按需显现（hover 时显示）；
- 缩放与导出过程采用状态切换（如导出态去除缩放），确保最终图像稳定。

### 5. Tailwind 使用策略与实战技巧

#### 原子化设计思想
传统 CSS 开发需要先命名类，再写样式规则；Tailwind 通过预定义的工具类直接在 HTML 中组合样式：

**传统方式**：
```css
.doctor-card {
  background: #fff;
  border-radius: 2rem;
  padding: 2rem;
  box-shadow: 0 10px 30px rgba(0,0,0,0.1);
}
```

**Tailwind 方式**：
```html
<div class="bg-white rounded-[2rem] p-8 shadow-2xl">
```

**优势**：无需起名、无需在文件间跳转、样式与结构关联紧密

#### 高阶技巧应用

**1. 自定义任意值（Arbitrary Values）**
```html
<!-- 标准尺寸不满足时，直接写数值 -->
<div class="w-[4200px] rounded-[3.5rem]">
```
用于精确控制画布宽度、超大圆角等非标准尺寸

**2. 分组修饰符（Group Modifiers）**
```html
<div class="group/card">
  <button class="opacity-0 group-hover/card:opacity-100">
    删除
  </button>
</div>
```
鼠标悬停父元素时，子元素的删除按钮才显示（避免界面杂乱）

**3. 颜色透明度控制**
```html
<div class="bg-orange-50/70">  <!-- 橙色背景 70% 透明度 -->
```
营造卡片与背景的层次感，保持视觉通透

**4. 超大字号适配导出场景**
```html
<div class="text-8xl">  <!-- 6rem / 96px -->
```
导出的 4200px 宽画布需要大字号才能保证打印清晰度

**5. 特殊 CSS 属性**
```html
<span class="[writing-mode:vertical-lr]">
  上午
</span>
```
通过方括号语法直接使用 CSS 属性（垂直排版）

**学习要点**：理解工具类命名规则、响应式前缀（sm/md/lg）、状态变体（hover/focus/disabled）

---

## 五、核心功能实现细节

### 1. 图片导出技术方案

#### html2canvas 工作原理
该库通过以下步骤将 DOM 转为图片：
1. 遍历目标 DOM 树，读取所有元素的计算样式
2. 在内存中创建 Canvas，按样式重新绘制每个元素
3. 将 Canvas 转为 Base64 图片数据
4. 触发浏览器下载

#### 实现代码片段
```typescript
const exportImage = async () => {
  isExporting.value = true  // 切换到导出态
  await nextTick()          // 等待 DOM 更新完成
  
  const element = document.getElementById('capture-area')
  const canvas = await html2canvas(element, {
    scale: 2,               // 放大 2 倍提升清晰度
    useCORS: true,          // 允许跨域图片
    backgroundColor: '#fff' // 强制白色背景
  })
  
  const link = document.createElement('a')
  link.download = `排班表_${store.startDate}.png`
  link.href = canvas.toDataURL('image/png')
  link.click()
  
  isExporting.value = false // 恢复编辑态
}
```

#### 关键技术点

**问题 1：缩放状态影响导出质量**
- **现象**：用户可能将视图缩小到 50% 浏览，此时导出会得到模糊的图片
- **原因**：`transform: scale(0.5)` 会让 html2canvas 按缩放后的尺寸渲染
- **解决**：
  ```vue
  <div :style="isExporting ? { transform: 'none' } : { transform: `scale(${zoomLevel})` }">
  ```
  导出时临时移除缩放，确保 1:1 比例渲染

**问题 2：导出图片分辨率不足**
- **解决**：设置 `scale: 2` 参数，Canvas 以 2 倍分辨率绘制（类似 Retina 屏）

### 2. 滚轮缩放功能（自定义 Composable）

#### 需求背景
排班表宽度 4200px，远超屏幕宽度，需要支持缩放以全局预览或聚焦编辑

#### 技术实现
封装为 `useWheelZoom` 复用逻辑：

```typescript
export function useWheelZoom(options: {
  targetElement: Ref<HTMLElement | null>
  zoomLevel: Ref<number>
  minZoom: number
  maxZoom: number
  sensitivity: number
}) {
  const handleWheel = (e: WheelEvent) => {
    if (!e.ctrlKey) return  // 仅 Ctrl + 滚轮触发
    e.preventDefault()
    
    const delta = -e.deltaY * options.sensitivity
    options.zoomLevel.value = Math.max(
      options.minZoom,
      Math.min(options.maxZoom, options.zoomLevel.value + delta)
    )
  }
  
  onMounted(() => {
    options.targetElement.value?.addEventListener('wheel', handleWheel)
  })
  
  onUnmounted(() => {
    options.targetElement.value?.removeEventListener('wheel', handleWheel)
  })
}
```

**学习要点**：
- Composition API 的逻辑复用模式
- 事件监听的生命周期管理（防止内存泄漏）
- 数值范围限制（clamp）

### 3. 键盘导航优化

支持方向键平移滚动，提升大画布浏览体验：

```typescript
const handleArrowScroll = (event: KeyboardEvent) => {
  if (isEditableTarget(event.target)) return  // 输入框中不拦截
  if (event.altKey || event.ctrlKey) return   // 避免冲突
  
  const step = event.shiftKey ? 240 : 80  // Shift 加速
  switch (event.key) {
    case 'ArrowUp':
      container.scrollTop -= step
      break
    // ... 其他方向
  }
}
```

**细节处理**：
- 在输入框中时不拦截方向键（保留光标移动功能）
- Shift + 方向键实现快速平移

### 4. 拖拽排序实现

vuedraggable 的配置与优化：

```vue
<draggable
  :list="getSlotList(day.weekName, '上午')"
  handle=".drag-handle"        <!-- 仅拖拽手柄可触发 -->
  :animation="200"             <!-- 200ms 过渡动画 -->
  :force-fallback="true"       <!-- 强制使用自定义拖拽样式 -->
  ghost-class="drag-ghost"     <!-- 拖拽占位元素样式 -->
  @change="applySlotReorder"   <!-- 排序变化回调 -->
>
```

**回调处理**：
```typescript
const applySlotReorder = (day: string, slot: string, evt: any) => {
  // evt.moved 包含 { oldIndex, newIndex, element }
  // vuedraggable 已自动更新数组，直接保存即可
  const newList = getSlotList(day, slot)
  store.setShifts([...otherSlots, ...newList])
}
```

**学习要点**：理解双向绑定数组、拖拽事件处理、状态同步时机

---

## 六、打包发布全流程与踩坑记录

### 1. electron-builder 打包原理

#### 打包流程图
```
源代码（src/）
    ↓ electron-vite build（编译）
编译产物（out/）
    ↓ electron-builder（打包）
  ┌─────────────────────────┐
  │   内嵌 Electron 运行时    │
  │   + 应用代码（ASAR 归档） │
  │   + Node.js 依赖         │
  │   + 资源文件             │
  └─────────────────────────┘
    ↓
最终产物（dist/）
```

#### 产物类型详解

**1. NSIS 安装包（hospital_calender-1.0.0-setup.exe）**
- **适用场景**：分发给普通用户
- **特点**：
  - 双击即可安装到 `C:\Program Files`
  - 自动创建桌面快捷方式
  - 提供卸载程序
  - 支持自动更新（需配置更新服务器）
- **文件大小**：约 150MB（包含完整 Chromium + Node.js）

**2. 免安装目录（win-unpacked/）**
- **适用场景**：开发测试、绿色便携版
- **目录结构**：
  ```
  win-unpacked/
  ├── hospital_calender.exe  ← 主程序（仅入口）
  ├── resources/
  │   └── app.asar           ← 应用代码归档
  ├── locales/               ← Chromium 语言包
  ├── *.dll                  ← 系统依赖库
  └── ...其他运行时文件
  ```
- **分发要求**：**必须整个目录打包**（ZIP/RAR），不能只发 `.exe`

### 2. 实际踩坑与解决方案

#### 坑点 1：符号链接权限错误

**完整错误日志**：
```
⨯ cannot execute  cause=exit status 2
ERROR: Cannot create symbolic link : 客户端没有所需的特权
C:\Users\...\electron-builder\Cache\winCodeSign\...\darwin\10.12\lib\libcrypto.dylib
```

**问题分析**：
1. `electron-builder` 下载 `winCodeSign` 用于 Windows 代码签名
2. 该工具包含 macOS 的符号链接文件（`.dylib`）
3. Windows 下 7-Zip 解压时需要管理员权限创建符号链接
4. 普通用户权限不足，解压失败

**根本原因**：项目未配置代码签名证书，但 `electron-builder` 默认尝试签名

**解决方案**：
```powershell
# 方案 1：禁用签名证书自动发现
$env:CSC_IDENTITY_AUTO_DISCOVERY='false'
npm run build:win

# 方案 2：在 electron-builder.yml 中全局禁用签名
win:
  signAndEditExecutable: false
  signingHashAlgorithms: []

# 方案 3：完整命令（推荐用于一次性打包）
$env:CSC_IDENTITY_AUTO_DISCOVERY='false'
npm run build
npx electron-builder --win nsis --config.win.signAndEditExecutable=false
```

**学习要点**：
- 代码签名的作用（防止 Windows SmartScreen 拦截）
- 企业发布需购买代码签名证书（年费约 $200-500）
- 个人项目可暂时禁用签名

#### 坑点 2：只发送 exe 文件导致启动失败

**现象**：
- 将 `win-unpacked/hospital_calender.exe` 单独发给同事
- 同事双击后弹出调试器窗口或直接闪退

**原因**：
- `.exe` 只是启动器，真正的代码在 `resources/app.asar` 中
- 缺少 `.dll`、`locales/` 等运行时依赖

**正确分发方式**：
```bash
# 方法 1：打包整个目录
Compress-Archive -Path win-unpacked -DestinationPath 排班系统便携版.zip

# 方法 2（推荐）：直接分发安装包
# 发送 hospital_calender-1.0.0-setup.exe
```

### 3. 优化建议：添加自定义打包脚本

在 `package.json` 中添加：
```json
"scripts": {
  "build:win:nosign": "cross-env CSC_IDENTITY_AUTO_DISCOVERY=false npm run build && electron-builder --win nsis --config.win.signAndEditExecutable=false"
}
```

后续直接运行 `npm run build:win:nosign` 即可

### 4. 打包配置文件解读（electron-builder.yml）

```yaml
appId: com.electron.app          # 应用唯一标识（用于注册表等）
productName: hospital_calender   # 显示名称

win:
  executableName: hospital_calender  # exe 文件名

nsis:  # Windows 安装包配置
  artifactName: ${name}-${version}-setup.${ext}  # 产物命名规则
  createDesktopShortcut: always                  # 始终创建桌面快捷方式
  oneClick: true                                 # 单击安装（无安装向导）

files:  # 打包包含的文件
  - '!**/.vscode/*'    # 排除 VSCode 配置
  - '!src/*'           # 排除源代码（只打包编译后的 out/）
  - '!*.md'            # 排除文档

electronDownload:
  mirror: https://npmmirror.com/mirrors/electron/  # 使用国内镜像加速下载
```

**学习要点**：理解打包配置、产物优化、分发策略

---

## 七、项目成果与价值

!(成果)[/images/calender-1.jpg]

### 1. 成果
- 完成从“数据录入 → 可视化编辑 → 图片导出 → Windows 打包”的闭环；
- 建立了可复用的 Electron + Vue 桌面项目模板与实践流程；
- 在真实需求的驱动下完成了样式迭代与交互细节打磨。

### 2. 价值
- 对业务侧：显著提升排班制作与更新效率；
- 对开发侧：沉淀了跨端桌面化、导出能力、打包分发的完整经验；
- 对个人成长：在工程化、UI 设计表达、问题定位与交付方面形成了系统实践。

---

## 八、可持续优化方向（后续）
- 增加“导出模板预设”（院区版本、打印版本、移动端分享版本）；
- 提供多周视图/批量复制排班能力；
- 增加导入导出（JSON/Excel）以对接外部数据；
- 增加自动备份与版本回退；
- 在打包层补充 `build:win:nosign` 脚本，降低后续发布门槛。

---

## 九、结语
本项目已达到可交付状态，具备明确的产品价值和稳定的工程实现。整体开发过程体现了“以真实业务场景驱动技术决策”的思路：先保证流程闭环，再逐步打磨视觉与交互，最终沉淀为可持续迭代的桌面应用。