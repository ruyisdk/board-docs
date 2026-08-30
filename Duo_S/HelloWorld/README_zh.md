---
sys: debian
sys_ver: v1.6.35
sys_var: v1

category: getting-started
last_update: 2026-04-06

model: Milk-V Duo S
profile: Hello World
---

# RuyiSDK 入门示例

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

## Hello World (GCC) 

创建并激活 ruyi 虚拟环境（GCC）

```
ruyi venv -t toolchain/gnu-plct manual venv-gnu-plct

. ~/venv-gnu-plct/bin/ruyi-activate
```

验证 GCC 版本

```
riscv64-plct-linux-gnu-gcc -v
```

编译 Hello World（GCC）

```
cat > hello.c << 'EOF'
#include <stdio.h>

int main() {
    printf("Hello, World!\n");
    return 0;
}
EOF

riscv64-plct-linux-gnu-gcc hello.c -o hello-gcc
```

正常情况下，终端会看到类似如下输出:

```
debian@duos-1cae:~$ source venv-gnu-plct/bin/ruyi-activate
<an@duos-1cae:~$ riscv64-plct-linux-gnu-gcc hello.c -o hello-gcc
«Ruyi venv-gnu-plct» debian@duos-1cae:~$
```
运行 Hello World（GCC）

```
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

返回上级目录并退出 ruyi GCC 虚拟环境

```
cd ..; ruyi-deactivate
```
## Hello World (LLVM) 

创建并激活 ruyi 虚拟环境（LLVM）

```
ruyi venv -t toolchain/llvm-plct manual --sysroot-from gnu-plct venv-llvm-plct

. ~/venv-llvm-plct/bin/ruyi-activate
```

验证 LLVM 版本

```
clang -v
```

编译 Hello World（LLVM）

```
clang hello.c -static -o hello-llvm
```

正常情况下，终端会看到类似如下输出：

```
debian@duos-1cae:~$ source venv-llvm-plct/bin/ruyi-activate
«Ruyi venv-llvm-plct» debian@duos-1cae:~$ clang hello.c -o hello-llvm
«Ruyi venv-llvm-plct» debian@duos-1cae:~$
```
运行 Hello World（LLVM）

```
./hello-llvm
```

正常情况下，终端会看到类似如下输出：

```
«Ruyi venv-llvm-plct» debian@duos-1cae:~$ ./hello-llvm
Hello, World!
«Ruyi venv-llvm-plct» debian@duos-1cae:~$
```
返回上级目录并退出 ruyi LLVM 虚拟环境

```
cd ..; ruyi-deactivate
```