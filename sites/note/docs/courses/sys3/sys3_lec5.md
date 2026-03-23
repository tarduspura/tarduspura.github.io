---
title: 第5课：内存层级结构
date: 2026-03-23
---

## 1.Introduction

### 1.1 Memory

- Register：位于CPU内部，速度最快，容量最小
- Cache：位于CPU和主存之间
- Memory：主存(RAM)，是程序运行时存放数据的地方
- Storage（外存）：硬盘、U盘等外部设备

### 1.2 存储器分类

- Mechanical memory（机械式存储）

    - Acoustic wave（声波）/torque wave（扭转波） delay line memory
        - 通过水银或金属丝中的波动循环来保存信息
    - Magnetic Drum Memory（磁鼓存储器）
        - 现代硬盘的前身。利用旋转的金属圆柱体表面的磁性来记录数据
    - Magnetic core memory（磁芯存储器）
        - 1950-1970的主流内存。利用小磁环的磁化方向来存储二进制位

- Electronic memory（电子存储）
    - 目前最主流，基于**半导体电路**
    - SRAM（静态随机存取存储器）：速度快，常用于Cache
    - DRAM（动态随机存取存储器）：密度高，成本较低，常用于内存
        - SDRAM（同步动态随机存取存储器）：时钟与CPU同步。现代内存的鼻祖
    - Flash（闪存）：断电不丢失数据。SSD、U盘
    - ROM：数据写入后通常不再更改
        - PROM（可编程）：只能编程（熔断熔丝的物理编程）一次
        - EPROM（可擦除、可编程）


### 1.3 局部性

- Temporal locality（时间局部性）
    - 一个item被访问之后，程序会倾向于在**短时间**再次访问

- Spatial locality（空间局部性）
    - 一个item被访问之后，其**地址附近**的item会更容易被访问


### 1.4 层级结构

- 根据局部性原理，为了让**处理器更高效地获取数据**，在简单的冯诺依曼架构上设计了**内存的层级结构**

![hierachy](../../images/sys3.5.1.jpg)


### 1.5 Cache

- 定义：a safe place for **hiding** or ** storing** things

- 特点
    - memory hierachy的最高层。addr一离开处理器就会进入cache
    - 使用buffering来重用常用的items

- hit/miss
    - 处理器可以/不可以在cache中找到需要的数据项

- Cache Miss：检索这个块第一个词的时间和检索这个块剩余所有词的时间
    - 取决于：
        - Latency：检索块中第一个词的时间
        - Bandwidth：检索块中所有剩余部分的时间
    
    - 产生原因：
        - Compulsory Miss（强制未命中）
            - 第一次访问一个clock的时候，因为此时程序刚开始运行，数据还没有被加载进cache，所以肯定会miss
        - Capacity Miss（容量未命中）
            - 因为cache的容量有限，为了给新数据腾出空间，cache将旧数据删除之后又需要用到旧数据，会导致miss
        - Conflict Miss（冲突未命中）
            - 程序重复引用一些不同块中的不同数据，但这些不同的数据映射到cache的同一个槽位。所以这些冲突的数据就会不断覆盖，导致miss。

- Cache局部性
    - Temporal locality: need the requested word again **soon**
        - 越经常使用的数据要越靠近处理器
    - Spatial locality: likely need other data **within the same block** soon
        - 把最近访问过的word所在的block移动到更接近处理器的位置


- 命中时间（hit time）：访问本层存储的时间，包括判断hit/miss的时间

- 失效损失（miss penalty）：将相应的块从下层存储替换到上层存储中的时间，加上该数据块返回给处理器的时间

- Block/Line Run
    - 调度的单位是包含目标数据的块或者行

![block/line](../../images/sys3.5.2.jpg)


## 2.Tech trend and Memory Hierachy

### 2.1 performance曲线

![trend1](../../images/sys3.5.3.jpg)

![trend2](../../images/sys3.5.4.jpg)


### 2.2 结构

- 结构发展

![architecture](../../images/sys3.5.5.jpg)


- Memory/Storage

![memory](../../images/sys3.5.5.jpg)


- 最经典的结构
    - Register
    - on-chip Cache
    - Second-level Cache(SRAM)
    - Main memory(DRAM)
    - Storage(Disk)

![typical_arch](../../images/sys3.5.6.jpg)













