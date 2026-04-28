---
sys: debian
sys_ver: v1.6.35
sys_var: null
provider: milkv
status: peripheral
last_update: 2026-04-05
model: Milk-V Duo S
profile: Mailbox-test
---

# RuyiSDK 外设示例

可直接在开发板上进行编译和运行的示例，适合初学者快速上手。

安装依赖包

```

sudo apt update; sudo apt install -y wget tar zstd xz-utils git build-essential

```

安装 ruyi 包管理器

```

wget https://mirror.iscas.ac.cn/ruyisdk/ruyi/tags/0.47.0/ruyi-0.47.0.riscv64

chmod +x ruyi-0.47.0.riscv64

sudo cp -v ruyi-0.47.0.riscv64 /usr/local/bin/ruyi

```

安装工具链

```

ruyi update

ruyi install gnu-plct llvm-plct

```

## Mailbox-test

本文介绍如何使用 RuyiSDK 在 Milk-V Duo S 开发板上快速部署编译环境，并构建 mailbox 双核通信程序，验证大核与小核之间的通信功能。

### 1. 硬件环境准备

* **开发板**：Milk-V Duo S (512M, SG2000)

* **其他**：microSD 卡、USB Type-C 数据线

#### 操作系统安装与启动验证

确保您的开发板已准备好系统。

参考文档：https://github.com/DuoQilai/riscv-board-custom-dev/blob/main/Duo_S/boot_DuoS.md

### 2. 获取源码

#### 克隆源码

```bash

ruyi extract milkv-duo-examples

mv milkv-duo-examples-* duo-examples 

cd duo-examples

```

### 3. 编译应用与验证

#### 创建虚拟环境

```bash

ruyi venv -t toolchain/gnu-plct manual venv-gnu-plct

. ~/venv-gnu-plct/bin/ruyi-activate

```

#### 验证工具链版本

```bash

riscv64-plct-linux-gnu-gcc -v

```

#### 编译 mailbox-test 程序

```bash

cd mailbox-test

riscv64-plct-linux-gnu-gcc mailbox_test.c -o mailbox_test

```

#### 验证结果

检查生成的二进制文件：

```bash

file mailbox_test

```

### 4.传输并运行

默认用户名：`root`，默认密码：`milkv`

```bash

# 传输到开发板

scp mailbox_test root@192.168.42.1:/root/

# SSH 登录开发板后运行

ssh root@192.168.42.1

# 运行测试

./mailbox_test

```

运行后，终端输出如下信息：

```bash

C906B: cmd.param_ptr = 0x2

C906B: cmd.param_ptr = 0x3

```

同时，板载蓝色 LED 短暂亮起后熄灭。
