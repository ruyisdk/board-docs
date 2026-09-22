---
sys: fedora
sys_ver: "44"
sys_var: null

category: benchmark
last_update: 2026-09-17

model: Premier P550
profile: Coremark
---

# RuyiSDK 性能测试示例

本示例可直接在开发板上编译并运行，适合初学者快速上手。

安装依赖包

```bash
sudo dnf install -y git make wget tar zstd xz
```

安装 ruyi 包管理器（其他安装方式见[官方安装文档](https://ruyisdk.org/docs/Package-Manager/installation)）

```bash
wget https://mirror.iscas.ac.cn/ruyisdk/ruyi/tags/0.52.0/ruyi-0.52.0.riscv64
chmod +x ./ruyi-0.52.0.riscv64
sudo cp -v ./ruyi-0.52.0.riscv64 /usr/local/bin/ruyi
```

安装 GCC 和 LLVM 工具链

```bash
ruyi update

ruyi install gnu-ruyisdk llvm-ruyisdk
```

## Coremark（GCC 版）

创建并激活 ruyi 虚拟环境（GCC）

```bash
ruyi venv -t toolchain/gnu-ruyisdk manual venv-gnu-ruyisdk
. venv-gnu-ruyisdk/bin/ruyi-activate
```

验证 GCC 版本

```bash
riscv64-ruyisdk-linux-gnu-gcc -v
```

获取、编译并运行 Coremark（GCC）

```bash
git clone https://github.com/eembc/coremark
cd coremark

make PORT_DIR=posix \
CC=riscv64-ruyisdk-linux-gnu-gcc \
XCFLAGS="-march=rv64imafdch_zicsr_zifencei_zca_zcd_zba_zbb -O2" \
compile
./coremark.exe
```

正常情况下，终端会看到类似如下输出：

```text
«Ruyi venv-gnu-ruyisdk» [fedora@localhost coremark]$ make PORT_DIR=posix \
CC=riscv64-ruyisdk-linux-gnu-gcc \
XCFLAGS="-march=rv64imafdch_zicsr_zifencei_zca_zcd_zba_zbb -O2" \
compile
riscv64-ruyisdk-linux-gnu-gcc -O2 -Iposix -Iposix -I. -DFLAGS_STR=\""-O2 -march=rv64imafdch_zicsr_zifencei_zca_zcd_zba_zbb -O2  -lrt"\" -DITERATIONS=0 -march=rv64imafdch_zicsr_zifencei_zca_zcd_zba_zbb -O2 core_list_join.c core_main.c core_matrix.c core_state.c core_util.c posix/core_portme.c -o ./coremark.exe -lrt
«Ruyi venv-gnu-ruyisdk» [fedora@localhost coremark]$ ./coremark.exe
2K performance run parameters for coremark.
CoreMark Size    : 666
Total ticks      : 13643
Total time (secs): 13.643000
Iterations/Sec   : 8062.742799
Iterations       : 110000
Compiler version : GCC16.1.1 20260624
Compiler flags   : -O2 -march=rv64imafdch_zicsr_zifencei_zca_zcd_zba_zbb -O2  -lrt
Memory location  : Please put data memory location here
			(e.g. code in flash, data on heap etc)
seedcrc          : 0xe9f5
[0]crclist       : 0xe714
[0]crcmatrix     : 0x1fd7
[0]crcstate      : 0x8e3a
[0]crcfinal      : 0x33ff
Correct operation validated. See README.md for run and reporting rules.
CoreMark 1.0 : 8062.742799 / GCC16.1.1 20260624 -O2 -march=rv64imafdch_zicsr_zifencei_zca_zcd_zba_zbb -O2  -lrt / Heap
«Ruyi venv-gnu-ruyisdk» [fedora@localhost coremark]$
```

返回上级目录并退出 ruyi GCC 虚拟环境

```bash
cd ..
ruyi-deactivate
```

## Coremark（LLVM 版）

创建并激活 ruyi 虚拟环境（LLVM）

```bash
ruyi venv -t llvm-ruyisdk manual --sysroot-from gnu-ruyisdk venv-llvm-ruyisdk
. venv-llvm-ruyisdk/bin/ruyi-activate
```

验证 LLVM 版本

```bash
clang -v
```

编译并运行 Coremark（LLVM）

```bash
cd coremark
make clean
make CC=clang XCFLAGS="-march=rv64imafdch_zicsr_zifencei_zca_zcd_zba_zbb" compile

./coremark.exe
```

正常情况下，终端会看到类似如下输出：

```text
«Ruyi venv-llvm-ruyisdk» [fedora@localhost coremark]$ ./coremark.exe
2K performance run parameters for coremark.
CoreMark Size    : 666
Total ticks      : 18332
Total time (secs): 18.332000
Iterations/Sec   : 6000.436395
Iterations       : 110000
Compiler version : RuyiSDK Clang 22.1.8 (https://github.com/ruyisdk/llvm-project 15a6990a121f883ac215df2fc2677c5ace23ec41 RuyiSDK 20260625)
Compiler flags   : -O2 -march=rv64imafdch_zicsr_zifencei_zca_zcd_zba_zbb  -lrt
Memory location  : Please put data memory location here
			(e.g. code in flash, data on heap etc)
seedcrc          : 0xe9f5
[0]crclist       : 0xe714
[0]crcmatrix     : 0x1fd7
[0]crcstate      : 0x8e3a
[0]crcfinal      : 0x33ff
Correct operation validated. See README.md for run and reporting rules.
CoreMark 1.0 : 6000.436395 / RuyiSDK Clang 22.1.8 (https://github.com/ruyisdk/llvm-project 15a6990a121f883ac215df2fc2677c5ace23ec41 RuyiSDK 20260625) -O2 -march=rv64imafdch_zicsr_zifencei_zca_zcd_zba_zbb  -lrt / Heap
«Ruyi venv-llvm-ruyisdk» [fedora@localhost coremark]$
```

返回上级目录并退出 ruyi LLVM 虚拟环境

```bash
cd ..
ruyi-deactivate
```
