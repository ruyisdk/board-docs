# RuyiSDK 开发板文档贡献指南

[English](./CONTRIBUTING.md) / [中文](./CONTRIBUTING_zh.md)

## 概述

本文档面向希望为 RuyiSDK 开发板文档项目贡献内容的开发者。项目采用 GitHub Pull Request 机制进行协作。

参与贡献前，您需要：
1. 拥有 [GitHub 账号](https://github.com/signup)
2. 熟悉基本的 Git 操作和 GitHub 工作流
3. 了解项目文档结构和元数据规范（见下文）

如果您不熟悉 GitHub 和 Git，建议先查看 [GitHub 快速入门指南](https://docs.github.com/zh/get-started/start-your-journey/hello-world)。

本文档包含一般性贡献信息，项目的各个部分也有更具体的说明：
- [开发板（示例 Milk-V Duo）](./Duo/README.md)：开发板说明和硬件元数据。
- [示例（Milk-V Duo/Coremark）](./Duo/Coremark/README_zh.md)：环境准备、运行命令和验证结果。
- [文档模板](./templates/)：新增开发板或示例时使用的文档结构。

项目结构分层：

```plaintext
开发板文档
 |
 |--- 开发板
    |
    |--- README.md # 开发板英文说明文档，硬件元数据包含其中
    |
    |--- README_zh.md # 开发板中文说明文档
    |
    |--- 各个示例
         |
         |--- README.md # 示例英文文档（可选）
         |
         |--- README_zh.md # 示例中文文档
         |
         |--- 图片及其他配套文件
```

## 约定

### 目录命名

- 新增板卡目录名应遵循芯片/板卡厂商的官方产品命名，并去掉空格（例如 `BPI-F3`、`Jupiter2`）。
- 新增示例目录名统一使用小写字母和连字符（例如 `hello-world`、`pedestrian-detection`）。
- 不要修改存量目录名；本约定只约束新增内容。

### 版本引用

- 安装 `ruyi` 的教程统一使用仓库集中维护的版本，以及 [RuyiSDK 版本标签镜像](https://mirror.iscas.ac.cn/ruyisdk/ruyi/tags/)中的版本路径和带版本号的二进制文件名。月度工作流会统一更新所有教程中的版本。
- 每行安装命令应能独立执行，不依赖前一行留下的 shell 状态。x86_64 主机使用 `.amd64`，RISC-V 开发板使用 `.riscv64`，并确保 `wget`、`chmod` 和 `cp` 命令中的版本号与架构后缀一致。
- 其他安装方式请链接到 [RuyiSDK 官方安装文档](https://ruyisdk.org/docs/Package-Manager/installation)。
- 仓库范围的 `ruyi` 自动升版不修改 frontmatter 中的 `last_update` 字段；该字段记录教程本身最后实际验证的日期。

### 双语文档

- 新示例必须提供中文 `README_zh.md`。
- 欢迎同时提供英文 `README.md`。
- 只有单一语言不阻塞合并。

## 行为准则

在为 RuyiSDK 做贡献时，请尊重并考虑他人。我们旨在为所有贡献者营造一个开放和友好的环境。

请您遵守[《RuyiSDK 社区行为准则》](https://ruyisdk.org/en/code_of_conduct)。

## 快速开始

### 创建 PR 流程

1. Fork 并克隆仓库到本地
2. 创建分支并更新或新增开发板、示例文档
3. 提交更改，确保提交信息清晰易懂，并包含 `Signed-off-by` 标签行（详情见下文）
    * 最好在推送之前合并 / 压缩您的提交。
4. 推送提交到您的 Fork 仓库并创建 Pull Request

> [!Note]
> 如果元数据无法解析或文档内容不符合要求，您的拉取请求可能会被要求修改。

### 开发者原创声明（DCO）

我们要求 RuyiSDK 的所有贡献都包含[开发者原创声明（DCO）](https://developercertificate.org/)。DCO 是一种轻量级方式，使贡献者可以证明他们编写或有权提交所贡献的代码。

#### 什么是 DCO？

DCO 是您通过签署（sign-off）提交的方式而作出的声明。其全文非常简短，转载如下：

```
Developer Certificate of Origin
Version 1.1

Copyright (C) 2004, 2006 The Linux Foundation and its contributors.

Everyone is permitted to copy and distribute verbatim copies of this
license document, but changing it is not allowed.


Developer's Certificate of Origin 1.1

By making a contribution to this project, I certify that:

(a) The contribution was created in whole or in part by me and I
    have the right to submit it under the open source license
    indicated in the file; or

(b) The contribution is based upon previous work that, to the best
    of my knowledge, is covered under an appropriate open source
    license and I have the right under that license to submit that
    work with modifications, whether created in whole or in part
    by me, under the same open source license (unless I am
    permitted to submit under a different license), as indicated
    in the file; or

(c) The contribution was provided directly to me by some other
    person who certified (a), (b) or (c) and I have not modified
    it.

(d) I understand and agree that this project and the contribution
    are public and that a record of the contribution (including all
    personal information I submit with it, including my sign-off) is
    maintained indefinitely and may be redistributed consistent with
    this project or the open source license(s) involved.
```

#### 如何签署提交

您需要在每个提交的说明中添加一行 `Signed-off-by`，证明您同意 DCO：

```
Signed-off-by: 您的姓名 <your.email@example.com>
```

您可以通过在提交时使用 `-s` 或 `--signoff` 参数自动添加此行：

```
git commit -s -m "您的提交说明"
```

确保签名中的姓名和电子邮件与您的 Git 配置匹配。您可以使用以下命令设置您的 Git 姓名和电子邮件：

```
git config --global user.name "您的姓名"
git config --global user.email "your.email@example.com"
```

#### CI 中的 DCO 验证

所有拉取请求（PR）都会在我们的持续集成 (CI) 流程中接受自动化 DCO 检查。此检查会验证您的拉取请求中的所有提交是否都有适当的 DCO 签名。如果任何提交缺少签名，CI 检查将失败，在解决问题之前，您的拉取请求将无法被合并。

## 数据结构规范

### 元数据定义

开发板文档的 YAML 元数据可参考 Milk-V Duo：

```yaml
# /Duo/README.md
---
product: Milk-V Duo (64M) # 产品全称
cpu: CV1800B              # 处理器型号
cpu_core: XuanTie C906     # CPU 核心架构
ram: 64MB                  # 内存和闪存信息
vendor: Milk-V             # 开发板制造商
silicon_vendor: Sophgo     # 芯片制造商
---
```

以上 6 个开发板元数据字段均为必填项，且值不得为空。

示例文档的 YAML 元数据可参考 Milk-V Duo S 的 Blink 示例：

```yaml
# /Duo_S/Blink/README_zh.md
---
sys: debian              # 系统标识
sys_ver: v1.6.35         # 系统版本
sys_var: null            # 变体标识
provider: milkv          # 镜像提供方
category: peripheral     # 示例分类
last_update: 2026-04-09  # 文档最后更新日期
model: Milk-V Duo S      # 开发板名称
profile: Blink           # 示例名称
---
```

除 `provider` 外，以上示例元数据字段均为必填项。无法确定系统版本或不存在系统变体时，
`sys_ver`、`sys_var` 仍须保留并填写 `null`。`provider` 用于标识系统镜像的提供者或维护者；
无法确定时可省略。

#### 示例分类

示例文档的 `category` 应填写以下规范值之一：

| `category` 值 | 分类 |
| --- | --- |
| `getting-started` | 入门 |
| `peripheral` | 外设控制 |
| `network` | 网络通信 |
| `system` | 系统编程 |
| `storage` | 存储 |
| `power-management` | 低功耗与电源管理 |
| `multimedia` | 多媒体应用 |
| `computer-vision` | 计算机视觉 |
| `ai` | 人工智能 |
| `security` | 安全 |
| `compression` | 数据压缩 |
| `gui` | 图形界面 |
| `benchmark` | 性能测试 |
| `application` | 综合应用 |
| `other` | 其他 |

每个示例应根据主要教学目标选择一个分类。UART、I2C、SPI 等板级接口通常归入
`peripheral`，网络协议和服务归入 `network`，系统调用、内核接口和多核协作归入
`system`。只有确实无法归类时才使用 `other`，并在拉取请求描述中简要说明原因。

如还有不清楚的部分，可以提交 Issue。

## 文档编写规范

### 开发板与示例文档

请参考以下模板：

- [开发板英文模板](./templates/[board-name]/README.md)
- [开发板中文模板](./templates/[board-name]/README_zh.md)
- [示例中文模板](./templates/[board-name]/[example-name]/README_zh.md)
- [示例英文模板（可选）](./templates/[board-name]/[example-name]/README.md)

### 国际化 (i18n)

- 开发板文档使用 README.md 编写英文版本，使用 README_zh.md 编写中文版本
- 示例文档使用 README_zh.md，英文版本 README.md 为可选内容
- 其他翻译文档使用 {FileName}_{lang}.md 格式
- 不同语言版本的元数据、命令、版本、链接和预期结果应保持一致
- 保持文档间超链接的正确性
- 使用与其他同语言文档一致的术语
