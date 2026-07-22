---
sys: Bianbu
sys_ver: 4.0.1
sys_var: null

status: basics
last_update: 2026-07-22

model: 	Milk-V Jupiter2
profile: Coremark
---

#  RuyiSDK 基础示例
安装依赖包

```
sudo apt update; sudo apt install -y wget tar zstd xz-utils git build-essential
```

安装ruyi包管理器

```
wget https://mirror.iscas.ac.cn/ruyisdk/ruyi/tags/0.51.0/ruyi-0.51.0.riscv64

chmod +x ./ruyi-0.51.0.riscv64

sudo cp -v ./ruyi-0.51.0.riscv64 /usr/local/bin/ruyi
```

安装GCC和LLVM工具链

```
ruyi update

ruyi install gnu-ruyisdk llvm-ruyisdk
```

## Coremark (GCC版)

创建并激活ruyi虚拟环境（GCC）
```
ruyi venv -t gnu-ruyisdk manual venv-gnu-ruyisdk-jupiter2

. venv-gnu-ruyisdk-jupiter2/bin/ruyi-activate
```

验证GCC版本

```
riscv64-ruyisdk-linux-gnu-gcc -v
```

编译并运行coremark（GCC）

```
git clone https://github.com/eembc/coremark

cd coremark

make CC=riscv64-ruyisdk-linux-gnu-gcc XCFLAGS="-march=rv64imafdcv_zicbom_zicbop_zicboz_zicntr_zicond_zicsr_zifencei_zihintntl_zihintpause_zihpm_zimop_zawrs_zfa_zfh_zfhmin_zcb_zcmop_zba_zbb_zbc_zbs_zkt_zvbb_zvbc_zvfh_zvfhmin_zvkb_zvkg_zvkned_zvknha_zvknhb_zvksed_zvksh_zvkt" compile

mv coremark.exe coremark-gcc

./coremark-gcc
```


正常情况下，终端会看到类似如下输出：

```
«Ruyi venv-gnu-ruyisdk-jupiter2» jupiter2@k3:~/coremark$ ./coremark-gcc
2K performance run parameters for coremark.
CoreMark Size    : 666
Total ticks      : 13133
Total time (secs): 13.133000
Iterations/Sec   : 15228.812914
Iterations       : 200000
Compiler version : GCC16.1.1 20260624
Compiler flags   : -O2 -march=rv64imafdcv_zicbom_zicbop_zicboz_zicntr_zicond_zicsr_zifencei_zihintntl_zihintpause_zihpm_zimop_zawrs_zfa_zfh_zfhmin_zcb_zcmop_zba_zbb_zbc_zbs_zkt_zvbb_zvbc_zvfh_zvfhmin_zvkb_zvkg_zvkned_zvknha_zvknhb_zvksed_zvksh_zvkt  -lrt
Memory location  : Please put data memory location here
			(e.g. code in flash, data on heap etc)
seedcrc          : 0xe9f5
[0]crclist       : 0xe714
[0]crcmatrix     : 0x1fd7
[0]crcstate      : 0x8e3a
[0]crcfinal      : 0x4983
Correct operation validated. See README.md for run and reporting rules.
CoreMark 1.0 : 15228.812914 / GCC16.1.1 20260624 -O2 -march=rv64imafdcv_zicbom_zicbop_zicboz_zicntr_zicond_zicsr_zifencei_zihintntl_zihintpause_zihpm_zimop_zawrs_zfa_zfh_zfhmin_zcb_zcmop_zba_zbb_zbc_zbs_zkt_zvbb_zvbc_zvfh_zvfhmin_zvkb_zvkg_zvkned_zvknha_zvknhb_zvksed_zvksh_zvkt  -lrt / Heap
«Ruyi venv-gnu-ruyisdk-jupiter2» jupiter2@k3:~/coremark$
```

返回上级目录并退出ruyi GCC虚拟环境

```
cd ..; ruyi-deactivate
```

## Coremark (LLVM版)
创建并激活ruyi虚拟环境（LLVM）

```
ruyi venv -t llvm-ruyisdk manual --sysroot-from gnu-ruyisdk venv-llvm-ruyisdk-jupiter2

. venv-llvm-ruyisdk-jupiter2/bin/ruyi-activate
```
验证LLVM版本

```
clang -v
```

编译并运行 coremark（LLVM）

```
cd coremark ; make clean

make CC=clang XCFLAGS="-march=rv64imafdcv_zicbom_zicbop_zicboz_zicntr_zicond_zicsr_zifencei_zihintntl_zihintpause_zihpm_zimop_zawrs_zfa_zfh_zfhmin_zcb_zcmop_zba_zbb_zbc_zbs_zkt_zvbb_zvbc_zvfh_zvfhmin_zvkb_zvkg_zvkned_zvknha_zvknhb_zvksed_zvksh_zvkt" compile

mv coremark.exe coremark-llvm

./coremark-llvm

```


正常情况下，终端会看到类似如下输出：

```
«Ruyi venv-llvm-ruyisdk-jupiter2» jupiter2@k3:~/coremark$ ./coremark-llvm
2K performance run parameters for coremark.
CoreMark Size    : 666
Total ticks      : 11554
Total time (secs): 11.554000
Iterations/Sec   : 9520.512377
Iterations       : 110000
Compiler version : RuyiSDK Clang 22.1.8 (https://github.com/ruyisdk/llvm-project 15a6990a121f883ac215df2fc2677c5ace23ec41 RuyiSDK 20260625)
Compiler flags   : -O2 -march=rv64imafdcv_zicbom_zicbop_zicboz_zicntr_zicond_zicsr_zifencei_zihintntl_zihintpause_zihpm_zimop_zawrs_zfa_zfh_zfhmin_zcb_zcmop_zba_zbb_zbc_zbs_zkt_zvbb_zvbc_zvfh_zvfhmin_zvkb_zvkg_zvkned_zvknha_zvknhb_zvksed_zvksh_zvkt  -lrt
Memory location  : Please put data memory location here
			(e.g. code in flash, data on heap etc)
seedcrc          : 0xe9f5
[0]crclist       : 0xe714
[0]crcmatrix     : 0x1fd7
[0]crcstate      : 0x8e3a
[0]crcfinal      : 0x33ff
Correct operation validated. See README.md for run and reporting rules.
CoreMark 1.0 : 9520.512377 / RuyiSDK Clang 22.1.8 (https://github.com/ruyisdk/llvm-project 15a6990a121f883ac215df2fc2677c5ace23ec41 RuyiSDK 20260625) -O2 -march=rv64imafdcv_zicbom_zicbop_zicboz_zicntr_zicond_zicsr_zifencei_zihintntl_zihintpause_zihpm_zimop_zawrs_zfa_zfh_zfhmin_zcb_zcmop_zba_zbb_zbc_zbs_zkt_zvbb_zvbc_zvfh_zvfhmin_zvkb_zvkg_zvkned_zvknha_zvknhb_zvksed_zvksh_zvkt  -lrt / Heap
«Ruyi venv-llvm-ruyisdk-jupiter2» jupiter2@k3:~/coremark$

```
返回上级目录并退出ruyi LLVM虚拟环境

```
cd ..; ruyi-deactivate
```
