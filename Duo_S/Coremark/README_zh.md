---
sys: buildroot
sys_ver: v1.1.4
sys_var: v1

status: basics
last_update: 2026-04-06
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

## Coremark（GCC）

创建并激活 ruyi 虚拟环境（GCC）

```
ruyi venv -t toolchain/gnu-plct milkv-duo venv-gnu-plct-duo

. ~/venv-gnu-plct-duo/bin/ruyi-activate
```

验证 GCC 版本

```
riscv64-plct-linux-gnu-gcc -v
```

获取源码并编译 coremark

```
git clone https://github.com/eembc/coremark  
#若无法访问GitHub，使用Gitee镜像替代  
#git clone https://gitee.com/mirrors_eembc/coremark

cd coremark

make CC=riscv64-plct-linux-gnu-gcc XCFLAGS="-mcpu=thead-c906 -static" compile

mv coremark.exe coremark-gcc
```

正常情况下，终端会看到类似如下输出：

```
debian@duos-1cae:~$ source venv-gnu-plct/bin/ruyi-activate
<an@duos-1cae:~$ riscv64-plct-linux-gnu-gcc hello.c -o hello-gcc
«Ruyi venv-gnu-plct» debian@duos-1cae:~$ ./hello-gcc
Hello, World!

«Ruyi venv-gnu-plct» debian@duos-1cae:~$ cd coremark
<ake CC=riscv64-plct-linux-gnu-gcc XCFLAGS="-mcpu=thead-c906" compile
riscv64-plct-linux-gnu-gcc -O2 -Ilinux -I. -DFLAGS_STR=\""-O2 -mcpu=thead-c906"\" -DITERATIONS=0 -mcpu=thead-c906 core_list_join.c core_main.c core_matrix.c core_state.c core_util.c posix/core_portme.c -o ./coremark.exe -lrt
«Ruyi venv-gnu-plct» debian@duos-1cae:~/coremark$
```

将 GCC 构建的二进制传输至开发板

```
scp ../coremark-gcc root@192.168.42.1:~
```

返回上级目录并退出 ruyi GCC 虚拟环境

```
cd ..; ruyi-deactivate
```

SSH 连接到开发板并执行编译好的二进制

```
ssh root@192.168.42.1

#如提示Host key verification failed：

#打开当前用户目录下的 .ssh/known_hosts目录，删除192.168.42.1对应行

#登录密码为milkv，提示Are you sure you want to continue connecting时输入yes回车即可

./coremark-gcc

```
正常情况下，终端会看到类似如下输出：

```
«Ruyi venv-gnu-plct» debian@duos-1cae:~/coremark$ ./coremark.exe
2K performance run parameters for coremark.
CoreMark Size    : 666
Total ticks      : 11883
Total time (secs): 11.883000
Iterations/Sec   : 3366.153328
Iterations       : 40000
Compiler version : GCC15.1.0 20250912 (experimental)
Compiler flags   : -O2 -mcpu=thead-c906 -lrt
Memory location  : Please put data memory location here
                   (e.g. code in flash, data on heap etc)
seedcrc          : 0xe9f5
[0]crclist       : 0xe714
[0]crcmatrix     : 0x1fd7
[0]crcstate      : 0x8e3a
[0]crcfinal       : 0x25b5
Correct operation validated. See README.md for run and reporting rules.
CoreMark 1.0 : 3366.153328 / GCC15.1.0 20250912 (experimental) -O2 -mcpu=thead-c906 -lrt / Heap
«Ruyi venv-gnu-plct» debian@duos-1cae:~/coremark$
```

## Coremark（LLVM）

创建并激活 ruyi 虚拟环境（LLVM）

```
ruyi venv -t toolchain/llvm-plct manual --sysroot-from gnu-plct venv-llvm-plct-duo

. ~/venv-llvm-plct-duo/bin/ruyi-activate
```

验证 LLVM 版本

```
clang -v
```

下载源码并编译 coremark（LLVM）

