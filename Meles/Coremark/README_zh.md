---
sys: revyos
sys_ver: "20250729"
sys_var: null

category: benchmark
last_update: 2026-04-19

model: Milk-V Meles
profile: Coremark
---
# RuyiSDK 性能测试示例

可直接在开发板上进行编译和运行的示例，适合初学者快速上手。

安装依赖包

```
sudo apt update; sudo apt install -y wget tar zstd xz-utils git build-essential
```

安装ruyi包管理器（其他安装方式见[官方安装文档](https://ruyisdk.org/docs/Package-Manager/installation)）

```bash
wget https://mirror.iscas.ac.cn/ruyisdk/ruyi/tags/0.51.0/ruyi-0.51.0.riscv64
chmod +x ./ruyi-0.51.0.riscv64
sudo cp -v ./ruyi-0.51.0.riscv64 /usr/local/bin/ruyi
```

安装GCC和LLVM工具链

```
ruyi update

ruyi install gnu-plct llvm-plct
```

## Hello World (GCC版)

创建并激活ruyi虚拟环境（GCC）

```
ruyi venv -t toolchain/gnu-plct manual venv-gnu-plct
. ~/venv-gnu-plct/bin/ruyi-activate
```

验证GCC版本

```
riscv64-plct-linux-gnu-gcc -v
```

编译并运行Coremark（GCC）

```
git clone https://github.com/eembc/coremark
cd coremark
make CC=riscv64-plct-linux-gnu-gcc XCFLAGS="-mcpu=xt-c910" compile

./coremark.exe
```

正常情况下，终端会看到类似如下输出：

```
$ make CC=riscv64-plct-linux-gnu-gcc XCFLAGS="-mcpu=xt-c910" compile

riscv64-plct-linux-gnu-gcc -O2 -Ilinux -Iposix -I. -DFLAGS_STR=\""-O2 -mcpu=xt-c910 -lrt"\" -DITERATIONS=0 -mcpu=xt-c910 core_list_join.c core_main.c core_matrix.c core_state.c core_util.c posix/core_portme.c -o ./coremark.exe -lrt

«Ruyi venv-gnu-plct» debian@revyos-meles:~/coremark$ ./coremark.exe

2K performance run parameters for coremark.
CoreMark Size    : 666
Total ticks      : 11160
Total time (secs): 11.160000
Iterations/Sec   : 9856.630824
Iterations       : 110000
Compiler version : GCC15.1.0 20250912 (experimental)
Compiler flags   : -O2 -mcpu=xt-c910 -lrt
Memory location  : Please put data memory location here
                   (e.g. code in flash, data on heap etc)
seedcrc          : 0xe9f5
[0]crclist       : 0xe714
[0]crcmatrix     : 0x1fd7
[0]crcstate      : 0x8e3a
[0]crcfinal      : 0x33ff

Correct operation validated. See README.md for run and reporting rules.
CoreMark 1.0 : 9856.630824 / GCC15.1.0 20250912 (experimental) -O2 -mcpu=xt-c910 -lrt / Heap

«Ruyi venv-gnu-plct» debian@revyos-meles:~/coremark$ 
```


退出ruyi GCC虚拟环境

```
cd ..; ruyi-deactivate
```

## Hello World (LLVM版)

创建并激活ruyi虚拟环境（LLVM）

```
ruyi venv -t toolchain/llvm-plct manual --sysroot-from gnu-plct venv-llvm-plct
. ~/venv-llvm-plct/bin/ruyi-activate
```

验证LLVM版本

```
clang -v
```

编译并运行Coremark（LLVM）

```
cd coremark; make clean; make CC=clang XCFLAGS="-march=rv64imafdc_zicntr_zicsr_zifencei_zihpm_zfh_\
xtheadba_xtheadbb_xtheadbs_xtheadcmo_\
xtheadcondmov_xtheadfmemidx_xtheadmac_xtheadmemidx_xtheadmempair_xtheadsync" compile

./coremark.exe
```

正常情况下，终端会看到类似如下输出：

```
CoreMark Size    : 666
Total ticks      : 15780
Total time (secs): 15.780000
Iterations/Sec   : 6970.849176
Iterations       : 110000
Compiler version : RuyiSDK Clang 21.1.0 (https://github.com/ruyisdk/llvm-project 3623fe661ae35c6c80ac221f14d85be76aa870f RuyiSDK 20250915)
Compiler flags   : -O2 -march=rv64imafdc_zicntr_zicsr_zifencei_zihpm_zfh_xtheadba_xtheadbb_xtheadbs_xtheadcmo_xtheadcondmov_xtheadfmemidx_xtheadmac_xtheadmemidx_xtheadmempair_xtheadsync -lrt
Memory location  : Please put data memory location here
                   (e.g. code in flash, data on heap etc)
seedcrc          : 0xe9f5
[0]crclist       : 0xe714
[0]crcmatrix     : 0x1fd7
[0]crcstate      : 0x8e3a
[0]crcfinal      : 0x33ff

Correct operation validated. See README.md for run and reporting rules.
CoreMark 1.0 : 6970.849176 / RuyiSDK Clang 21.1.0 (https://github.com/ruyisdk/llvm-project 3623fe661ae35c6c80ac221f14d85be76aa870f RuyiSDK 20250915) -O2 -march=rv64imafdc_zicntr_zicsr_zifencei_zihpm_zfh_xtheadba_xtheadbb_xtheadbs_xtheadcmo_xtheadcondmov_xtheadfmemidx_xtheadmac_xtheadmemidx_xtheadmempair_xtheadsync -lrt / Heap

«Ruyi venv-llvm-plct» debian@revyos-meles:~/coremark$
```

退出ruyi GCC虚拟环境

```
cd ..; ruyi-deactivate
```


