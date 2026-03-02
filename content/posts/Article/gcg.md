---
title: "Universal and Transferable Adversarial Attacks on Aligned Language Models"
date: 2026-02-26T23:02:05+08:00
draft: false
---


这篇笔记聚焦“对齐（aligned）LLM 的通用（universal）+可迁移（transferable）对抗攻击”，以及它为什么对**“只靠对齐微调就能安全”**的直觉构成挑战。
关键词：jailbroken; adversarial suffix; affirmative prefix; GCC; Universal and Transformable

## 0. 基础信息（Paper Card）

- 标题：Universal and Transferable Adversarial Attacks on Aligned Language Models
- 作者：Andy Zou, Zifan Wang, Nicholas Carlini, Milad Nasr, J. Zico Kolter, Matt Fredrikson
- 机构：Carnegie Mellon University；Center for AI Safety；Google DeepMind；Bosch Center for AI
- 论文链接：
	- PDF：https://arxiv.org/pdf/2307.15043v2
	- HTML：https://arxiv.org/html/2307.15043v2
- 代码： https://github.com/llm-attacks/llm-attacks

**总结**：作者提出了一种对离散token进行优化的对抗后缀生成方法（Greedy Coordinate Gradient, GCG），能自动训练出**后缀式的对抗提示**，以诱导大模型输出有害字符串或选择遵循有害指令，并通过聚合训练，在多提示词和多种商用大模型上都取得了不错的泛化能力。


## 1. 背景：对齐、拒答与“对抗对齐”

对齐（RLHF / Constitutional AI 等）在常规输入下能显著降低模型输出不当内容的概率，但论文强调：

- 这更像是对“自然分布上的提示”进行约束；
- 一旦允许攻击者在输入里加入额外 token（尤其是通用 suffix），模型可能存在稳定的“绕过路径”。

这与视觉对抗样本历史很像：系统在自然输入上很强，但对刻意构造的输入脆弱。

## 2. 问题形式化：把“越狱 suffix”写成优化问题

### 2.1 语言模型概率记号

把 LLM 看作对下一个 token 的条件分布：

$$p(x_{n+1}\mid x_{1:n}),\quad x_i\in\{1,\dots,V\}$$

生成长度为 $H$ 的续写序列概率：

$$p(x_{n+1:n+H}\mid x_{1:n}) = \prod_{i=1}^{H} p(x_{n+i}\mid x_{1:n+i-1})$$

### 2.2 目标：诱导“肯定式开头”而非直接指定完整有害输出

论文一个关键工程选择是：不要求模型输出某个完整目标字符串（过强且不通用），而是让模型的回复**以一段肯定式前缀开头**（例如“Sure, here is …”并复述用户请求），从而更容易触发后续顺从。

把目标前缀 token 记为 $x_{n+1:n+H^*}^*$，攻击损失定义为目标前缀的负对数似然：

$$\mathcal{L}(x_{1:n}) = -\log p\big(x_{n+1:n+H^*}^*\mid x_{1:n}\big)$$

于是目标就转换成了最小化负对数似然（即最大化生成肯定前缀的概率）。

### 2.3 “后缀攻击”的优化变量

输入 $x_{1:n}$ 中只有一部分 token 允许被修改（后缀位置集合 $\mathcal{I}$），优化问题写成：

$$\min_{x_{\mathcal{I}}\in\{1,\dots,V\}^{|\mathcal{I}|}}\ \mathcal{L}(x_{1:n})$$

直观上：用户问题保持不变，攻击者只在末尾附加/替换一段 suffix token，使得模型“更倾向以肯定式开头”。

## 3. 方法：Greedy Coordinate Gradient（GCG）离散优化

- 难点：输入是离散 token，无法直接对 token 做连续梯度下降。

GCG 的核心思路是：

1) 把当前 token 看成 one-hot 指示向量 $e_{x_i}$；
2) 由于 one-hot 编码的特性，嵌入后的token可以看作一个关于该编码的函数，因此可以对 loss 计算关于 $e_{x_i}$ 的梯度，得到一个长度为 $V$ 的向量：

$$\nabla_{e_{x_i}}\mathcal{L}(x_{1:n})\in\mathbb{R}^{V}$$

3) 用“线性化近似”挑出**最可能降低 loss 的候选替换 token**（Top-$k$ 个负梯度最大的坐标）；
4) 在这些候选里做小规模的真实前向评估，选出最优替换。

与 AutoPrompt 的区别（论文强调“看似微小但非常关键”）：

- AutoPrompt 往往每步只选定一个坐标（一个 token 位置）去替换；
- GCG 每步对所有可改坐标都计算候选，再从全局候选中采样/评估，等价于“更强的坐标搜索”。

我自己的理解：这相当于把离散优化做成“梯度引导的候选生成 + 小批量精确搜索”的混合策略，计算瓶颈主要在前向评估次数（batch size $B$）。

## 4. 通用性：多提示（multi-prompt）+ 多模型（multi-model）联合优化

### 4.1 多提示：一个 suffix 覆盖多条行为

为了得到“通用 suffix”，论文对多个训练提示（多种不当请求）共同优化一个后缀 $p_{1:\ell}$：

$$\min_{p_{1:\ell}}\sum_{j=1}^{m_c} \mathcal{L}_j\big(x^{(j)}_{1:n_j}\ \|\ p_{1:\ell}\big)$$

