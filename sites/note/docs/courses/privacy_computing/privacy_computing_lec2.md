---
title: 现代密码学基础
date: 2026-03-17
---

# 1.现代密码学三大原则

- 传统密码学：“艺术”与“直觉”
- 现代密码学：严谨的科学范式

## 1.1 形式化的定义(Formal Definitions)

- 安全保证
    - ~~不能恢复明文~~
    - 敌手无法从密文中获得关于明文的**任何信息**
- 威胁模型(Threat Model)
    - Ciphertext-only
    - Known-plaintext：已知部分明文密文对
    - CPA
    - CCA

### 1.1.1 基于游戏的安全性定义

- IND-CPA: indistinguishability under Chosen-Plaintext Attack
![INV-CPA](../../images/pc_2.1.1.1.jpg)
  

## 1.2 