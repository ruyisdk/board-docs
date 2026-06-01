---
sys: baremetal
sys_ver: null
sys_var: null
status: basics
last_update: 2026-05-31
model: Nuclei RV-STAR
profile: Hello World

---

# RuyiSDK 基础示例

> 说明：Nuclei RV-STAR 硬件驱动依赖 Nuclei 官方 SDK 和专用工具链。本示例中，RuyiSDK 仅用于虚拟环境管理、源码获取和编辑，编译烧录仍使用 make 和 openocd 命令。

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

创建 RuyiSDK 虚拟环境

```

ruyi update

ruyi venv -t gnu-plct generic ./ruyi-venv

source ruyi-venv/bin/activate

```

克隆 Nuclei SDK

```

git clone https://github.com/Nuclei-Software/nuclei-sdk.git

cd nuclei-sdk

```

下载 Nuclei 专用 GCC 工具链

```

wget https://download.nucleisys.com/upload/files/toolchain/gcc/nuclei_riscv_newlibc_prebuilt_linux64_nuclei-2024.tar.bz2
tar -xjvf nuclei_riscv_newlibc_prebuilt_linux64_nuclei-2024.tar.bz2

```

下载 Nuclei OpenOCD

```

wget https://download.nucleisys.com/upload/files/toolchain/openocd/nuclei-openocd-2024.02.28-linux-x64.tgz
tar -xzvf nuclei-openocd-2024.02.28-linux-x64.tgz

```

设置环境变量

```

export PATH=~/nuclei-sdk/gcc/bin:$PATH
export PATH=~/nuclei-sdk/Nuclei/openocd/2024.02.28/bin:$PATH

```

在终端1启动 OpenOCD

```

sudo openocd -f ~/nuclei-sdk/SoC/gd32vf103/Board/gd32vf103v_rvstar/openocd_gd32vf103.cfg

```

## Hello World (GCC版)

编译Hello World

```
cd ~/nuclei-sdk/application/baremetal/helloworld

make SOC=gd32vf103 BOARD=gd32vf103v_rvstar TOOLCHAIN=nuclei_gnu clean
make SOC=gd32vf103 BOARD=gd32vf103v_rvstar TOOLCHAIN=nuclei_gnu all

```

在终端2执行烧录

```

sudo chmod 666 /dev/ttyUSB1

riscv64-unknown-elf-gdb helloworld.elf -ex "target extended-remote localhost:3333" -ex "monitor reset halt" -ex "load" -ex "monitor resume" -ex "quit"

minicom -D /dev/ttyUSB1 -b 115200

```

正常情况下，终端会看到类似如下输出：

```

Nuclei SDK Build Time: May 31 2026, 17:59:30
Download Mode: FLASHXIP
CPU Frequency 108000000 Hz
Hello RISC-V from RV-STAR!
Testing GCC toolchain with Nuclei SDK.

```

## Hello World (LLVM版)

编译Hello World

```
cd ~/nuclei-sdk/application/baremetal/helloworld

make SOC=gd32vf103 BOARD=gd32vf103v_rvstar TOOLCHAIN=nuclei_llvm clean
make SOC=gd32vf103 BOARD=gd32vf103v_rvstar TOOLCHAIN=nuclei_llvm all

```

在终端2执行烧录

```

sudo chmod 666 /dev/ttyUSB1

riscv64-unknown-elf-gdb helloworld.elf -ex "target extended-remote localhost:3333" -ex "monitor reset halt" -ex "load" -ex "monitor resume" -ex "quit"

minicom -D /dev/ttyUSB1 -b 115200

```

正常情况下，终端会看到类似如下输出：

```

Nuclei SDK Build Time: May 31 2026, 18:01:49
Download Mode: FLASHXIP
CPU Frequency 108000000 Hz
Hello RISC-V from RV-STAR!
Testing LLVM/Clang toolchain with Nuclei SDK.

```
