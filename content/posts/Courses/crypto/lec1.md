---
title: "Lec1"
date: 2025-09-25T08:23:36+08:00
draft: true
---

# 现代密码学介绍<br>

## 语法<br>

### 元素 elements：

- **$ \mathcal{M} $**: message space
- **$ \mathcal{K} $**: key space
- **Gen**: key generation
- **Enc**: encrypting
- **Dec**: decryprting

### 名词 nouns：

- **eavestropping adversary**: （信息传输间）窃听的攻击者
- **encryption scheme**: 加密方案


### 功能 functionality：

1.The *key-generation* algorithm **Gen** is a probabilistic algorithm that outputs a key k chosen according to some distribution.

2.The *encryption algorithm* **Enc** takes as input a key k and a message m and outputs a ciphertext c. We denote by **$Enc_k(m)$** the encryption of the plaintext m using the key k.

3.The *decryption algorithm* **Dec** takes as input a key k and a ciphertext c and outputs a plaintext m. We denote the decryption of the ciphertext c using the key k by **$Dec_k(c)$**.

for every key k output by Gen and every message m ∈ M, it holds that:
$$
Dec_k(Enc_K(m))=m
$$
即：使用对应的解密算法对一个加密后的密文解密可以得到正确的明文
<br><br>

## Kerckhoffs’ principle

### 内容：

他提出了一些军事密码学的原则，其中一条最为重要：

*The cipher method must not be required to be secret, and it must be able to fall into the hands of the enemy without inconvenience.*

这说明加密需要在攻击者知道密文的所有细节的前提下，依然是安全的，即：

*security rely solely on secrecy of the key*

### 三个支持这一原则的论点：

- 1.相比保密复杂的算法，让人员对较短的密钥进行保密更加简单。

- 2.密钥被泄露的话，单纯替换密钥会比替换整个加密方案来的方便得多。

- 3.使用固定的算法和私人密钥可以更好地进行大规模部署。

[Auguste Kerckhoffs wiki](https://en.wikipedia.org/wiki/Auguste_Kerckhoffs)
<br><br>

## 现代密码学原则
>From art to science

### Principle 1 - Formal Ddefinitions：


#### secure encryption

- *regardless of **any** information an attacker already has, a ciphertext should leak no **additional** information about the underlying plaintext*

#### attack model(attacker's power)

1 **Ciphertext-only attack**

2 **Known-plaintext attack**

3 **Chosen-plaintext attack**

4 **Chosen-ciphertext attack**


### Principle 2 - Precise Assumptions：

1 **Validation of assummptions**：算法中用到的假设（数学问题）需要被研究和细化，这样我们才可以愈发信任它

2 **Comparision of schemes**：通过依赖假设的强弱来比较两个算法的优劣

3 **Understanding the necessary assumptions**：理解一些假设是由哪些底层模块组成的，哪些底层模块是绝对正确的，哪些是暂时无法证明的


### Principle 3 - Proofs of Security：

  以上两个原则可以帮助我们得以对一种加密方式的安全性进行严密的证明，与追求快速解决的不成熟、即兴的方案相比，经过严谨的定义、假设和验证的方案取代了传统密码学而成为现代密码学的根基，历史也证明了这种思想在安全方面的优越性。

   然而现实场景的复杂性使得密码学仍然没有脱离某种设计的艺术性，在数学证明以外，如何构建威胁模型、提出安全需求仍然是现代密码学的重点，这同样也是漏洞有可能发生，密码学仍然在进步的地方。














