---
sys: bianbu
sys_ver: 3.0.1
sys_var: Desktop
status: basics
last_update: 2026-04-20

model: Lichee Pi 3A
profile: Coremark
---

# RuyiSDK 基础示例

可直接在开发板上进行编译和运行的示例，适合初学者快速上手。

安装依赖包

```
sudo apt update; sudo apt install -y wget tar zstd xz-utils git build-essential
```

安装ruyi包管理器

```
wget https://fast-mirror.isrc.ac.cn/ruyisdk/ruyi/tags/0.47.0/ruyi.riscv64

chmod +x ruyi-0.47.0.riscv64

sudo cp -v ruyi-0.47.0.riscv64 /usr/local/bin/ruyi
```

安装GCC和LLVM工具链

```
ruyi update

ruyi install gnu-plct llvm-plct
```

## Coremark（GCC）

创建并激活 ruyi 虚拟环境（GCC）

```
ruyi venv -t toolchain/gnu-plct manual venv-gnu-plct

. ~/venv-gnu-plct/bin/ruyi-activate

```

验证 GCC 版本

```
riscv64-plct-linux-gnu-gcc -v
```

编译并运行 coremark

```
git clone https://github.com/eembc/coremark  
#若无法访问GitHub，使用Gitee镜像替代  
#git clone https://gitee.com/mirrors_eembc/coremark

cd coremark

make CC=riscv64-plct-linux-gnu-gcc 
XCFLAGS="-march=rv64imafdcv_zicbom_zicboz_zicntr_zicond_zicsr_zifencei_zihintpause_zihpm_zfh_zfhmin_zca_zcd_zba_zbb_zbc_zbs_zkt_zve32f_zve32x_zve64d\
_zve64f_zve64x_zvfh_zvfhmin_zvkt_sscofpmf_sstc_svinval_svnapot_svpbmt" compile

./coremark.exe

```

正常情况下，终端会看到类似如下输出：

```
riscv64-plct-linux-gnu-gcc -O2 -Ilinux -Iposix -I. -DFLAGS_STR=\""-O2 -march=rv64gc_zba_zbb -lrt"\" -DITERATIONS=0 -march=rv64gc_zba_zbb core_list_join.c core_main.c core_matrix.c core_state.c core_util.c posix/core_portme.c -o ./coremark.exe -lrt

«Ruyi venv-gnu-plct» work@work-sipeedlpi3aboard:~/coremark$ ./coremark.exe
2K performance run parameters for coremark.
CoreMark Size    : 666
Total ticks      : 17930
Total time (secs): 17.930000
Iterations/Sec   : 6134.969325
Iterations       : 110000
Compiler version : GCC15.1.0 20250912 (experimental)
Compiler flags   : -O2 -march=rv64gc_zba_zbb -lrt
Memory location  : Please put data memory location here
                   (e.g. code in flash, data on heap etc)
seedcrc          : 0xe9f5
[0]crclist       : 0xe714
[0]crcmatrix     : 0x1fd7
[0]crcstate      : 0x8e3a
[0]crcfinal      : 0x33ff

Correct operation validated. See README.md for run and reporting rules.
CoreMark 1.0 : 6134.969325 / GCC15.1.0 20250912 (experimental) -O2 -march=rv64gc_zba_zbb -lrt / Heap

«Ruyi venv-gnu-plct» work@work-sipeedlpi3aboard:~/coremark$ 
```

返回上级目录并退出 ruyi LLVM 虚拟环境

```
cd ..; ruyi-deactivate
```

## Coremark（LLVM）

创建并激活 ruyi 虚拟环境（LLVM）

```
ruyi venv -t toolchain/llvm-plct manual --sysroot-from gnu-plct venv-llvm-plct

. ~/venv-llvm-plct/bin/ruyi-activate
```

验证 LLVM 版本

```
clang -v
```

编译并运行 coremark（LLVM）

```
cd coremark; make clean; make CC=clang XCFLAGS="-march=rv64imafdcv_zicbom_zicboz_zicntr_zicond_zicsr_zifencei_zihintpause_zihpm_zfh_zfhmin_zca_zcd_zba_zbb_zbc_zbs_zkt_zve32f_zve32x_zve64d_zve64f_zve64x_zvfh_
zvfhmin_zvkt_sscofpmf_sstc_svinval_svnapot_svpbmt" compile

./coremark.exe
```

正常情况下，终端会看到类似如下输出：

```
-DITERATIONS=0 -march=rv64gc_zba_zbb core_list_join.c core_main.c core_matrix.c core_state.c core_util.c posix/core_portme.c -o ./coremark.exe -lrt

«Ruyi venv-llvm-plct» work@work-sipeedlpi3aboard:~/coremark$ ./coremark.exe
2K performance run parameters for coremark.
CoreMark Size    : 666
Total ticks      : 21579
Total time (secs): 21.579000
Iterations/Sec   : 5097.548543
Iterations       : 110000
Compiler version : RuyiSDK Clang 21.1.0 (https://github.com/ruyisdk/llvm-project 3623fe661ae35c6c80ac221f14d85be76aa870f RuyiSDK 20250915)
Compiler flags   : -O2 -march=rv64gc_zba_zbb -lrt
Memory location  : Please put data memory location here
                   (e.g. code in flash, data on heap etc)
seedcrc          : 0xe9f5
[0]crclist       : 0xe714
[0]crcmatrix     : 0x1fd7
[0]crcstate      : 0x8e3a
[0]crcfinal      : 0x33ff

Correct operation validated. See README.md for run and reporting rules.
CoreMark 1.0 : 5097.548543 / RuyiSDK Clang 21.1.0 (https://github.com/ruyisdk/llvm-project 3623fe661ae35c6c80ac221f14d85be76aa870f RuyiSDK 20250915) -O2 -march=rv64gc_zba_zbb -lrt / Heap

«Ruyi venv-llvm-plct» work@work-sipeedlpi3aboard:~/coremark$ █
```

返回上级目录并退出 ruyi LLVM 虚拟环境

```
cd ..; ruyi-deactivate
```
