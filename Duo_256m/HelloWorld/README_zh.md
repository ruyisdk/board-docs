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

## Hello World (GCC版) 

创建并激活ruyi虚拟环境（GCC）
```
ruyi venv -t toolchain/gnu-plct milkv-duo venv-gnu-plct-duo

. ~/venv-gnu-plct/bin/ruyi-activate
```

验证GCC版本

```
riscv64-plct-linux-gnu-gcc -v
```

编译Hello World（GCC）

```
cat << EOF > hello.c

#include <stdio.h>

int main() {

    printf("Hello, World!\n");

    return 0;

}

EOF

riscv64-plct-linux-gnu-gcc hello.c -o hello-gcc

```


将GCC构建的二进制传输至开发板

```
scp ../hello-gcc root@192.168.42.1:~
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

./hello-gcc
```

正常情况下，终端会看到类似如下输出：

```
[root@milkv-duo]~# ./hello-gcc
Hello, World!
[root@milkv-duo]~#
```

## Hello World (LLVM版) 
创建并激活ruyi虚拟环境（LLVM）

```
ruyi venv -t toolchain/llvm-plct manual --sysroot-from gnu-plct venv-llvm-plct

. ~/venv-llvm-plct/bin/ruyi-activate
```
验证LLVM版本

```
clang -v
```

编译Hello World（LLVM）

```
clang hello.c -o hello-llvm; 
```


将LLVM构建的二进制传输到开发板

```
scp ../hello-llvm root@192.168.42.1:~
```

返回上级目录并退出ruyi GCC虚拟环境

```
cd ..; ruyi-deactivate
```

SSH 连接到开发板并执行编译好的二进制
```
ssh root@192.168.42.1

#如提示Host key verification failed：

#打开当前用户目录下的 .ssh/known_hosts目录，删除192.168.42.1对应行

#登录密码为milkv，提示Are you sure you want to continue connecting时输入yes回车即可

./hello-llvm
```


正常情况下，终端会看到类似如下输出：

```
[root@milkv-duo]~# ./hello-llvm
Hello, World!
[root@milkv-duo]~#
```
