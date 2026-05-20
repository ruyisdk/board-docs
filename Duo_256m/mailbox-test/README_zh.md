---
sys: buildroot
sys_ver: v1.1.4
sys_var: v1

status: peripheral
last_update: 2026-05-03

model: Milk-V Duo (256M)
profile: Mailbox-test
---

# RuyiSDK 外设示例

安装依赖包

```Plain Text
sudo apt update; sudo apt install -y wget tar zstd xz-utils git build-essential
```

安装ruyi包管理器

```Plain Text
wget https://mirror.iscas.ac.cn/ruyisdk/ruyi/tags/0.45.0/ruyi-0.45.0.amd64
chmod +x ruyi-0.45.0.amd64
sudo cp -v ruyi-0.45.0.amd64 /usr/local/bin/ruyi
```

安装GCC工具链

```Plain Text
ruyi update
ruyi install gnu-plct 
```
## Mailbox-test

本文介绍如何使用 RuyiSDK 在 Milk-V Duo 256M 开发板上快速部署编译环境，并构建 mailbox 双核通信程序，验证大核与小核之间的通信功能。

### 1. 准备工作

* **开发板**：Milk-V Duo 256M (256M, SG2002)

* **其他**：microSD 卡、USB Type-C 数据线

#### 操作系统安装与启动验证

确保您的开发板已准备好系统。

参考文档： https://milkv.io/zh/docs/duo/getting-started/boot


### 2. 获取源码

#### 克隆源码

```bash

ruyi extract milkv-duo-examples

mv milkv-duo-examples-* duo-examples 

cd duo-examples

```

### 3. 编译应用与验证
#### 创建并激活ruyi虚拟环境（GCC）

```Plain Text
ruyi venv -t toolchain/gnu-plct milkv-duo venv-mailbox
. ~/venv-mailbox/bin/ruyi-activate
```

#### 验证GCC版本

```Plain Text
riscv64-plct-linux-gnu-gcc -v
```

正常情况下，终端会看到类似如下输出：

```
cuiqiyun@DESKTOP-FOE2N7B:~$ . ~/venv-mailbox/bin/ruyi-activate
«Ruyi venv-mailbox» cuiqiyun@DESKTOP-FOE2N7B:~$ riscv64-plct-linux-gnu-gcc -v
Using built-in specs.
COLLECT_GCC=/home/cuiqiyun/.local/share/ruyi/binaries/x86_64/gnu-plct-0.20250912.0/bin/riscv64-plct-linux-gnu-gcc
COLLECT_LTO_WRAPPER=/home/cuiqiyun/.local/share/ruyi/binaries/x86_64/gnu-plct-0.20250912.0/bin/../libexec/gcc/riscv64-plct-linux-gnu/15.1.0/lto-wrapper
Target: riscv64-plct-linux-gnu
Configured with: /work/riscv64-plct-linux-gnu/src/gcc/configure --build=x86_64-build_pc-linux-gnu --host=x86_64-build_pc-linux-gnu --target=riscv64-plct-linux-gnu --prefix=/opt/ruyi/riscv64-plct-linux-gnu --exec_prefix=/opt/ruyi/riscv64-plct-linux-gnu --with-sysroot=/opt/ruyi/riscv64-plct-linux-gnu/riscv64-plct-linux-gnu/sysroot --enable-languages=c,c++,fortran,objc,obj-c++ --with-arch=rv64gc --with-abi=lp64d --with-pkgversion='RuyiSDK 20250912 PLCT-Sources-c926bf6b4d86' --with-bugurl=https://github.com/ruyisdk/ruyisdk/issues --enable-__cxa_atexit --disable-libmudflap --enable-libgomp --disable-libquadmath --disable-libquadmath-support --disable-libmpx --with-gmp=/work/riscv64-plct-linux-gnu/buildtools --with-mpfr=/work/riscv64-plct-linux-gnu/buildtools --with-mpc=/work/riscv64-plct-linux-gnu/buildtools --with-isl=/work/riscv64-plct-linux-gnu/buildtools --enable-lto --enable-threads=posix --enable-default-pie --enable-target-optspace --enable-linker-build-id --with-linker-hash-style=gnu --enable-plugin --disable-nls --enable-multiarch --with-local-prefix=/opt/ruyi/riscv64-plct-linux-gnu/riscv64-plct-linux-gnu/sysroot --enable-long-long
Thread model: posix
Supported LTO compression algorithms: zlib zstd
gcc version 15.1.0 20250912 (experimental) (RuyiSDK 20250912 PLCT-Sources-c926bf6b4d86)
```

#### 编译 mailbox-test 程序

```Plain Text
cd mailbox-test

riscv64-plct-linux-gnu-gcc mailbox_test.c -static -o mailbox-test -O2 -lm
```

正常情况下，终端会看到类似如下输出：

```
«Ruyi venv-mailbox» cuiqiyun@DESKTOP-FOE2N7B:~/duo-examples/mailbox-test$ riscv64-plct-linux-gnu-gcc mailbox_test.c -static -o mailbox-test -O2 -lm
```



### 4.将二进制文件传输至开发板并运行

#### 将编译好的二进制传输至开发板

```Plain Text
scp mailbox-test root@192.168.42.1:~
```

正常情况下，终端会看到类似如下输出：

```
«Ruyi venv-mailbox» cuiqiyun@DESKTOP-FOE2N7B:~/duo-examples/mailbox-test$ scp mailbox-test root@192.168.42.1:~
root@192.168.42.1's password:
mailbox-test                                                                          100% 3005KB   3.5MB/s   00:00
```

#### SSH连接到开发板

```Plain Text
ssh root@192.168.42.1
```

正常情况下，终端会看到类似如下输出：

```
«Ruyi venv-mailbox» cuiqiyun@DESKTOP-FOE2N7B:~/duo-examples/mailbox-test$ ssh root@192.168.42.1
root@192.168.42.1's password:
```

#### 运行 mailbox-test 程序

```Plain Text
./mailbox-test
```

正常情况下，终端会看到类似如下输出：

```
[root@milkv-duo]~# ./mailbox-test
C906B: cmd.param_ptr = 0x2
C906B: cmd.param_ptr = 0x3
[root@milkv-duo]~#
```
