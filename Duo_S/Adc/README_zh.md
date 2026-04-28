---
sys: debian
sys_ver: v1.6.35
sys_var: null
provider: milkv
status: peripheral 
last_update: 2026-04-23
model: Milk-V Duo S
profile: ADC
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

## ADC

本文介绍如何使用 RuyiSDK 在 Milk-V Duo S 开发板上快速部署编译环境，并构建 ADC 测试程序，验证芯片内部模数转换器通道的读取功能。

### 1. 准备工作

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

#### 编译 ADC 程序

```bash

cd adc

riscv64-plct-linux-gnu-gcc adcRead.c -o adcRead

```

#### 验证结果

检查生成的二进制文件：

```bash

file adcRead

```

### 4.传输并运行

默认用户名：`root`，默认密码：`milkv`

```bash

# 传输到开发板

scp adcRead root@192.168.42.1:/root/

# SSH 登录开发板

ssh root@192.168.42.1

# 运行测试

./adcRead

```

运行后，终端持续输出数据：
#### 选择通道 4 (VDDC_RTC)：

```bash

ADC4 value is 0
ADC4 value is 0
ADC4 value is 0
...

```

#### 选择通道 5 (PWR_GPIO1)：

```bash

ADC5 value is 4095
ADC5 value is 4095
ADC5 value is 4095
...

```

#### 选择通道 6 (PWR_VBAT_V)：

```bash

ADC6 value is 3712
ADC6 value is 3688
ADC6 value is 3696
...

```
