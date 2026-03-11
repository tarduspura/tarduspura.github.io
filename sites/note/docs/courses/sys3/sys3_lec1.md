---
title: 计算机系统3
date: 2026-03-02
---

<div class="article-meta">
<span>约 1500 字</span>
<span>预计阅读 8 分钟</span>
</div>

## 1.2 Classes of Computers

### Classed by Flynn

1. SISD (Single Instruction Stream, Single Data Stream)
2. SIMD
3. MISD
4. MIMD

### 更常见的一种分类方法

1. **台式电脑（个人电脑）**
    - 通用性
    - 适合个人使用
    - 使用第三方软件

2. **服务器电脑**
    - 对个别复杂应用有更好的支持
    - 或者在多用户情况下更可靠
    - 更强的计算、存储或者网络能力

3. **嵌入式电脑**
    - 最广泛、最多样
    - 隐藏为系统的一部分
    - 有严格的 power、性能、cost 限制

4. **个人移动设备**

5. **超级计算机**
    - 集群

## 1.3 Performance

- 算法：有多少指令需要执行
- 语言、编译器、架构：每个 operation 包含的机器指令数量
- 处理期和内存系统：指令执行的速度
- I/O system（包括 OS）：I/O 操作的速度

### Measuring Performance

- **Response time (Elapsed time)**: total latency, including all aspects
- **Execution time (CPU time)**

### Definition

$$\text{Performance} = \frac{1}{\text{Execution Time}}$$

## 1.4 Quantitative Approach

### 1.4.1 CPU Performance

$$\text{CPU Execution Time} = \text{CPU Clock Cycles} \times \text{Clock Period}$$

或者：

$$\text{CPU Execution Time} = \frac{\text{Clock Cycles}}{\text{Clock Rate}}$$

$$\text{Clock Rate} = \frac{\text{Clock Cycles}}{\text{CPU Time}}$$

### 1.4.2 Instruction Count and CPI

- **IC**: 指令总数，由程序、ISA 和编译器决定
- **CPI**: Average cycles per instruction

$$\text{CPI} = \frac{\text{Clock Cycles}}{\text{IC}}$$

CPU Time 的两种表达方式：

$$\text{CPU Time} = \frac{\text{IC} \times \text{CPI}}{\text{Clock Rate}}$$

$$\text{CPU Time} = \text{IC} \times \text{CPI} \times \text{Clock Period}$$

不同类型的指令具有不同的 CPI：

$$\text{Clock Cycles} = \sum_{i=1}^{n} (\text{CPI}_i \times \text{Instruction Count}_i)$$

CPU 的性能取决于：

- 算法：影响 IC，可能影响 CPI
- 编程语言：影响 IC，CPI
- 编译器：影响 IC，CPI
- ISA：影响 IC，CPI，$T_C$（时钟周期）

### 1.4.3 Multiprocessors

- 2 core ≈ 1.5x performance
- 4 core ≈ 3x performance
- 8 core ≈ 6x performance

### 1.4.4 Amdahl's Law

两个关键因素：

1. 有多大比例的执行时间可以被优化
2. 优化之后总的执行时间有多大程度的提升

$$\text{Improved Execution Time} = \frac{\text{Affected Execution Time}}{\text{Amount of Improvement}} + \text{Unaffected Execution Time}$$

**Amdahl's Law** 描述的是优化计算机的某一部分对于整体优化的影响程度，揭示的核心道理是：即便把计算机的某一个部分优化到极致，如果不解决瓶颈部件，同样无法对整体运行性能带来显著的改善。

- $\text{Fraction}_{\text{enhanced}}$: 可优化的部分时间占总时间的比例，小于 1
- $\text{Speedup}$: 永远比 1 大

**Basic idea**

令 $T_{\text{old}}$ 为优化前执行时间，$T_{\text{new}}$ 为优化后执行时间，$f$ 为可优化部分占比，$S$ 为该部分的加速比，则：

$$T_{\text{new}} = T_{\text{old}}\left((1-f)+\frac{f}{S}\right)$$

$$\text{Speedup}_{\text{overall}}=\frac{T_{\text{old}}}{T_{\text{new}}}=\frac{1}{(1-f)+\frac{f}{S}}$$

$$\text{Speedup}_{\text{overall}}<\frac{1}{1-f}$$

## 1.5 Great Architecture Ideas

8 个重要的 architecture idea：

1. **摩尔定律**
    - 芯片上的晶体管 (transistor) 每 18-24 个月会 double
    - 当系统设计完成之后，如何设计架构会成为重要的问题

2. **抽象**
    - 较低层级的细节在高层被抽象为更简单的模型

3. **Make the common case fast**
    - 识别并加速常见情况

4. **并行**
    - 指令级并行、进程级并行...

5. **流水线**
    - break task into stages, and performed simultaneously

6. **预测**
    - 在分支预测中提前"猜"出后续指令，从而加速

7. **内存的层级结构**
    - 让访问最快、容量最小、每 bit 价格最贵的内存作为第 1 层级
    - 让访问最慢、容量最大、每 bit 价格最低的内存作为最后一个层级
    - 尽可能让内存访问可以命中最快的一级内存，让末级内存包含尽可能多的信息

8. **冗余设计 (redundancy)**
    - 增加系统的可靠性 (dependability)
    - 包括可以探测和可以纠正错误的冗余部件
    - 不同层级都有冗余设计

