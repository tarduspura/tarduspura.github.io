---
title: "Agent"
date: 2026-02-12T16:56:10+08:00
draft: false
---


## Skill

### Definition

> Agent Skills are **modular capabilities** that extend Claude's functionality.Each Skill packages **instructions**, **metadata**, and **optional resources**(scripts, templates) that Claude uses **automatically** when relevant.

### Format

!(format)[/images/skill-1.jpg]

- SKILL.md为第一指引（有时候还会有一些子技能）
- 结合任务情况，判断何时需要调用代码脚本（scripts）、翻阅参考文档（ref.）、使用素材资源（assets）
- 规划 - 执行 - 观察，循环直到完成任务目标


### Value

1.自然语言编写

例子1：Anthropic的brand-guidelines skill
metadata: 什么时候用
content: 品牌颜色、字体等文本描述信息

> Skill 有两种加载模式：显式 / 隐式。前者通过 user query 直接指定调用；后者根据任务与元信息描述的相关性，LLM 自动匹配。

例子2：skill作为复杂agent，以AI-Partner Skill为例

!(partner)[/images/skill-2.jpg]

使用这样的方式，ai识别到partner功能后就会自主学习并生成向量数据库来进行基于上下文感知的个性化交流


2.突破预设限制，更加灵活

- workflow/传统程序：所有情况都能预设，但存在用户与预设交互断层的情况

- agent skill：
（1）可以接受各类用户数据（text、file、picture）
（2）可以自主转换输出格式
（3）更好弥合边缘问题

3.多skills自由联用

- agent skills本质上是挂载上下文的context工程
- 因而Skills在实际应用中非常灵活，可以在一次任务中调用多个skill达成更好的效果

e.g.:产品分析报告
1.抓取网页同类产品信息：web scraping Skill
2.体取PDF中的信息：PDF Skill
3.分析制作图表：Data Analysis Skill
4.制作品牌PPT：Brand Guidelines + PPTX Skills


### 核心机制：渐进式披露

- Skill包放在Agent文件系统而非默认全量加载到上下文 
- 解决context工程中上下文过长导致的模型能力下降问题


- 根据Context加载的优先级，Skill被划分为3中层级：
（1）Metadata(YAML): always loaded. about 100 tokens
（2）Skill.md Body(markdown): Loaded when skill triggers. less than 5k tokens
（3）Bundled files(scripts, data...): loaded as needed by agent. unlimited tokens


- 默认加载元数据在安装多个skills的同时，几乎不影响上下文性能

- 慢起来可以是prompt，快起来也可以是workflow



### 应用时机

1.需要多轮对话、解释去完成的任务

2.需要特定知识、模板、材料的任务（技术文档写作、品牌设计...）

3.需要多流程协同完成的任务













