---
title: Gigabrain-0.5M*
date: 2026-04-14
---

## 0. 摘要

- **场景理解受限**、**未来预测能力较弱**
- 在网络规模的**视频语料库上预训练的**视频世界模型**展现出强大的**时空推理**和准确的**未来预测能力**
- GigaBrain-0.5M*：GigaBrain-0.5 + RAMP

## 1. 背景与核心演进
- **从 0.5 到 0.5M 的质变**: 从单纯的规模化模仿学习 (IL)，转向基于世界模型 (World Model) 的强化学习 (RL)。
- **核心痛点解决**: 传统 VLA 在长程任务 (Long-horizon) 中容易产生累计误差。0.5M 引入的 RAMP 架构，使其具备了“预见未来状态”并“评估长期价值”的能力，复杂任务成功率提升约 30%。



## 2. RAMP 架构

### 2.1 结构


> RAMP (Reinforcement leArning via world Model-conditioned Policy) 的本质，是将反应式策略 $\pi(a_t | o_t)$ 升级为以世界模型内部状态为条件的预见式策略 $\pi(a_t | o_t, \mathbf{C}_{WM})$。

### A. 条件变量的构建 (The Condition Variable)
世界模型提供的条件变量 $\mathbf{C}_{WM}$ 包含高维和低维两部分：
- **未来状态预测** $\hat{s}_{t+k}$：世界模型对未来 $k$ 步的视觉 Latent 预测（高维）。
- **价值评估** $V_t$：当前状态的预期 Return（低维标量）。
- **本体感知** $p_t$：机器人当前的关节角度与末端位姿（低维向量）。

### B. 异构特征对齐：Spatial Tiling
**问题**: 视觉 Transformer 的特征图是 $H \times W \times C$ 的高维张量，而 $V_t$ 和 $p_t$ 是低维特征，如何让视觉的每一个 Patch 都能感知到全局的价值和状态？

**数学推导**:
1. **线性投影 (Projection)**: 首先将拼接后的低维特征映射到与视觉通道数 $C$ 相同的维度：
   $$\mathbf{v}_{low} = \mathbf{W}_{proj} [V_t \oplus p_t] \in \mathbb{R}^C$$
2. **空间广播 (Broadcasting/Tiling)**: 将该向量在空间维度 $(H \times W)$ 上复制，生成辅助特征图：
   $$\mathbf{F}_{aux} = \mathbf{v}_{low} \otimes \mathbf{1}_{H \times W} \in \mathbb{R}^{H \times W \times C}$$
3. **特征融合 (Fusion)**: 直接与原始视觉特征图相加（或拼接）：
   $$\mathbf{F}_{fused} = \mathbf{F}_{visual} + \mathbf{F}_{aux}$$

!!! abstract "Tips"
    - *高维的未来预测 $\hat{s}_{t+k}$ 因为本身具备空间结构，通常直接通过 Cross-Attention 注入。*

### C. 动作轨迹生成：Flow Matching (流匹配)
**动机**: 放弃传统的 Diffusion (DDPM)，因为扩散模型通过布朗运动加噪/去噪，推理步数多且轨迹抖动。Flow Matching 学习的是最优传输的直线路径，推理速度更快而且动作丝滑。

**数学推导**:
1. **定义概率路径 (Probability Path)**: 
   设 $t \in [0, 1]$ 为积分时间。$x_0 \sim \mathcal{N}(0, I)$ 为标准高斯噪声，$x_1 \sim p_{data}$ 为真实动作轨迹数据。
   强行构造一条连接噪声和真实数据的线性插值路径：
   $$x_t = (1-t)x_0 + t x_1$$
2. **目标速度场 (Target Vector Field)**:
   对上式求时间 $t$ 的导数，得到粒子在任意时刻的理想速度：
   $$u_t(x_t) = \frac{d}{dt}x_t = x_1 - x_0$$
   *极其优雅的结论：理想的速度场是一个指向目标的恒定向量。*
3. **网络训练目标 (Loss Function)**:
   神经网络 $v_\theta$ 的任务是，在给定当前噪声状态 $x_t$、时间步 $t$ 以及世界模型条件 $\mathbf{C}_{WM}$ 的情况下，拟合这个速度场。
   损失函数为均方误差：
   $$\mathcal{L}_{FM} = \mathbb{E}_{t \sim \mathcal{U}[0,1], x_0 \sim p_0, x_1 \sim p_{data}} \left[ \| v_\theta(x_t, t, \mathbf{C}_{WM}) - (x_1 - x_0) \|_2^2 \right]$$

