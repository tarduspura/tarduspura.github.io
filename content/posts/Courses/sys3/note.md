---
title: "计算机系统3"
date: 2026-03-02T10:08:38+08:00
draft: false
---

### 1.2 Classes of Computers

- Classed by Flynn

1.SISD(Single Instruction Stream, Single Data Stream)
2.SIMD
3.MISD
4.MIMD


- 更常见的一种分类方法

1.台式电脑（个人电脑）
- 通用性
- 适合个人使用
- 使用第三方软件

2.服务器电脑
- 对个别复杂应用有更好的支持
- 或者在多用户情况下更可靠
- 更强的计算、存储或者网络能力

3.嵌入式电脑
- 最广泛、最多样
- 隐藏为系统的一部分
- 有严格的power、性能、cost限制

4.个人移动设备

5.超级计算机
- 集群


### 1.3 Performance
 
- 算法：有多少指令需要执行
 
- 语言、编译器、架构：每个operation包含的机器指令数量

- 处理期和内存系统： 指令执行的速度

- I/O system（包括OS）：I/O操作的速度

#### Mesuring Perfomace

- Response time(Elapsed time)
total latency, including all aspects

- Execution time(CPU time)

#### Definition
**define performance = $\frac{1}{execution time}$**


### 1.4 Quantitive approach

#### 1.4.1 CPU Performance

*CPU Execution Time = CPU Clock Cycles x Clock Period*

or,

*$CPU Execution Time = \frac{Clock Cycle}{Clock Rate}$*

*$Clock Rate = \frac{Clock Cycles}{CPU Time}$*

#### 1.4.2 Instruction Count and CPI

IC : 指令总数。determined by programm, ISA and compiler

CPI : Average cycles per instruction

*$CPI = \frac{Clock Cycle}{IC}$*

于是CPU Time又有以下两种表达方式：

*$CPU Time = \frac{IC * CPI}{Clock Rate}$*

*$CPU Time = IC * CPI * Clock Period$*

- 不同类型的指令具有不同的CPI，可以按如下的方式计算：
*$Clock Cycles = \sum_{i=1}^{n} (CPI_i \times Instruction Count_i)$*

CPU的性能取决于：
- 算法：影响IC，可能影响CPI
- 编程语言：影响IC，CPI
- 编译器：影响IC，CPI
- ISA：影响IC，CPI，T_C_（时钟周期）


#### 1.4.3 Mutiprocessors

2 core \approx 1.5x performance

4 core \approx 3x performance

8 core \approx 6x performance


#### 1.4.4 Amdahl's Law

- 两个关键因素：
1.有多大比例的执行时间可以被优化
2.优化之后总的执行时间有多大程度的提升

*$Improved Execution Time = \frac{Affected Execution Time}{Amount of Improvement} + Unaffected Execution Time$*

*Amdahl's Law*描述的是优化计算机的某一部分对于整体优化的影响程度，揭示的核心道理是：即便把计算机的某一个部分优化到极致，如果不解决瓶颈部件，同样无法对整体运行性能带来显著的改善。

- Fraction_enhanced_ : 可优化的部分时间占总时间的比例。小于1。

- Sppedup : 永远比1大。


- basic idea

令 $T_{old}$ 为优化前执行时间，$T_{new}$ 为优化后执行时间，
$f$ 为可优化部分占比，$S$ 为该部分的加速比，则：

$$T_{new} = T_{old}\left((1-f)+\frac{f}{S}\right)$$

$$\text{Speedup}_{overall} = \frac{T_{old}}{T_{new}} = \frac{1}{(1-f)+\frac{f}{S}}$$

$$\text{Speedup}_{overall}<\frac{1}{1-f}$$


### 1.5 Great Architecture Ideas



