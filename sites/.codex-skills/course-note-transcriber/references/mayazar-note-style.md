# Mayazar Note Style

Use this reference to make converted lecture notes feel consistent with `note/docs/courses`.

## Document Shape

Start course notes with YAML frontmatter:

```markdown
---
title: 第N课：主题
date: YYYY-MM-DD
---
```

- Titles usually use `第N课：主题` or `第N讲 主题`; English-only lecture titles are acceptable for security courses.
- After frontmatter, optionally add `!!! abstract "Summary"` for a lecture overview.
- Use `## 1.主题`, `### 1.1 子主题`, and `#### 1.1.1 更细分主题`.
- Keep numbering consecutive and tied to the logical outline rather than to PDF page numbers.

## Summary And Admonitions

Use MkDocs admonitions sparingly for meta-level notes:

```markdown
!!! abstract "Summary"
    章节介绍：
    1.核心定义
    2.关键构造
    3.安全性证明思路
```

Common labels:

- `Summary`: lecture overview or section recap.
- `Tips`: exam/task heuristics or easy-to-miss distinctions.
- `Background`: prerequisite intuition or why a definition is needed.
- `Question`: a motivating question from the lecture.
- Chinese labels such as `定量计算` are fine for focused blocks.

Indent admonition content by four spaces. Inside admonitions, use short bullets or numbered lines.

## Tone

- Write mainly in Chinese, keeping important English terms and acronyms: `动态调度(Dynamic Scheduling)`, `Common Data Bus`, `IND-CPA Security`.
- Prefer class-note language over polished textbook prose.
- Use explanatory anchors often: `核心`, `直觉`, `本质`, `问题`, `解决方法`, `例子`, `证明思路`, `优点`, `缺点`, `观察`.
- Add one or two bridging sentences when slides jump too quickly, but avoid long essay paragraphs.
- Keep a slightly informal learning-note feel when helpful: `你可能会有一个疑问：...`, `徒手做的时候...`.

## Bullets

- Use `-` bullets as the default unit of explanation.
- Leave blank lines between larger bullet groups.
- Use four spaces for nested bullets.
- Numbered processes usually appear as nested bullets like `- 1.首先...`, not as top-level ordered lists.
- A good bullet is usually one concept, one definition, or one step.

Example:

```markdown
- 基本方法：DPA 的本质是统计学攻击
    - 猜测密钥
    - 构建功耗模型，并基于假设的密钥，计算对应的中间值 $\beta$
    - 与示波器实际采集到的 *$W_i$* 进行相关性分析
```

## Terminology

- Define terms with `：`, e.g. `Cache Miss：...`.
- Preserve acronyms and formulas exactly when confident.
- Use Chinese explanation plus English term when the English term is likely to appear in exams or slides.
- Keep common computing/security words in English when that matches the notes: `cache`, `hit/miss`, `buffer`, `Issue`, `Execute`, `Write results`, `receiver`, `sender`.

## Emphasis

- Use `**bold**` for key conceptual contrasts, security properties, and final takeaways.
- Use emphasis sparingly; do not bold every noun.
- Use italics for mathematical objects or source notation when needed, such as `*G*`, `*$W_i$*`.

## Math

- Use inline MathJax with `$...$`: `$M_c$`, `$a \land b$`, `$g^{ab}$`.
- Use display math for recurrence relations or central equations:

```markdown
$$
L_i = R_{i-1}
$$
$$
R_i = L_{i-1} \oplus f(R_{i-1}, K_i)
$$
```

- Do not silently change notation. If OCR makes a symbol uncertain, mark it for review.
- Keep proof sketches concise and structured by claim, intuition, and reduction steps.

## Images And Tables

- Existing notes link images from the note file to `../../images/...`.
- Place image links near the bullet that introduces them.
- Use compact alt text: `![eg1]`, `![proof]`, `![process]`, `![cache]`.
- Use Markdown tables for compact comparisons, especially algorithm parameters or security notions.

## Preferred Section Patterns

For concept-heavy lectures:

```markdown
## 1.核心问题

### 1.1 定义

- ...

### 1.2 直觉

- ...

## 2.具体构造

### 2.1 Setup
```

For systems/architecture lectures:

```markdown
## 1.Introduction

### 1.1 背景

- ...

## 2.机制

### 2.1 基本结构

- ...

## 3.例子
```

For security/crypto lectures:

```markdown
## 1.问题定义

## 2.安全性

### 2.1 安全游戏/假设

## 3.构造

## 4.证明思路
```

## Cleanup Rules

- Correct obvious OCR noise and spacing issues.
- Keep the user's occasional bilingual style; do not over-translate all English.
- Do not retain duplicated slide headers, footers, page numbers, or bibliography clutter unless useful.
- If the PDF contains references, keep only the sources that the notes directly rely on.
- Before final output, read the note top to bottom once and check whether it can be reviewed without opening the PDF.
