---
title: RT2
date: 2026-03-15
---

- Goal: 端到端的模型能学习 1）机器人 观测——>动作 的映射  2）基于网络信息的预训练（语言信息、图像-语言信息）

- Method(VLA): 将动作表示为text tokens并像natural language tokens那样直接纳入模型的训练集

- 方法优点：1）对新物体的泛化能力 2）基本推理能力 3）结合思维链推理实现多阶段语义推理


- Cartesian end-effector commands


- Problem: Can large pretrained visionlanguage models be integrated directly into low-level robotic control to boost generalization and enable emergent semantic resoning?


### 1.VLA(Vision-Language-Action Models)

#### 1.1 Pre-Trained Vision-Language Models

- input: 一张或多张图象
- output: 自然语言

- 选择了PaLI-X和PaLM-E两个VLM来改造成VLA


#### 1.2 Robot-Action Fine-Tuning

- 目标：训练VLM使其可以输出动作