```
git clone https://github.com/eembc/coremark  
#若无法访问GitHub，使用Gitee镜像替代  
#git clone https://gitee.com/mirrors_eembc/coremark

cd coremark; make clean

make CC=clang XCFLAGS="-march=rv64imafdc_xtheadba_xtheadbb_xtheadbs_xtheadcmo_\

xtheadcondmov_xtheadfmemidx_xtheadmac_xtheadmemidx_xtheadmempair_xtheadsync -static" compile

mv coremark.exe coremark-llvm
```

正常情况下，终端会看到类似如下输出：

```
«Ruyi venv-llvm-plct» debian@duos-1cae:~$ cd coremark
«Ruyi venv-llvm-plct» debian@duos-1cae:~/coremark$ make clean
rm -f ./coremark.exe ./core_list_join.o ./core_main.o ./core_matrix.o ./core_state.o ./core_util.o ./*.log *.info ./index.html
<rch=rv64imafdc_xtheadba_xtheadbb_xtheadbs_xtheadcmo_\
<dx_xtheadmac_xtheadmemidx_xtheadmempair_xtheadsync" compile
clang -O2 -Ilinux -Iposix -I. -DFLAGS_STR=\""-O2 -march=rv64imafdc_xtheadba_xtheadbb_xtheadbs_xtheadcmo_xtheadcondmov_xtheadfmemidx_xtheadmac_xtheadmemidx_xtheadmempair_xtheadsync -lrt"\" -DITERATIONS=0 -march=rv64imafdc_xtheadba_xtheadbb_xtheadbs_xtheadcmo_xtheadcondmov_xtheadfmemidx_xtheadmac_xtheadmemidx_xtheadmempair_xtheadsync core_list_join.c core_main.c core_matrix.c core_state.c core_util.c posix/core_portme.c -o ./coremark.exe -lrt
«Ruyi venv-llvm-plct» debian@duos-1cae:~/coremark$ 
```


将 GCC 构建的二进制传输至开发板

```
scp ../coremark-llvm root@192.168.42.1:~
```

返回上级目录并退出 ruyi LLVM 虚拟环境

```
cd ..; ruyi-deactivate
```

SSH 连接到开发板并执行编译好的二进制

```
ssh root@192.168.42.1

#如提示Host key verification failed：

#打开当前用户目录下的 .ssh/known_hosts目录，删除192.168.42.1对应行

#登录密码为milkv，提示Are you sure you want to continue connecting时输入yes回车即可

./coremark-llvm

```

正常情况下，终端会看到类似如下输出：

```
«Ruyi venv-llvm-plct» debian@duos-1cae:~/coremark$ ./coremark.exe
2K performance run parameters for coremark.
CoreMark Size    : 666
Total ticks      : 14666
Total time (secs): 14.666000
Iterations/Sec   : 2727.396700
Iterations       : 40000
Compiler version : RuyiSDK Clang 21.1.0 (https://github.com/ruyisdk/llvm-project 3623fe661ae35c6c80ac221f14d85be76aa870f RuyiSDK 20250915)
Compiler flags   : -O2 -march=rv64imafdc_xtheadba_xtheadbb_xtheadbs_xtheadcmo_xtheadcondmov_xtheadfmemidx_xtheadmac_xtheadmemidx_xtheadmempair_xtheadsync -lrt
Memory location  : Please put data memory location here
                   (e.g. code in flash, data on heap etc)
seedcrc          : 0xe9f5
[0] crclist      : 0xe714
[0] crcmatrix    : 0x1fd7
[0] crcstate     : 0x8e3a
[0] crcfinal     : 0x25b5
Correct operation validated. See README.md for run and reporting rules.
CoreMark 1.0 : 2727.396700 / RuyiSDK Clang 21.1.0 (https://github.com/ruyisdk/llvm-project 3623fe661ae35c6c80ac221f14d85be76aa870f RuyiSDK 20250915) -O2 -march=rv64imafdc_xtheadba_xtheadbb_xtheadbs_xtheadcmo_xtheadcondmov_xtheadfmemidx_xtheadmac_xtheadmemidx_xtheadmempair_xtheadsync -lrt / Heap
«Ruyi venv-llvm-plct» debian@duos-1cae:~/coremark$
```

