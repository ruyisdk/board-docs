---
sys: debian
sys_ver: v1.6.35
sys_var: null
provider: milkv
status: peripheral 
last_update: 2026-06-06
model: Milk-V Duo S
profile: SPI
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

## SPI

本文介绍如何使用 RuyiSDK 在 Milk-V Duo S 开发板上快速部署编译环境，并构建 SPI 回环测试程序，验证芯片内部 SPI 总线的数据发送与接收功能。

### 1. 准备工作

* **开发板**：Milk-V Duo S (512M, SG2000)

* **其他**：microSD 卡、USB Type-C 数据线、一根母对母杜邦线

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

#### 创建 SPI 回环测试程序

```bash

nano spi.c

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/ioctl.h>
#include <linux/spi/spidev.h>

#define SPI_DEVICE "/dev/spidev0.0"

int main() {
    int fd;
    unsigned char tx_data[] = {0xA5, 0x5A, 0x0F, 0xF0, 0x55, 0xAA};
    unsigned char rx_data[sizeof(tx_data)];
    int len = sizeof(tx_data);
    int ret;
    int mode = 0;
    int speed = 1000000;

    fd = open(SPI_DEVICE, O_RDWR);
    if (fd < 0) {
        perror("Failed to open SPI device");
        return -1;
    }

    ret = ioctl(fd, SPI_IOC_WR_MODE, &mode);
    if (ret < 0) {
        perror("Failed to set SPI mode");
        close(fd);
        return -1;
    }

    ret = ioctl(fd, SPI_IOC_WR_MAX_SPEED_HZ, &speed);
    if (ret < 0) {
        perror("Failed to set SPI speed");
        close(fd);
        return -1;
    }

    printf("SPI device %s opened successfully\n", SPI_DEVICE);
    printf("Mode: %d, Speed: %d Hz\n", mode, speed);

    struct spi_ioc_transfer tr = {
        .tx_buf = (unsigned long)tx_data,
        .rx_buf = (unsigned long)rx_data,
        .len = len,
        .speed_hz = speed,
        .bits_per_word = 8,
    };

    ret = ioctl(fd, SPI_IOC_MESSAGE(1), &tr);
    if (ret < 1) {
        perror("SPI transfer failed");
        close(fd);
        return -1;
    }

    printf("Sent: ");
    for (int i = 0; i < len; i++) printf("0x%02X ", tx_data[i]);
    printf("\n");

    printf("Recv: ");
    for (int i = 0; i < len; i++) printf("0x%02X ", rx_data[i]);
    printf("\n");

    if (memcmp(tx_data, rx_data, len) == 0) {
        printf("✓ Loopback test PASSED! SPI communication works.\n");
    } else {
        printf("✗ Loopback test FAILED! Check your connection.\n");
    }

    close(fd);
    return 0;
}

```

#### 编译 SPI 程序

```bash

riscv64-plct-linux-gnu-gcc spi.c -o spi

```

#### 验证结果

检查生成的二进制文件：

```bash

file spi

```

### 4.传输并运行

默认用户名：`root`，默认密码：`milkv`

```bash

# 传输到开发板

scp spi root@192.168.42.1:/root/

# SSH 登录开发板

ssh root@192.168.42.1

# 运行测试

./spi

```

运行后终端输出数据：

```bash

SPI device /dev/spidev0.0 opened successfully
Mode: 0, Speed: 1000000 Hz
Sent: 0xA5 0x5A 0x0F 0xF0 0x55 0xAA
Recv: 0xA5 0x5A 0x0F 0xF0 0x55 0xAA
✓ Loopback test PASSED! SPI communication works.

```
