---
sys: baremetal
sys_ver: null
sys_var: null
category: getting-started
last_update: 2026-05-31
model: Nuclei RV-STAR
profile: Hello World

---

# RuyiSDK Getting Started Example

> Note: The Nuclei RV-STAR hardware driver depends on the official Nuclei SDK and dedicated toolchains. In this example, RuyiSDK is used only for virtual environment management, obtaining the source code, and editing; compilation and flashing still use the `make` and `openocd` commands.

This example can be compiled and run directly on the development board, making it suitable for beginners.

Install dependencies

```

sudo apt update; sudo apt install -y wget tar zstd xz-utils git build-essential

```

Install the ruyi package manager

```

wget https://mirror.iscas.ac.cn/ruyisdk/ruyi/tags/0.47.0/ruyi-0.47.0.riscv64

chmod +x ruyi-0.47.0.riscv64

sudo cp -v ruyi-0.47.0.riscv64 /usr/local/bin/ruyi

```

Create a RuyiSDK virtual environment

```

ruyi update

ruyi venv -t gnu-plct generic ./ruyi-venv

source ruyi-venv/bin/activate

```

Clone the Nuclei SDK

```

git clone https://github.com/Nuclei-Software/nuclei-sdk.git

cd nuclei-sdk

```

Download the dedicated Nuclei GCC toolchain

```

wget https://download.nucleisys.com/upload/files/toolchain/gcc/nuclei_riscv_newlibc_prebuilt_linux64_nuclei-2024.tar.bz2
tar -xjvf nuclei_riscv_newlibc_prebuilt_linux64_nuclei-2024.tar.bz2

```

Download Nuclei OpenOCD

```

wget https://download.nucleisys.com/upload/files/toolchain/openocd/nuclei-openocd-2024.02.28-linux-x64.tgz
tar -xzvf nuclei-openocd-2024.02.28-linux-x64.tgz

```

Set the environment variables

```

export PATH=~/nuclei-sdk/gcc/bin:$PATH
export PATH=~/nuclei-sdk/Nuclei/openocd/2024.02.28/bin:$PATH

```

Start OpenOCD in Terminal 1

```

sudo openocd -f ~/nuclei-sdk/SoC/gd32vf103/Board/gd32vf103v_rvstar/openocd_gd32vf103.cfg

```

## Hello World (GCC)

Compile Hello World

```
cd ~/nuclei-sdk/application/baremetal/helloworld

make SOC=gd32vf103 BOARD=gd32vf103v_rvstar TOOLCHAIN=nuclei_gnu clean
make SOC=gd32vf103 BOARD=gd32vf103v_rvstar TOOLCHAIN=nuclei_gnu all

```

Flash the board from Terminal 2

```

sudo chmod 666 /dev/ttyUSB1

riscv64-unknown-elf-gdb helloworld.elf -ex "target extended-remote localhost:3333" -ex "monitor reset halt" -ex "load" -ex "monitor resume" -ex "quit"

minicom -D /dev/ttyUSB1 -b 115200

```

Under normal circumstances, the terminal displays output similar to:

```

Nuclei SDK Build Time: May 31 2026, 17:59:30
Download Mode: FLASHXIP
CPU Frequency 108000000 Hz
Hello RISC-V from RV-STAR!
Testing GCC toolchain with Nuclei SDK.

```

## Hello World (LLVM)

Compile Hello World

```
cd ~/nuclei-sdk/application/baremetal/helloworld

make SOC=gd32vf103 BOARD=gd32vf103v_rvstar TOOLCHAIN=nuclei_llvm clean
make SOC=gd32vf103 BOARD=gd32vf103v_rvstar TOOLCHAIN=nuclei_llvm all

```

Flash the board from Terminal 2

```

sudo chmod 666 /dev/ttyUSB1

riscv64-unknown-elf-gdb helloworld.elf -ex "target extended-remote localhost:3333" -ex "monitor reset halt" -ex "load" -ex "monitor resume" -ex "quit"

minicom -D /dev/ttyUSB1 -b 115200

```

Under normal circumstances, the terminal displays output similar to:

```

Nuclei SDK Build Time: May 31 2026, 18:01:49
Download Mode: FLASHXIP
CPU Frequency 108000000 Hz
Hello RISC-V from RV-STAR!
Testing LLVM/Clang toolchain with Nuclei SDK.

```
