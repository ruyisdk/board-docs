---
sys: buildroot
sys_ver: v1.1.4
sys_var: v1

status: peripheral
last_update: 2026-04-06
---

# RuyiSDK 外设示例

## Pico-ePaper-2.13

本文介绍如何利用 RuyiSDK 为 Milk-V Duo S 开发板快速部署交叉编译环境，并构建 Pico-ePaper-2.13 电子纸显示屏的驱动程序。

### 1. 准备工作

#### 硬件环境

* **开发板**：Milk-V Duo S (512M, SG2000)

* **显示屏**：Pico-ePaper-2.13 (电子纸显示屏模块)

* **其他**：microSD 卡、杜邦线

#### 操作系统安装与启动验证

确保您的开发板已准备好系统。


参考文档：https://github.com/DuoQilai/riscv-board-custom-dev/blob/main/Duo_S/boot_DuoS.md

#### 登录系统

将 microSD 卡插入 Milk-V Duo S，重启。使用串口连接登录系统（默认用户名：`root`，默认密码：`milkv`）。

![串口连接](https://raw.githubusercontent.com/jason-hue/riscv-board-custom-dev/main/Duo_S/images/uart.png)

### 2. 硬件连接

**注意**：连接杜邦线时不要参考显示屏的丝印，它的标注很容易让人连接错，请参考引脚图连接。

[![Pico-ePaper1-2.13](https://raw.githubusercontent.com/jason-hue/riscv-board-custom-dev/main/Duo_S/images/Pico-ePaper1-2.13.webp)](https://raw.githubusercontent.com/jason-hue/plct/main/Pico-ePaper1-2.13.webp)

  

| 连接名称 | GND | VCC | DC | CS | RST | BUSY | CLK | DIN |
| -------- | ---- | ---------- | ----- | ----- | ----- | ----- | ----- | ----- |
| 引脚 | GND | VCC (3.3V) | PIN50 | PIN11 | PIN13 | PIN46 | PIN23 | PIN19 |

  

[![2.13英寸 LCD Pico 扩展板引脚排列介绍](https://raw.githubusercontent.com/jason-hue/plct/main/Pico-ePaper-2.13-details-inter.jpg)](https://raw.githubusercontent.com/jason-hue/plct/main/Pico-ePaper-2.13-details-inter.jpg)

  

### 3. 部署 RuyiSDK 环境

#### 部署编译环境

使用 ruyi 安装工具链及示例代码包：

```bash

ruyi update

ruyi install gnu-milkv-milkv-duo-musl-bin

ruyi install milkv-duo-examples

  

# 创建虚拟开发环境

ruyi venv milkv-duo ./venv -t gnu-milkv-milkv-duo-musl-bin

```

### 4. 编译应用与验证

#### 获取源码

```bash

# 克隆源码

git clone https://github.com/zwyzwm/Pico-ePaper-2.13.git

cd Pico-ePaper-2.13/Pico-ePaper-2.13/c

```

#### 编译构建

激活虚拟环境并配置环境变量进行编译：

```bash

# 激活虚拟环境并配置环境变量

source ../../../venv/bin/ruyi-activate

export TOOLCHAIN_PREFIX=riscv64-unknown-linux-musl-

export SYSROOT=$(pwd)/../../../venv/sysroot

  

# 使用 ruyi 软件包提供的 wiringX 库进行编译

export CFLAGS="-mcpu=c906fdv -march=rv64imafdcv0p7xthead -mcmodel=medany -mabi=lp64d -I$(pwd)/../../../include/system"

export LDFLAGS="-L$(pwd)/../../../libs/system/musl_riscv64"

  

# 编译

make clean

make

```

正常情况下，终端会看到类似如下输出：

```bash
«Ruyi venv» λ ~/tmp/Pico-ePaper-2.13/Pico-ePaper-2.13/c/ main* make clean
«Ruyi venv» λ ~/tmp/Pico-ePaper-2.13/Pico-ePaper-2.13/c/ main* source ../../../../venv/bin/ruyi-activate
export TOOLCHAIN_PREFIX=riscv64-unknown-linux-musl-
export SYSROOT=$(pwd)/../../../../venv/sysroot
«Ruyi venv» λ ~/tmp/Pico-ePaper-2.13/Pico-ePaper-2.13/c/ main* export CFLAGS="-mcpu=c906fdv -march=rv64imafdcv0p7xthead -mcmodel=medany -mabi=lp64d -I$(pwd)/../../../../include/system"
export LDFLAGS="-L$(pwd)/../../../../libs/system/musl_riscv64"
«Ruyi venv» λ ~/tmp/Pico-ePaper-2.13/Pico-ePaper-2.13/c/ main* make
riscv64-unknown-linux-musl-gcc -mcpu=c906fdv -march=rv64imafdcv0p7xthead -mcmodel=medany -mabi=lp64d -I/home/knifefire/tmp/Pico-ePaper-2.13/Pico-ePaper-2.13/c/../../../../include/system -I/home/knifefire/tmp/Pico-ePaper-2.13/Pico-ePaper-2.13/c/../../../../venv/sysroot/usr/include -o ImageData.o -c ImageData.c
riscv64-unknown-linux-musl-gcc -mcpu=c906fdv -march=rv64imafdcv0p7xthead -mcmodel=medany -mabi=lp64d -I/home/knifefire/tmp/Pico-ePaper-2.13/Pico-ePaper-2.13/c/../../../../include/system -I/home/knifefire/tmp/Pico-ePaper-2.13/Pico-ePaper-2.13/c/../../../../venv/sysroot/usr/include -o font12.o -c font12.c
riscv64-unknown-linux-musl-gcc -mcpu=c906fdv -march=rv64imafdcv0p7xthead -mcmodel=medany -mabi=lp64d -I/home/knifefire/tmp/Pico-ePaper-2.13/Pico-ePaper-2.13/c/../../../../include/system -I/home/knifefire/tmp/Pico-ePaper-2.13/Pico-ePaper-2.13/c/../../../../venv/sysroot/usr/include -o font16.o -c font16.c
riscv64-unknown-linux-musl-gcc -mcpu=c906fdv -march=rv64imafdcv0p7xthead -mcmodel=medany -mabi=lp64d -I/home/knifefire/tmp/Pico-ePaper-2.13/Pico-ePaper-2.13/c/../../../../include/system -I/home/knifefire/tmp/Pico-ePaper-2.13/Pico-ePaper-2.13/c/../../../../venv/sysroot/usr/include -o font20.o -c font20.c
riscv64-unknown-linux-musl-gcc -mcpu=c906fdv -march=rv64imafdcv0p7xthead -mcmodel=medany -mabi=lp64d -I/home/knifefire/tmp/Pico-ePaper-2.13/Pico-ePaper-2.13/c/../../../../include/system -I/home/knifefire/tmp/Pico-ePaper-2.13/Pico-ePaper-2.13/c/../../../../venv/sysroot/usr/include -o font24.o -c font24.c
riscv64-unknown-linux-musl-gcc -mcpu=c906fdv -march=rv64imafdcv0p7xthead -mcmodel=medany -mabi=lp64d -I/home/knifefire/tmp/Pico-ePaper-2.13/Pico-ePaper-2.13/c/../../../../include/system -I/home/knifefire/tmp/Pico-ePaper-2.13/Pico-ePaper-2.13/c/../../../../venv/sysroot/usr/include -o font8.o -c font8.c
riscv64-unknown-linux-musl-gcc -mcpu=c906fdv -march=rv64imafdcv0p7xthead -mcmodel=medany -mabi=lp64d -I/home/knifefire/tmp/Pico-ePaper-2.13/Pico-ePaper-2.13/c/../../../../include/system -I/home/knifefire/tmp/Pico-ePaper-2.13/Pico-ePaper-2.13/c/../../../../venv/sysroot/usr/include -o paper.o -c paper.c
riscv64-unknown-linux-musl-gcc -mcpu=c906fdv -march=rv64imafdcv0p7xthead -mcmodel=medany -mabi=lp64d -I/home/knifefire/tmp/Pico-ePaper-2.13/Pico-ePaper-2.13/c/../../../../include/system -I/home/knifefire/tmp/Pico-ePaper-2.13/Pico-ePaper-2.13/c/../../../../venv/sysroot/usr/include -o paper ImageData.o font12.o font16.o font20.o font24.o font8.o paper.o -L/home/knifefire/tmp/Pico-ePaper-2.13/Pico-ePaper-2.13/c/../../../../libs/system/musl_riscv64 -L/home/knifefire/tmp/Pico-ePaper-2.13/Pico-ePaper-2.13/c/../../../../venv/sysroot/lib -L/home/knifefire/tmp/Pico-ePaper-2.13/Pico-ePaper-2.13/c/../../../../venv/sysroot/usr/lib -lwiringx
«Ruyi venv» λ ~/tmp/Pico-ePaper-2.13/Pico-ePaper-2.13/c/ main* |
```



#### 验证结果

检查生成的二进制文件：

```bash

file paper

```

正常情况下，终端会看到类似如下输出：
```bash
«Ruyi venv» λ ~/tmp/Pico-ePaper-2.13/Pico-ePaper-2.13/c/ main* file paper
paper: ELF 64-bit LSB executable, UCB RISC-V, RVC, double-float ABI, version 1 (SYSV), dynamically linked, interpreter /lib/ld-musl-riscv64v0p7_xthead.so.1, with debug_info, not stripped
«Ruyi venv» λ ~/tmp/Pico-ePaper-2.13/Pico-ePaper-2.13/c/ main* 
```


### 5. 显示字符

> - 以字符大小为`Font16`为例:

在main函数中调用`Paint_DrawString_EN(5, 10, "HELLO", &Font16, WHITE, BLACK);` ，便可以顶格显示字符 `HELLO` 。

```bash

./paper

```


![运行验证结果](https://raw.githubusercontent.com/jason-hue/riscv-board-custom-dev/main/Duo_S/images/image-20250511160733556.png)