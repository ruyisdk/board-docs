---
sys: buildroot
sys_ver: v1.1.4
sys_var: v1

status: basics
last_update: 2026-04-03
---

#  RuyiSDK 基础示例
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
ruyi venv -t toolchain/gnu-plct milkv-duo venv-gnu-plct-duo

. ~/venv-gnu-plct/bin/ruyi-activate
```

验证GCC版本

```
riscv64-plct-linux-gnu-gcc -v
```

编译coremark（GCC）
 
```
git clone https://github.com/eembc/coremark
cd coremark
make CC=riscv64-plct-linux-gnu-gcc XCFLAGS="-mcpu=thead-c906 -static" compile
mv coremark.exe coremark-gcc
```

将GCC构建的二进制传输至开发板

```
scp ../coremark-gcc root@192.168.42.1:~
```

返回上级目录并退出ruyi GCC虚拟环境

```
cd ..; ruyi-deactivate
```

SSH连接到开发板并执行编译好的二进制

```
ssh root@192.168.42.1

#如提示Host key verification failed：

#打开当前用户目录下的 .ssh/known_hosts目录，删除192.168.42.1对应行

#登录密码为milkv，提示Are you sure you want to continue connecting时输入yes回车即可

./coremark-gcc
```

正常情况下，终端会看到类似如下输出：

```
[root@milkv-duo]~# ./coremark-gcc
2K performance run parameters for coremark.
CoreMark Size    : 666
Total ticks      : 13853
Total time (s)   : 13.853000
Iterations/Sec   : 2165.595900
Iterations       : 30000
Compiler version : GCC15.1.0 20250912 (experimental)
Compiler flags   : -O2 -mcpu=thead-c906 -static -lrt
Memory location  : Please put data memory location here
                   (e.g. code in flash, data on heap etc)
seedcrc          : 0xe9f5
[0]crc list      : 0x714
[0]crc matrix    : 0x1fd7
[0]crc state     : 0x8e3a
[0]crc final     : 0x5275
Correct operation validated. See README.md for rules.
CoreMark 1.0: 2165.595900 / GCC15.1.0 20250912 (experimental) -O2 -mcpu=thead-c906 -static -lrt / Heap
[root@milkv-duo]~# ./hello-llvm
Hello, World!
[root@milkv-duo]~#
```
## Coremark (LLVM版) 
创建并激活ruyi虚拟环境（LLVM）

```
ruyi venv -t toolchain/llvm-plct manual --sysroot-from gnu-plct venv-llvm-plct
. ~/venv-llvm-plct/bin/ruyi-activate
```

验证LLVM版本

```
clang -v
```
编译coremark（LLVM）

```
cd coremark; make clean
make CC=clang XCFLAGS="-march=rv64imafdc_xtheadba_xtheadbb_xtheadbs_xtheadcmo_\
xtheadcondmov_xtheadfmemidx_xtheadmac_xtheadmemidx_xtheadmempair_xtheadsync -static" compile
mv coremark.exe coremark-llvm
```

将LLVM构建的二进制传输到开发板

```
scp ../coremark-llvm root@192.168.42.1:~
```

返回上级目录并退出ruyi GCC虚拟环境

```
cd ..; ruyi-deactivate
```

SSH连接到开发板并执行编译好的二进制

```
ssh root@192.168.42.1

#如提示Host key verification failed：

#打开当前用户目录下的 .ssh/known_hosts目录，删除192.168.42.1对应行

#登录密码为milkv，提示Are you sure you want to continue connecting时输入yes回车即可

./coremark-llvm
```

正常情况下，终端会看到类似如下输出：

```
2K performance run parameters for coremark.
CoreMark Size    : 666
Total ticks      : 13939
Total time (secs): 13.939000
Iterations/Sec   : 2152.234737
Iterations       : 30000
Compiler version : RuyiSDK Clang 21.1.0 (https://github.com/ruyisdk/llvm-project 3623fe661ae35c6c80ac221f14d85be76aa870f RuyiSDK 20250915)
Compiler flags   : -O2 -march=rv64imafdc_xtheadba_xtheadbb_xtheadbs_xtheadcmo_xtheadcondmov_xtheadfmemidx_xtheadmac_xtheadmemidx_xtheadmempair_xtheadsync -static -lrt
Memory location  : Please put data memory location here
                   (e.g. code in flash, data on heap etc)
seedcrc          : 0xe9f5
[0]crclist       : 0xe714
[0]crcmatrix     : 0x1fd7
[0]crcstate      : 0x8e3a
[0]crcfinal      : 0x5275
Correct operation validated. See README.md for run and reporting rules.
CoreMark 1.0 : 2152.234737 / RuyiSDK Clang 21.1.0 (https://github.com/ruyisdk/llvm-project 3623fe661ae35c6c80ac221f14d85be76aa870f RuyiSDK 20250915) -O2 -march=rv64imafdc_xtheadba_xtheadbb_xtheadbs_xtheadcmo_xtheadcondmov_xtheadfmemidx_xtheadmac_xtheadmemidx_xtheadmempair_xtheadsync -static -lrt / Heap
[root@milkv-duo]~#
```