### D. 联合优化与一致性约束
为了防止策略网络的动作轨迹与世界模型预测的未来状态对不上，0.5M 的整体 Loss 实际上包含了思维链（CoT）和对齐惩罚：
$$\mathcal{L}_{total} = \sum w_i \cdot \text{CE}(\hat{y}_i, y_i) + \lambda \mathcal{L}_{FM} + \beta \mathcal{L}_{align}(\tau, \hat{\tau})$$

**1. 逻辑推理与思维链项：$\sum w_i \cdot \text{CE}(\hat{y}_i, y_i)$**
* **含义**：这是针对“具身思维链”(Embodied CoT) 的自回归生成损失。
* **$\text{CE}$**：交叉熵损失 (Cross-Entropy)，用于衡量模型输出的文本/离散 Token 与真实标签的差距。
* **$\hat{y}_i, y_i$**：分别代表模型预测的第 $i$ 个 Token 和真实的 Token（例如子目标描述“移向杯子”）。
* **$w_i$**：掩码权重 (Mask/Weight)。因为输出序列里既有自然语言，又有离散的动作 Token，用 $w_i$ 可以灵活控制不同部分的学习权重（例如过滤掉不需要计算 Loss 的 padding 占位符）。

**2. 连续动作生成项：$\lambda \mathcal{L}_{FM}$**
* **含义**：这是策略网络通过 Flow Matching (流匹配) 生成底层物理运动轨迹的损失。
* **$\mathcal{L}_{FM}$**：流匹配的均方误差。强制神经网络去拟合那个指向目标数据分布的最优“直线速度场” ($x_1 - x_0$)。
* **$\lambda$**：平衡超参数。控制“底层物理动作”在整体学习目标中的重要程度。

**3. 世界模型一致性约束项：$\beta \mathcal{L}_{align}(\tau, \hat{\tau})$**
* **含义**：**这是 RAMP 架构的灵魂约束**。它要求策略网络不仅要完成任务，其执行过程还必须与世界模型“脑补”的未来相吻合。
* **$\tau$**：策略网络 (Policy) 实际生成的物理轨迹。
* **$\hat{\tau}$**：世界模型 (World Model) 基于当前状态预测出的未来轨迹或特征演化。
* **$\mathcal{L}_{align}$**：对齐惩罚（通常是 MSE 等距离度量）。如果策略网络不按照预期来执行——虽然动作能得分，但轨迹导致的环境变化和世界模型预测的完全不一样，这项 Loss 就会飙升。
* **$\beta$**：控制对齐强度的超参数。
其中 $\mathcal{L}_{align}$ 强行约束策略网络输出的物理轨迹 $\tau$ 必须能通向世界模型预测的未来特征 $\hat{\tau}$。


## 3. 对比：RAMP 与 RECAP 的关系
- **RECAP 是特例**: $a_t = \pi(o_t, \text{history})$。当 RAMP 的视野长度 $k=0$ 且丢弃价值引导 $V_t$ 时，就退化成了依靠历史循环反馈的 RECAP。
- **RAMP 的优势**: RECAP 是在时间轴上向前看，用于纠错，RAMP 是向后看，更多地是预见。这种机制让模型可以在世界模型里做条件策略强化学习，摆脱了真实数据的规模瓶颈。


## 4. 安全性探讨 (NESA Lab Focus)
从上述公式可以看出，整个 $v_\theta$ 的输出极度依赖 $\mathbf{C}_{WM}$。
- **攻击平面**: 如果我们对输入的视觉图像 $o_t$ 注入极小的对抗扰动 $\delta$，目标**不是**直接破坏特征提取，而是专门针对世界模型的价值预测模块，使其输出错误的标量 $\hat{V}_t$（例如让危险动作得分极高）。
- **影响**: 因为 Spatial Tiling 的存在，这个错误的标量会被**广播放大到整个感知空间的每一个角落**（$\mathbf{F}_{aux}$）。这种全局的污染会直接导致 Flow Matching 积分出来的轨迹发生致命漂移。