其中 $\|$ 表示拼接。

实现细节上，他们会：

- 聚合多个 prompt 的梯度（并做裁剪/归一化以避免某个样本主导）；
- 采用一种“逐步加难度”的课程策略：先让 suffix 在少量 prompt 上成功，再逐步加入更多 prompt（避免一开始优化目标过难导致卡住）。

### 4.2 多模型：用开源模型训练，迁移到黑盒

为了可迁移性，作者把多个白盒开源模型的 loss/梯度一起纳入优化。

重要限制：当模型使用相同 tokenizer（同一词表）时，token-level 梯度都在 $\mathbb{R}^V$，才能直接聚合；这也解释了为什么 embedding-space 的方法在“迁移到别的 tokenizer/接口”时更麻烦。

## 5. 实验与主要结论（只摘关键结论与指标）

### 5.1 基准与指标

- 数据集：AdvBench（论文构建），包含两种设置：
	- Harmful Strings：目标是让模型输出“精确匹配”的目标字符串（更难、更强控制）。
	- Harmful Behaviors：目标是让模型对指令做“合理的尝试执行”而非拒答（更贴近红队）。
- 指标：ASR（Attack Success Rate），以及（在 string 任务中）目标字符串的交叉熵 loss。
- 对比方法：PEZ、GBDA、AutoPrompt。

### 5.2 白盒有效性（开源对齐模型上）

论文报告（v2 HTML 摘要/实验部分）：

- 在 Vicuna-7B 上，GCG 在 Harmful Strings 上达到约 88% ASR；在 Harmful Behaviors 上接近 100% ASR。
- 在 LLaMA-2-7B-Chat 上，数字更低但仍显著优于基线（例如 strings 约 57%，behaviors 约 88%）。

从优化角度看，这说明离散 token 级的“梯度引导 + 坐标贪心搜索”足以在对齐模型上找到稳定触发器。

### 5.3 迁移性（黑盒商用模型）

论文展示了把 suffix 在多提示/多模型上训练后，对商用接口存在非平凡迁移：例如对 GPT-3.5、GPT-4、PaLM-2 有一定成功率，而对 Claude-2 明显更低。

作者还观察到两点很像“经典迁移对抗样本”的现象：

- **蒸馏/同源性提升迁移**：Vicuna 与 ChatGPT 输出数据的关系可能让迁移更强。
- **过拟合降低迁移**：优化步数太多，白盒 loss 继续下降，但黑盒 ASR 反而下降（需要 early stopping）。

## 6. 我觉得最有启发的点

### 6.1 “肯定式前缀”像一个模式切换开关

对齐系统很多时候表现为“拒答模板 + 安全解释”。如果攻击目标是让模型先吐出少量肯定 token（并复述指令），模型的后续生成会更容易沿着顺从轨迹走。

从概率视角，这相当于把解锁条件压缩成“让某个短前缀的条件概率足够高”，优化难度显著下降。

### 6.2 离散优化：不需要神奇技巧，但需要把搜索做对

这篇工作很“工程真相”：很多组件并非首次提出（HotFlip / AutoPrompt / prompt tuning / universal triggers 都有前作），但**组合方式**（全坐标候选、批量评估、多提示课程、多模型聚合）让它从“偶尔成功”变成“稳定可复现”。

### 6.3 Transfer 不是玄学，更像分布与表示的重叠

论文在讨论里提到：迁移在蒸馏模型之间会更强；我会把它理解为：不同模型的“拒答/顺从边界”在表示空间里可能共享某些非鲁棒特征（non-robust features），因此同一个 suffix 能跨模型推过边界。

## 7. 防御视角：这篇论文对“安全对齐”的启示

论文并没有给出万能防御，但提供了几个清晰方向（我按工程优先级重排）：

1) **对抗训练 / 红队自动化纳入训练**：把这类 suffix 搜索当作训练内环，持续更新。
2) **检测器不是终局**：输入过滤器在视觉对抗史上反复被绕过；LLM 里也可能演变成“同时攻击检测器+模型”。
3) **评测要更贴近威胁模型**：只测自然提示的安全性会高估鲁棒性；需要“自动化可扩展攻击”的评测。

## 8. 引用（BibTeX）

```bibtex
@misc{zou2023universaltransferableadversarialattacks,
	title={Universal and Transferable Adversarial Attacks on Aligned Language Models},
	author={Andy Zou and Zifan Wang and Nicholas Carlini and Milad Nasr and J. Zico Kolter and Matt Fredrikson},
	year={2023},
	eprint={2307.15043},
	archivePrefix={arXiv},
	primaryClass={cs.CL},
	url={https://arxiv.org/abs/2307.15043}
}
```

## 9. 我下一步想补的（可选）

- 把 Algorithm 1/2 用更“可实现”的伪代码重写一遍，并标注计算复杂度（前向次数 vs 反向次数）。
- 梳理与 Wallace et al. 2019（Universal Adversarial Triggers）/ AutoPrompt 的具体差异：到底哪个改动带来主要收益。
- 结合自己跑一次最小复现实验：在本地开源 chat 模型上验证“early stopping 对迁移”的影响（只做安全任务，不生成任何有害内容）。



