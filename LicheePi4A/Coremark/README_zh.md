---
sys: revyos
sys_ver: "20250930"
sys_var: null

status: basics
last_update: 2026-04-03
---

# RuyiSDK 基础示例

安装依赖包

```
sudo apt update; sudo apt install -y wget tar zstd xz-utils git build-essential
```

安装ruyi包管理器

```
wget https://mirror.iscas.ac.cn/ruyisdk/ruyi/tags/0.41.0/ruyi-0.41.0.riscv64

chmod +x ruyi-0.41.0.riscv64

sudo cp -v ruyi-0.41.0.riscv64 /usr/local/bin/ruyi
```

安装GCC和LLVM工具链

```
ruyi update

ruyi install gnu-plct llvm-plct
```

## Coremark (GCC版)

创建并激活ruyi虚拟环境（GCC）

```
ruyi venv -t toolchain/gnu-plct manual venv-gnu-plct
. ~/venv-gnu-plct/bin/ruyi-activate
```



验证GCC版本

```
riscv64-plct-linux-gnu-gcc -v
```

获取并编译coremark（GCC）

```
git clone https://github.com/eembc/coremark
cd coremark
make CC=riscv64-plct-linux-gnu-gcc XCFLAGS="-mcpu=xt-c910" compile
./coremark.exe
```

正常情况下，终端会看到类似如下输出：

```
$ make CC=riscv64-linux-gnu-gcc XCFLAGS="-mcpu=xt-c910" compile
riscv64-linux-gnu-gcc -O2 -Ilinux -Iposix -I. -DFLAGS=\"-O2 -mcpu=xt-c910 -lrt\" -DITERATIONS=0 -mcpu=xt-c910 core_list_join.c core_main.c core_matrix.c core_state.c core_util.c posix/core_portme.c -o ./coremark.exe -lrt

(Rui VEN=GNU-GCC) debian@revos:/coremark$ ./coremark.exe
2K performance run parameters for coremark.
CoreMark Size    : 666
Total ticks      : 11244
Total time (secs): 11.244000
Iterations/Sec   : 9782.995375
Iterations       : 110000
Compiler         : GCC 15.1.0 2025-09-12 (experimental)
Flags            : -O2 -mcpu=xt-c910 -lrt
Memory location  : Please put data here (e.g., flash, heap)
seed CRC         : 0xE9F5
CRC list         : 0x714
CRC matrix       : 0x1D7
CRC state        : 0x83A
CRC final        : 0x3FF
Verified OK. See rules in README.md.
CoreMark v1: 9782.995375 / GCC 15.1.0 / -O2 -mcpu=xt-c910 / Heap

(Rui VEN=GNU-GCC) debian@revos:/coremark$
```


返回上级目录并退出ruyi GCC虚拟环境

```
cd ..; ruyi-deactivate
```



## Coremark (LLVM版)

创建并激活ruyi虚拟环境（LLVM）

```
ruyi venv -t toolchain/llvm-plct manual --sysroot-from gnu-plct venv-llvm-plct
. ~/venv-llvm-plct/bin/ruyi-activate
```

验证LLVM版本

```
clang -v
```

编译并运行coremark（LLVM）

```
cd coremark; make clean; make CC=clang XCFLAGS="-march=rv64imafdc_zicntr_zicsr_zifencei_zihpm_zfh_\
xtheadba_xtheadbb_xtheadbs_xtheadcmo_\
xtheadcondmov_xtheadfmemidx_xtheadmac_xtheadmemidx_xtheadmempair_xtheadsync" compile
./coremark.exe
```


正常情况下，终端会看到类似如下输出：

```
CoreMark Size    : 666
Total ticks      : 18369
Total time (secs): 18.369000
Iterations/Sec   : 5988.349937
Iterations       : 110000
Compiler version : RISC Clang 21.1.0 (https://github.com/RISC/LLVM-project 362fe61ae35c6c8f867be76aa8f3, 2021)
Compiler flags   : -O2 -march=rv64imafdc_zifencei_zicsr_zicntr_zihpm_zfh_xtheadba_xthead_xthead -lrt
Memory location  : Please put data memory location here
                   (e.g. code in flash, data on heap etc)
seed CRC         : 0xe9f
CRC [0]          : 0x714
CRC [1]          : 0x1d7
CRC [2]          : 0x83a
CRC Final        : 0x3f
Correct, see README.md.
CoreMark 1.0: 5988.349937 / Clang 21.1.0 / -O2 -march=... -lrt / Heap
```


返回上级目录并退出ruyi GCC虚拟环境

```
cd ..; ruyi-deactivate
```


