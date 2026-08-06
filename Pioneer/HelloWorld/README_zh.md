---
sys: revyos
sys_ver: "20251030"
sys_var: null

category: getting-started
last_update: 2026-04-19

model: Milk-V Pioneer
profile: Hello World
---

# RuyiSDK 入门示例

可直接在开发板上进行编译和运行的示例，适合初学者快速上手。

安装ruyi包管理器

```
sudo apt update; sudo apt install -y python3-ruyi
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
debian@revyos-pioneer:~$ source venv-gnu-plct/bin/ruyi-activate
<an@revyos-pioneer:~$ riscv64-plct-linux-gnu-gcc hello.c -o hello-gcc
«Ruyi venv-gnu-plct» debian@revyos-pioneer:~$ ./hello-gcc
Hello, World!
«Ruyi venv-gnu-plct» debian@revyos-pioneer:~$ █

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
«Ruyi venv-gnu-plct» debian@revyos-pioneer:~/coremark$ ruyi-deactivate
debian@revyos-pioneer:~/coremark$ cd ..
debian@revyos-pioneer:~$ source venv-llvm-plct/bin/ruyi-activate
«Ruyi venv-llvm-plct» debian@revyos-pioneer:~$ clang hello.c -o hello-llvm
«Ruyi venv-llvm-plct» debian@revyos-pioneer:~$ ./hello-llvm
Hello, World!
«Ruyi venv-llvm-plct» debian@revyos-pioneer:~$

```

退出ruyi GCC虚拟环境

```
cd ..; ruyi-deactivate
```


