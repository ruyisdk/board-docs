---
sys: bianbu
sys_ver: v3.0.1
sys_var: null

category: getting-started
last_update: 2026-04-22

model: Banana Pi BPI-F3
profile: Hello World
---

# RuyiSDK Getting Started Example

This example can be compiled and run directly on the development board, making it suitable for beginners.

Install dependencies

```
sudo apt update; sudo apt install -y wget tar zstd xz-utils git build-essential
```

Install the ruyi package manager

```
wget https://fast-mirror.isrc.ac.cn/ruyisdk/ruyi/tags/0.47.0/ruyi.riscv64

chmod +x ruyi-0.47.0.riscv64

sudo cp -v ruyi-0.47.0.riscv64 /usr/local/bin/ruyi
```

Install the GCC and LLVM toolchains

```
ruyi update

ruyi install gnu-plct llvm-plct
```

## Hello World (GCC)

Create and activate the ruyi virtual environment (GCC)

```
ruyi venv -t toolchain/gnu-plct manual venv-gnu-plct

. ~/venv-gnu-plct/bin/ruyi-activate
```

Verify the GCC version

```
riscv64-plct-linux-gnu-gcc -v
```

Compile and run Hello World (GCC)

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

Under normal circumstances, the terminal displays output similar to:

```
work@work-spacemitk1xdeb1board:~$ source venv-gnu-plct/bin/ruyi-activate
<:~$ riscv64-plct-linux-gnu-gcc hello.c -o hello-gcc
«Ruyi venv-gnu-plct» work@work-spacemitk1xdeb1board:~$ ./hello-gcc
Hello, World!
«Ruyi venv-gnu-plct» work@work-spacemitk1xdeb1board:~$
```

Return to the parent directory and exit the ruyi GCC virtual environment

```
cd ..; ruyi-deactivate
```

## Hello World (LLVM)

Create and activate the ruyi virtual environment (LLVM)

```
ruyi venv -t toolchain/llvm-plct manual --sysroot-from gnu-plct venv-llvm-plct

. ~/venv-llvm-plct/bin/ruyi-activate
```

Verify the LLVM version

```
clang -v
```

Compile and run Hello World (LLVM)

```
clang hello.c -static -o hello-llvm

./hello-llvm
```

Under normal circumstances, the terminal displays output similar to:

```
<@work-spacemitk1xdeb1board:~/coremark$ ruyi-deactivate
work@work-spacemitk1xdeb1board:~/coremark$ cd ..
work@work-spacemitk1xdeb1board:~$ source venv-llvm-plct/bin/ruyi-activate
<k@work-spacemitk1xdeb1board:~$ clang hello.c -o hello-llvm
«Ruyi venv-llvm-plct» work@work-spacemitk1xdeb1board:~$ ./hello-llvm
Hello, World!
«Ruyi venv-llvm-plct» work@work-spacemitk1xdeb1board:~$
```

Return to the parent directory and exit the ruyi LLVM virtual environment

```
cd ..; ruyi-deactivate
```
