---
sys: buildroot
sys_ver: v1.1.4
sys_var: v1

status: peripheral
last_update: 2026-04-06
---

# RuyiSDK 外设示例

## Pico-8SEG-LED

本文介绍如何使用 RuyiSDK 在 Milk-V Duo S 开发板上快速部署编译环境，并构建 Pico-8SEG-LED 数码管模块的驱动程序。

### 1. 准备工作

#### 硬件环境

* **开发板**：Milk-V Duo S (512M, SG2000)

* **模块**：Pico-8SEG-LED 数码管模块

* **其他**：microSD 卡、USB 串口调试器、杜邦线

#### 操作系统安装与启动验证

确保您的开发板已刷入 Debian v1.6.35 系统。


参考文档：https://github.com/DuoQilai/riscv-board-custom-dev/blob/main/Duo_S/boot_DuoS.md

#### 登录系统

将 microSD 卡插入 Milk-V Duo S，重启。使用串口连接登录系统（默认用户名：`root`，默认密码：`milkv`）。

![串口连接](https://raw.githubusercontent.com/jason-hue/riscv-board-custom-dev/main/Duo_S/images/uart.png)

### 2. 硬件连接

请参考以下引脚对照表及图片将模块连接至 Duo S。

[![Pico-8SEG-LED 引脚图](https://raw.githubusercontent.com/jason-hue/riscv-board-custom-dev/main/Duo_S/images/Pico-8SEG-LED.webp)](https://raw.githubusercontent.com/jason-hue/plct/main/Pico-8SEG-LED.webp)

  

[![duos-pinout-v1.1](https://raw.githubusercontent.com/jason-hue/riscv-board-custom-dev/main/Duo_S/images/duos-pinout-v1.1.webp)](https://raw.githubusercontent.com/jason-hue/plct/main/duos-pinout-v1.1.webp)

  

| 连接名称 | VSYS | GND | RCLK | CLK | DIN |
| -------- | ---- | ---- | ----- | ----- | ----- |
| 连接引脚 | 3.3V | GND | PIN50 | PIN23 | PIN19 |

  

| Pico-8SEG | 信号 | Milk-V Duo S |
| ------------------------------- | -------- | ------------------ |
| VSYS（39脚） | 3.3V供电 | J3头部 1脚（3.3V） |
| GND（任选，比如3、8、13、18脚） | 地 | J3头部 6脚（GND） |
| GP9（12脚） | RCLK | J4头部 50脚 |
| GP10（14脚） | CLK | J3头部 23脚 |
| GP11（15脚） | DIN | J3头部 19脚 |

  

![接线图 1](https://raw.githubusercontent.com/jason-hue/riscv-board-custom-dev/main/Duo_S/images/image-20250426174905950.png)

![接线图 2](https://raw.githubusercontent.com/jason-hue/riscv-board-custom-dev/main/Duo_S/images/image-20250426174927503.png)

### 3. 部署 RuyiSDK 环境

#### 安装 ruyi 包管理器

```bash

wget https://mirror.iscas.ac.cn/ruyisdk/ruyi/tags/0.41.0/ruyi-0.41.0.riscv64

chmod +x ruyi-0.41.0.riscv64

sudo cp -v ruyi-0.41.0.riscv64 /usr/local/bin/ruyi

ruyi update

```
#### 部署编译环境

使用 ruyi 安装工具链及示例代码包：

```bash

# 安装工具链和示例包

ruyi install gnu-milkv-milkv-duo-musl-bin

ruyi install milkv-duo-examples

  

# 创建基于 Milk-V Duo 的虚拟开发环境 (venv)

ruyi venv milkv-duo ./venv -t gnu-milkv-milkv-duo-musl-bin

```

### 4. 编译应用与验证

#### 获取源码

```bash

# 克隆源码

git clone https://github.com/zwyzwm/Pico-8SEG-LED.git

cd Pico-8SEG-LED/Pico-8SEG-LED/c

```

#### 编译构建

激活虚拟环境并配置环境变量进行编译：

```bash

# 激活虚拟环境并配置环境变量

source ../../../venv/bin/ruyi-activate

export TOOLCHAIN_PREFIX=riscv64-unknown-linux-musl-

export SYSROOT=$(pwd)/../../../venv/sysroot

  

# 使用 milkv-duo-examples 提供的库 and 头文件进行编译

# 这里的路径需根据实际 ruyi 提取位置调整，本教程中直接引用提取出的目录

export CFLAGS="-mcpu=c906fdv -march=rv64imafdcv0p7xthead -mcmodel=medany -mabi=lp64d -I$(pwd)/../../../include/system"

export LDFLAGS="-L$(pwd)/../../../libs/system/musl_riscv64"

  

# 清理并编译

make clean

make

```

正常情况下，终端会看到类似如下输出：

```bash
«Ruyi venv» λ ~/tmp/Pico-8SEG-LED/Pico-8SEG-LED/c/ main* make clean
«Ruyi venv» λ ~/tmp/Pico-8SEG-LED/Pico-8SEG-LED/c/ main* make
riscv64-unknown-linux-musl-gcc -mcpu=c906fdv -march=rv64imafdcv0p7xthead -mcmodel=medany -mabi=lp64d -I/home/knifefire/tmp/Pico-8SEG-LED/Pico-8SEG-LED/c/../../../../include/system -I /home/knifefire/tmp/Pico-8SEG-LED/Pico-8SEG-LED/c/../../../../venv/sysroot/usr/include -o DEV_Config.o -c DEV_Config.c
riscv64-unknown-linux-musl-gcc -mcpu=c906fdv -march=rv64imafdcv0p7xthead -mcmodel=medany -mabi=lp64d -I/home/knifefire/tmp/Pico-8SEG-LED/Pico-8SEG-LED/c/../../../../include/system -I /home/knifefire/tmp/Pico-8SEG-LED/Pico-8SEG-LED/c/../../../../venv/sysroot/usr/include -o shu.o -c shu.c
riscv64-unknown-linux-musl-gcc -mcpu=c906fdv -march=rv64imafdcv0p7xthead -mcmodel=medany -mabi=lp64d -I/home/knifefire/tmp/Pico-8SEG-LED/Pico-8SEG-LED/c/../../../../include/system -I /home/knifefire/tmp/Pico-8SEG-LED/Pico-8SEG-LED/c/../../../../venv/sysroot/usr/include -o shu DEV_Config.o shu.o -L/home/knifefire/tmp/Pico-8SEG-LED/Pico-8SEG-LED/c/../../../../libs/system/musl_riscv64 -L/home/knifefire/tmp/Pico-8SEG-LED/Pico-8SEG-LED/c/../../../../venv/sysroot/lib -L/home/knifefire/tmp/Pico-8SEG-LED/Pico-8SEG-LED/c/../../../../venv/sysroot/usr/lib -l wiringx
«Ruyi venv» λ ~/tmp/Pico-8SEG-LED/Pico-8SEG-LED/c/ main* 
```


#### 验证结果

检查生成的二进制文件：

```bash

file shu

```

正常情况下，终端会看到类似如下输出：

```bash
«Ruyi venv» λ ~/tmp/Pico-8SEG-LED/Pico-8SEG-LED/c/ main* file shu
shu: ELF 64-bit LSB executable, UCB RISC-V, RVC, double-float ABI, version 1 (SYSV), dynamically linked, interpreter /lib/ld-musl-riscv64.so.1, with debug_info, not stripped
```

