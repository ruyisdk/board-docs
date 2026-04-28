# 使用 RuyiSDK 在 Milk-V Duo256m 上编译运行 mailbox-test 教程

本教程以在Milk-V Duo256m上编译运行mailbox-test为例，基于mailbox通信机制验证RuyiSDK对RISC-V架构的编译适配性，以及开发板核间/外设mailbox通信的功能正确性。

## 1.准备工作

### 下载系统镜像

```Plain Text
https://github.com/milkv-duo/duo-buildroot-sdk-v2/releases/download/v2.0.1/milkv-duo256m-musl-riscv64-sd_v2.0.1.img.zip
```

### 解压系统镜像

```Plain Text
unzip milkv-duo256m-musl-riscv64-sd_v2.0.1.img.zip
```

### 系统镜像烧录进存储卡

```Plain Text
sudo dd if=milkv-duo256m-musl-riscv64-sd_v2.0.1.img of=/dev/sdX bs=1M; sync
```

### 安装依赖包

```Plain Text
sudo apt update; sudo apt install -y wget tar zstd xz-utils git build-essential
```

### 安装ruyi包管理器

```Plain Text
wget https://mirror.iscas.ac.cn/ruyisdk/ruyi/tags/0.45.0/ruyi-0.45.0.amd64
chmod +x ruyi-0.45.0.amd64
sudo cp -v ruyi-0.45.0.amd64 /usr/local/bin/ruyi
```

### 安装GCC工具链

```Plain Text
ruyi update
ruyi install gnu-plct 
```

## 2.获取 mailbox-test 源码并编译

### 创建并激活ruyi虚拟环境（GCC）

```Plain Text
ruyi venv -t toolchain/gnu-plct milkv-duo venv-mailbox
. ~/venv-mailbox/bin/ruyi-activate
```

### 验证GCC版本

```Plain Text
riscv64-plct-linux-gnu-gcc -v
```

#### log：

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



### 获取 mailbox-test 源码

Milk-V Duo官方提供了mailbox相关测试代码，直接克隆官方示例仓库：

```Plain Text
git clone https://github.com/milkv-duo/duo-examples.git
cd duo-examples/mailbox-test
```

#### log：

```
«Ruyi venv-mailbox» cuiqiyun@DESKTOP-FOE2N7B:~$ git clone https://github.com/milkv-duo/duo-examples.git
fatal: destination path 'duo-examples' already exists and is not an empty directory.
«Ruyi venv-mailbox» cuiqiyun@DESKTOP-FOE2N7B:~$ cd duo-examples/mailbox-test
```

### 编译 mailbox-test 测试程序

```Plain Text
riscv64-plct-linux-gnu-gcc mailbox_test.c -static -o mailbox-test -O2 -lm
```

#### log：

```
«Ruyi venv-mailbox» cuiqiyun@DESKTOP-FOE2N7B:~/duo-examples/mailbox-test$ riscv64-plct-linux-gnu-gcc mailbox_test.c -static -o mailbox-test -O2 -lm
```



## 3.将二进制文件传输至开发板并运行验证

### 将编译好的二进制传输至开发板

```Plain Text
scp mailbox-test root@192.168.42.1:~
```

#### log：

```
«Ruyi venv-mailbox» cuiqiyun@DESKTOP-FOE2N7B:~/duo-examples/mailbox-test$ scp mailbox-test root@192.168.42.1:~
root@192.168.42.1's password:
mailbox-test                                                                          100% 3005KB   3.5MB/s   00:00
```

### SSH连接到开发板

```Plain Text
ssh root@192.168.42.1
```

#### log：

```
«Ruyi venv-mailbox» cuiqiyun@DESKTOP-FOE2N7B:~/duo-examples/mailbox-test$ ssh root@192.168.42.1
root@192.168.42.1's password:
```

### 运行 mailbox-test 测试程序

```Plain Text
./mailbox-test
```

#### log：

```
[root@milkv-duo]~# ./mailbox-test
C906B: cmd.param_ptr = 0x2
C906B: cmd.param_ptr = 0x3
[root@milkv-duo]~#
```
