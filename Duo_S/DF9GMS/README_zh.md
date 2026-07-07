---
sys: debian
sys_ver: v1.6.35
sys_var: null
provider: milkv
status: peripheral
last_update: 2026-06-26
model: Milk-V Duo S
profile: DF9GMS
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

## DF9GMS

本文介绍如何使用 RuyiSDK 在 Milk-V Duo S 开发板上快速部署编译环境，构建 DF9GMS 舵机控制测试程序，验证舵机角度控制功能。

### 1. 准备工作

* **开发板**：Milk-V Duo S (512M, SG2000)

* **传感器**：DF9GMS 微型舵机

* **其他**：microSD 卡、USB Type-C 数据线、杜邦线 3 根

#### 操作系统安装与启动验证

确保您的开发板已准备好系统。

参考文档：https://github.com/DuoQilai/riscv-board-custom-dev/blob/main/Duo_S/boot_DuoS.md

### 2. 硬件连接

请参考以下引脚对照表及图片将模块连接至 Duo S。

[![df9gms 引脚图](https://raw.githubusercontent.com/ZihanCheng63/my-repo/main/videos/df9gms.png)](https://raw.githubusercontent.com/ZihanCheng63/my-repo/main/videos/df9gms.png)

  

[![duos-pinout-v1.1](https://raw.githubusercontent.com/ruyisdk/board-docs/main/Duo_S/images/duos-pinout-v1.1.webp)](https://raw.githubusercontent.com/ruyisdk/board-docs/main/Duo_S/images/duos-pinout-v1.1.webp)



| 连接名称 | VCC | GND | SIGNAL |
| -------- | --- | --- | ---- |
| 连接引脚 | 5V | GND | PIN23 |

| DF9GMS | 信号 | Milk-V Duo S |
| ------ | ---- | ------------- |
| VCC | 5V供电 | J3头部 2脚（5V） |
| GND | 地 | J3头部 6脚（GND） |
| SIGNAL | PWM信号 | J3头部 23脚 |




![接线图 1](https://raw.githubusercontent.com/ZihanCheng63/my-repo/main/videos/image-20260602601.png)

![接线图 2](https://raw.githubusercontent.com/ZihanCheng63/my-repo/main/videos/image-20260602602.png)

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

cd df9gms

nano df9gms.c

```

修改以下内容：

```bash

# 将初始化参数改为 milkv_duos

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

#### 编译 DF9GMS 程序

```bash

cd df9gms

riscv64-plct-linux-gnu-gcc df9gms.c -o df9gms \
    -I../include \
    -I../wiringX/src \
    -L../libs/system/musl_riscv64 \
    -lwiringx

```

#### 验证结果

检查生成的二进制文件：

```bash

file df9gms

```

### 5.传输并运行

默认用户名：`root`，默认密码：`milkv`

```bash

# 传输到开发板

scp df9gms root@192.168.42.1:/root/

# SSH 登录开发板

ssh root@192.168.42.1

# 配置引脚功能

duo-pinmux -w B15/B15_PWM

# 运行测试

./df9gms

```

运行后终端持续输出脉宽值，舵机会根据脉宽变化执行顺/逆时针旋转或停止：

```bash

Duty: 10000
Duty: 20000
Duty: 30000
Duty: 40000
Duty: 50000
Duty: 60000
Duty: 70000
Duty: 80000
Duty: 90000
Duty: 100000
Duty: 110000
Duty: 120000
Duty: 130000
Duty: 140000
Duty: 150000

```
