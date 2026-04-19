---
sys: bianbu
sys_ver: 3.0.1
sys_var: Desktop
status: basics
last_update: 2026-04-20

model: Lichee Pi 3A
profile: Hello World
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

编译并运行Hello World（GCC）

```
cat > hello.c << 'EOF'
#include <stdio.h>

int main() {
    printf("Hello, World!\n");
    return 0;
}
EOF

riscv64-plct-linux-gnu-gcc hello.c -o hello-gcc
./hello-gcc
```

正常情况下，终端会看到类似如下输出：

```
work@work-sipeedlpi3aboard:~$ source venv-gnu-plct/bin/ruyi-activate
<@work-sipeedlpi3aboard:~$ riscv64-plct-linux-gnu-gcc hello.c -o hello-gcc
«Ruyi venv-gnu-plct» work@work-sipeedlpi3aboard:~/$ ./hello-gcc
Hello, World!
«Ruyi venv-gnu-plct» work@work-sipeedlpi3aboard:~$ █
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

编译并运行Hello World（LLVM）

```
clang hello.c -o hello-llvm; ./hello-llvm
```

正常情况下，终端会看到类似如下输出：

```
«Ruyi venv-gnu-plct» work@work-sipeedlpi3aboard:~/coremark$ ruyi-deactivate
work@work-sipeedlpi3aboard:~/coremark$ cd ..
work@work-sipeedlpi3aboard:~$ source venv-llvm-plct/bin/ruyi-activate
<k@work-sipeedlpi3aboard:~$ clang hello.c -o hello-llvm
«Ruyi venv-llvm-plct» work@work-sipeedlpi3aboard:~$ ./hello-llvm
Hello, World!
«Ruyi venv-llvm-plct» work@work-sipeedlpi3aboard:~$ 
```

退出ruyi GCC虚拟环境

```
cd ..; ruyi-deactivate
```


