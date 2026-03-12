---
title: DES & AES
date: 2026-03-05
---

## 1.DES

- Data Excryption Standard(美国数据加密标准)
- 1972年美国IBM公司研制的**对称密码体制加密算法**
- 加密方法
    1.明文按64位进行分组，密钥长64位（实际上是56位，8的倍数位是校验值，是的每个密钥都有奇数个1）
    2.分组后的明文组和密钥按位替换或交换形成密文组

    具体加密方法如下：
    ![DES](../../images/hs.1.1.jpg)

    - IP(Initial Permutation)：简单的位置重排（比如第58位换到第1位），只是为了打乱输入模式，不具有加密强度。
    - Split：$L_0$ 为左32位，$R_0$ 为右32位。
    - 16 Rounds of Feistel：
    $$
    L_i = R_{i-1}
    R_i = L_{i-1} \oplus f(R_{i-1}, K_i)
    $$
        - f(·)
            - 接收：32位R寄存器数据，48位**子密钥 K**
            - 输出：经过四个步骤输出一个32位结果
            - 步骤1：E扩展置换(Expansion P-box)：32位R寄存器扩展为48位
            - 步骤2：Key Mixing：48位数据异或48位key
            - 步骤3：S盒替换(S-box Substitution)：引入唯一的**非线性因素**
                - a.48位数据被分成每组6位的8组
                - b.对于每组，取首尾二进制数组成行号，中间四个组成的二进制数为列号
                - c.从S-box中取出对应行列号的4位数据
                - d.8个数据组成32位的输出
            - 步骤4：P盒替换(Straight P-box)：将S盒输出的32位数据进行位置重新排列，进一步扩散S盒的输出  

    - $IP^(-1)$：按照初始置换，逆向变化，得到最终的密文。

- DES的安全性来自于
    - Confusion：来自S-box的非线性混淆
    - Diffusion：通过16轮的迭代和位移，让明文的任何1位变化都能影响到密文的多个位


## 2.AES

- Advanced Encryption Standard
- **Rijndael**加密法([Vincent Rijmen](https://en.wikipedia.org/wiki/Vincent_Rijmen), [
Joan Daemen](https://en.wikipedia.org/wiki/Joan_Daemen))
- 经过五年的甄选，AES由美国国家标准与技术研究院(NIST)于2001年11月26日发布于FIPS PUB 197，并在2002年5月26日成伪有效的标准
- AES是一种分组加密法，明文的每个分组为16字节，即128位，密钥长度可以使用128、192或256位。密钥长度越长，加密的轮数越多，加密的强度越高

- 加密、解密流程
![AES_process](../../images/hs.1.2.jpg)


| AES |	密钥长度（32位比特字）|	分组长度(32位比特字) | 加密轮数
AES-128	| 4	| 4 | 10
AES-192	| 6 | 4	| 12
AES-256	| 8	| 4 | 14


