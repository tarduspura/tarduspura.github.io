---
title: MPC
date: 2026-03-05
---

# 1.MPC（安全多方计算）概览

## 1.1 核心问题

- 一组互不信任的参与方 $P_1, \dots, P_n$，各自持有隐私输入 $x_i$，希望在不泄露隐私的前提下协同计算函数 $y=f(x_1, \dots, xn)$

- 理想世界(Trusted Third Party, TTP)
    - 参与方将 $x_i$发送给可信第三方 *T*
    - *T* 计算并发布y
    - 缺点在于：单点故障，不显示

- 现实世界
    - 去中心化
    - Correctness：输出的y正确
    - Privacy：除了y，不泄露任何 $x_i$ 信息


## 2 核心工具：秘密分享(Secret Sharing)

### 2.1 目标
- $P_1$ 想分享秘密 $x \in \mathcal{Z}_p$ 给 $P_1$，$P_1$，$P_1$

### 2.2 方法


## 3 例子

### 3.1 Secure Addition

![secadd](../../images/pc_1.3.1.1.jpg)


### 3.2 Secure Multiplication

![secmul](../../images/pc_1.3.2.1.jpg)

!!! abstract "Tips"
- 注意这里得到的u1，u2，u3无法继续进行安全乘法。因为每个P都只持有结果的一个分片，所以无法得到交叉项（比如u1*u2）
- 为了解决这一点需要经过参与者之间的通信（顺时针通信）

### 3.3 应用：隐私配对 


## 4 恶意模型

### 4.1 输入替换

- Input Substitution
- **无法通过协议防止**，只能通过博弈论或外部机制解决

### 4.2 违背协议

- Protocol Deviation
- **
