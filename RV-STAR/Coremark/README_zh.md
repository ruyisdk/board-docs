---
sys: baremetal
sys_ver: null
sys_var: null
status: basics
last_update: 2026-05-31
model: Nuclei RV-STAR
profile: Coremark

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

## Coremark (GCC版)

编译Coremark

```

cd nuclei-sdk/application/baremetal/benchmark/coremark

make SOC=gd32vf103 BOARD=gd32vf103v_rvstar TOOLCHAIN=nuclei_gnu clean
make SOC=gd32vf103 BOARD=gd32vf103v_rvstar TOOLCHAIN=nuclei_gnu all

```

在终端2执行烧录

```

sudo chmod 666 /dev/ttyUSB1

riscv64-unknown-elf-gdb coremark.elf -ex "target extended-remote localhost:3333" -ex "monitor reset halt" -ex "load" -ex "monitor resume" -ex "quit"

minicom -D /dev/ttyUSB1 -b 115200

```

正常情况下，终端会看到类似如下输出：

```

Nuclei SDK BNuclei SDK Build Time: May 31 2026, 17:11:34 Time: May 31 2026, 17:11:34
Download Mode: FLASHXIP
CPU Frequency 108000000 Hz
Start to run coremark for 800 iterations
2K performance run parameters for coremark.
CoreMark Size    : 666
Total ticks      : 237323748
Total time (secs): 2.197440
Iterations/Sec   : 364.059997
ERROR! Must execute for at least 10 secs for a valid result!
Iterations       : 800
Compiler version : GCC13.1.1 20230713
Compiler flags   : -Ofast -fno-code-hoisting -fno-common -finline-functions -falign-fu1
Memory location  : STACK
seedcrc          : 0xe9f5
[0]crclist       : 0xe714
[0]crcmatrix     : 0x1fd7
[0]crcstate      : 0x8e3a
[0]crcfinal      : 0xcc42
Errors detected


Print Personal Added Addtional Info to Easy Visual Analysis

     (Iterations is: 800
     (total_ticks is: 237323748
 (*) Assume the core running at 1 MHz
     So the CoreMark/MHz can be calculated by:
     (Iterations*1000000/total_ticks) = 3.370923 CoreMark/MHz


CSV, Benchmark, Iterations, Cycles, CoreMark/MHz
CSV, CoreMark, 800, 237323748, 3.370
IPC = Instret/Cycle = 187415138/237323748 = 0.789

```

## Coremark (LLVM版)

编译Coremark

```

cd ~/nuclei-sdk/application/baremetal/benchmark/coremark

make SOC=gd32vf103 BOARD=gd32vf103v_rvstar TOOLCHAIN=nuclei_llvm clean
make SOC=gd32vf103 BOARD=gd32vf103v_rvstar TOOLCHAIN=nuclei_llvm all

```

在终端2执行烧录：

```

sudo chmod 666 /dev/ttyUSB1

riscv64-unknown-elf-gdb coremark.elf -ex "target extended-remote localhost:3333" -ex "monitor reset halt" -ex "load" -ex "monitor resume" -ex "quit"

minicom -D /dev/ttyUSB1 -b 115200

```

正常情况下，终端会看到类似如下输出：

```
CSV, Benchmark, Iterations, Cycles, CoreMark/MHz
CSV, CoreMark, 800, 1366745084, 0.585
IPC = Instret/Cycle = 904435054/1366745084 = 0.661
Nuclei SDK Build Time: May 31 2026, 17:35:03
DownNuclei SDK Build Time: Nuclei SDK Build TimNuclei SDK Build Time: May 31 2026, 17:9
Download Mode: FLASHXIP
CPU Frequency 108000000 Hz
Start to run coremark for 800 iterations
2K performance run parameters for coremark.
CoreMark Size    : 666
Total ticks      : 396216119
Total time (secs): 3.668667
Iterations/Sec   : 218.062840
ERROR! Must execute for at least 10 secs for a valid result!
Iterations       : 800
Compiler version : GCCClang 17.0.2 (git@gito.corp.nucleisys.com:software/devtools/llvm)
Compiler flags   : -O3 -flto -DITERATIONS=800 -DPERFORMANCE_RUN=1
Memory location  : STACK
seedcrc          : 0xe9f5
[0]crclist       : 0xe714
[0]crcmatrix     : 0x1fd7
[0]crcstate      : 0x8e3a
[0]crcfinal      : 0xcc42
Errors detected


Print Personal Added Addtional Info to Easy Visual Analysis

     (Iterations is: 800
     (total_ticks is: 396216119
 (*) Assume the core running at 1 MHz
     So the CoreMark/MHz can be calculated by:
     (Iterations*1000000/total_ticks) = 2.019100 CoreMark/MHz


CSV, Benchmark, Iterations, Cycles, CoreMark/MHz
CSV, CoreMark, 800, 396216119, 2.019
IPC = Instret/Cycle = 307677732/396216119 = 0.776

```
