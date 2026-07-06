---
sys: ubuntu
sys_ver: 24.04
sys_var: 

status: basics
last_update: 2026-07-06

model: EBC7700
profile: Coremark
---
# RuyiSDK 基础示例

可直接在开发板上进行编译和运行的示例，适合初学者快速上手。

安装依赖包

```bash
sudo apt update
sudo apt install -y wget tar zstd xz-utils git build-essential
```

安装ruyi包管理器

```bash
wget https://mirror.iscas.ac.cn/ruyisdk/ruyi/tags/0.47.0/ruyi.riscv64

chmod +x ruyi.riscv64

sudo cp -v ruyi.riscv64 /usr/local/bin/ruyi
```

安装GCC和LLVM工具链

```bash
ruyi update

ruyi install gnu-ruyisdk llvm-ruyisdk
```

## Coremark (GCC版)

创建并激活ruyi虚拟环境（GCC）

```bash
ruyi venv -t toolchain/gnu-ruyisdk manual venv-gnu-ruyisdk
. venv-gnu-ruyisdk/bin/ruyi-activate
```

验证GCC版本

```bash
riscv64-ruyisdk-linux-gnu-gcc -v
```

编译并运行Coremark（GCC）

```bash
git clone https://github.com/eembc/coremark
cd coremark
make PORT_DIR=posix CC=riscv64-ruyisdk-linux-gnu-gcc XCFLAGS="-march=rv64gc_zba_zbb" compile

./coremark.exe
```

正常情况下，终端会看到类似如下输出：

```text
«Ruyi venv-gnu-ruyisdk» ubuntu@ubuntu:~/coremark$ ./coremark.exe
2K performance run parameters for coremark.
CoreMark Size    : 666
Total ticks      : 14865
Total time (secs): 14.865000
Iterations/Sec   : 13454.423142
Iterations       : 200000
Compiler version : GCC16.1.1 20260624
Compiler flags   : -O2 -march=rv64gc_zba_zbb  -lrt
Memory location  : Please put data memory location here
                        (e.g. code in flash, data on heap etc)
seedcrc          : 0xe9f5
[0]crclist       : 0xe714
[0]crcmatrix     : 0x1fd7
[0]crcstate      : 0x8e3a
[0]crcfinal      : 0x4983
Correct operation validated. See README.md for run and reporting rules.
CoreMark 1.0 : 13454.423142 / GCC16.1.1 20260624 -O2 -march=rv64gc_zba_zbb  -lrt / Heap
«Ruyi venv-gnu-ruyisdk» ubuntu@ubuntu:~/coremark$

```

退出ruyi GCC虚拟环境

```bash
cd ..
ruyi-deactivate
```

## Coremark (LLVM版)

创建并激活ruyi虚拟环境（LLVM）

```bash
ruyi venv -t toolchain/llvm-ruyisdk manual --sysroot-from gnu-ruyisdk venv-llvm-ruyisdk
. venv-llvm-ruyisdk/bin/ruyi-activate
```

验证LLVM版本

```bash
clang -v
```

编译并运行Coremark（LLVM）

```bash
cd coremark
make clean
make PORT_DIR=posix CC=clang XCFLAGS="-march=rv64gc_zba_zbb -O3" compile

./coremark.exe
```

正常情况下，终端会看到类似如下输出：

```text
«Ruyi venv-llvm-ruyisdk» ubuntu@ubuntu:~/coremark$ ./coremark.exe
2K performance run parameters for coremark.
CoreMark Size    : 666
Total ticks      : 12099
Total time (secs): 12.099000
Iterations/Sec   : 9091.660468
Iterations       : 110000
Compiler version : RuyiSDK Clang 22.1.8 (https://github.com/ruyisdk/llvm-project 15a6990a121f883ac215df2fc2677c5ace23ec41 RuyiSDK 20260625)
Compiler flags   : -O2 -march=rv64gc_zba_zbb -O3  -lrt
Memory location  : Please put data memory location here
                        (e.g. code in flash, data on heap etc)
seedcrc          : 0xe9f5
[0]crclist       : 0xe714
[0]crcmatrix     : 0x1fd7
[0]crcstate      : 0x8e3a
[0]crcfinal      : 0x33ff
Correct operation validated. See README.md for run and reporting rules.
CoreMark 1.0 : 9091.660468 / RuyiSDK Clang 22.1.8 (https://github.com/ruyisdk/llvm-project 15a6990a121f883ac215df2fc2677c5ace23ec41 RuyiSDK 20260625) -O2 -march=rv64gc_zba_zbb -O3  -lrt / Heap
«Ruyi venv-llvm-ruyisdk» ubuntu@ubuntu:~/coremark$

```

退出ruyi LLVM虚拟环境

```bash
cd ..
ruyi-deactivate
```
