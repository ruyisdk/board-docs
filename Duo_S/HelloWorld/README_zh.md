---
sys: buildroot
sys_ver: v1.1.4
sys_var: v1

status: basics
last_update: 2026-04-06
---

# RuyiSDK 基础示例

## Hello World (GCC) 

创建并激活 ruyi 虚拟环境（GCC）

```
ruyi venv -t toolchain/gnu-plct milkv-duo venv-gnu-plct-duo

. ~/venv-gnu-plct-duo/bin/ruyi-activate
```

验证 GCC 版本

```
riscv64-plct-linux-gnu-gcc -v
```

编译 Hello World（GCC）

```
cat << EOF > hello.c

#include <stdio.h>

int main() {

printf("Hello, World!\n");

return 0;

}

EOF

riscv64-plct-linux-gnu-gcc hello.c -static -o hello-gcc
```

正常情况下，终端会看到类似如下输出：

```
debian@duos-1cae:~$ source venv-gnu-plct/bin/ruyi-activate
<an@duos-1cae:~$ riscv64-plct-linux-gnu-gcc hello.c -o hello-gcc
«Ruyi venv-gnu-plct» debian@duos-1cae:~$ 
```


将 GCC 构建的二进制传输至开发板

```
scp ../hello-gcc root@192.168.42.1:~
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

./hello-gcc

```
正常情况下，终端会看到类似如下输出：

```
debian@duos-1cae:~$ source venv-gnu-plct/bin/ruyi-activate
<an@duos-1cae:~$ riscv64-plct-linux-gnu-gcc hello.c -o hello-gcc
«Ruyi venv-gnu-plct» debian@duos-1cae:~$ ./hello-gcc
Hello, World!
«Ruyi venv-gnu-plct» debian@duos-1cae:~$ 
```

## Hello World (LLVM) 

创建并激活 ruyi 虚拟环境（LLVM）

```
ruyi venv -t toolchain/llvm-plct manual --sysroot-from gnu-plct venv-llvm-plct-duo

. ~/venv-llvm-plct-duo/bin/ruyi-activate
```

验证 LLVM 版本

```
clang -v
```

编译并运行 Hello World（LLVM）

```
clang hello.c -static -o hello-llvm
```

正常情况下，终端会看到类似如下输出：

```
debian@duos-1cae:~$ source venv-llvm-plct/bin/ruyi-activate
«Ruyi venv-llvm-plct» debian@duos-1cae:~$ clang hello.c -o hello-llvm
«Ruyi venv-llvm-plct» debian@duos-1cae:~$ 
```


将 LLVM 构建的二进制传输至开发板

```
scp ../hello-llvm root@192.168.42.1:~
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

./hello-llvm

```
正常情况下，终端会看到类似如下输出：

```
«Ruyi venv-llvm-plct» debian@duos-1cae:~$ ./hello-llvm
Hello, World!
«Ruyi venv-llvm-plct» debian@duos-1cae:~$ 
```
