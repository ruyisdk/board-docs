---
sys: debian
sys_ver: v1.6.35
sys_var: null
provider: milkv
status: peripheral
last_update: 2026-04-17
model: Milk-V Duo S
profile: Dht22
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

## Dht22 

本文介绍如何使用 RuyiSDK 在 Milk-V Duo S 开发板上快速部署编译环境，构建 DHT22 温湿度传感器测试程序，验证传感器数据读取功能。

### 1. 准备工作

* **开发板**：Milk-V Duo S (512M, SG2000)

* **传感器**：DHT22 温湿度传感器模块

* **其他**：microSD 卡、USB Type-C 数据线、杜邦线 3 根（母对母）

#### 操作系统安装与启动验证

确保您的开发板已准备好系统。

参考文档：https://github.com/DuoQilai/riscv-board-custom-dev/blob/main/Duo_S/boot_DuoS.md

### 2. 硬件连接

请参考以下引脚对照表及图片将模块连接至 Duo S。

[![dht22 引脚图](https://raw.githubusercontent.com/ZihanCheng63/board-docs/main/Duo_S/images/dht22.png)](https://raw.githubusercontent.com/ZihanCheng63/board-docs/main/Duo_S/images/dht22.png)



[![duos-pinout-v1.1](https://raw.githubusercontent.com/ruyisdk/board-docs/main/Duo_S/images/duos-pinout-v1.1.webp)](https://raw.githubusercontent.com/ruyisdk/board-docs/main/Duo_S/images/duos-pinout-v1.1.webp)



| 连接名称 | VCC | GND | SIGNAL |
| -------- | --- | --- | ---- |
| 连接引脚 | 3.3V | GND | PIN23 |

| DHT22 | 信号 | Milk-V Duo S |
| ----- | ---- | ------------- |
| VCC | 3.3V供电 | J3头部 17脚（3.3V） |
| GND | 地 | J3头部 14脚（GND） |
| DATA | 数据引脚 | J3头部 23脚 |




![接线图 1](https://raw.githubusercontent.com/ZihanCheng63/board-docs/main/Duo_S/images/image-2026041701.png)

![接线图 2](https://raw.githubusercontent.com/ZihanCheng63/board-docs/main/Duo_S/images/image-2026041702.png)

### 3. 获取源码

#### 克隆源码

```bash

ruyi extract milkv-duo-examples

mv milkv-duo-examples-* duo-examples 

cd duo-examples

```

### 4. 编译应用与验证

#### 修改源码

```bash

cd dht22

nano dht.c

```

修改以下两处内容：

```bash

# 1. 将引脚号改为 23（对应物理引脚 B15）

static int DHTPIN = 23;

# 2. 将初始化参数改为 milkv_duos

if (wiringXSetup("milkv_duos", NULL) == -1)

```

保存并退出。

#### 创建虚拟环境

```bash

cd ~/duo-examples

ruyi venv -t toolchain/gnu-plct manual venv-gnu-plct

. ~/venv-gnu-plct/bin/ruyi-activate

```

#### 验证工具链版本

```bash

riscv64-plct-linux-gnu-gcc -v

```

#### 编译 DHT22 程序

```bash

cd dht22

riscv64-plct-linux-gnu-gcc dht.c -o dht22 \
    -I../include \
    -I../wiringX/src \
    -L../libs/system/musl_riscv64 \
    -lwiringx

```

#### 验证结果

检查生成的二进制文件：

```bash

file dht22

```

### 5.传输并运行

默认用户名：`root`，默认密码：`milkv`

```bash

# 传输到开发板

scp dht22 root@192.168.42.1:/root/

# SSH 登录开发板

ssh root@192.168.42.1

# 配置引脚功能

duo-pinmux -w B15/B15

# 运行测试

./dht22

```

运行后，终端持续输出温湿度数据：

```bash

Humidity = 51.50 % Temperature = 27.30 *C
Humidity = 51.60 % Temperature = 27.30 *C
Humidity = 51.20 % Temperature = 27.30 *C
Humidity = 51.10 % Temperature = 27.30 *C
Humidity = 51.20 % Temperature = 27.30 *C
Humidity = 51.40 % Temperature = 27.30 *C

...

```
