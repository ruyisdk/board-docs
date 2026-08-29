---
sys: revyos
sys_ver: "20251030"
sys_var: null

category: getting-started
last_update: 2026-04-19

model: Milk-V Pioneer
profile: Hello World
---

# RuyiSDK Getting Started Example

This example can be compiled and run directly on the development board, making it suitable for beginners.

Install the ruyi package manager

```
sudo apt update; sudo apt install -y python3-ruyi
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
debian@revyos-pioneer:~$ source venv-gnu-plct/bin/ruyi-activate
<an@revyos-pioneer:~$ riscv64-plct-linux-gnu-gcc hello.c -o hello-gcc
«Ruyi venv-gnu-plct» debian@revyos-pioneer:~$ ./hello-gcc
Hello, World!
«Ruyi venv-gnu-plct» debian@revyos-pioneer:~$ █

```


Exit the ruyi GCC virtual environment

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
clang hello.c -o hello-llvm; ./hello-llvm
```

Under normal circumstances, the terminal displays output similar to:

```
«Ruyi venv-gnu-plct» debian@revyos-pioneer:~/coremark$ ruyi-deactivate
debian@revyos-pioneer:~/coremark$ cd ..
debian@revyos-pioneer:~$ source venv-llvm-plct/bin/ruyi-activate
«Ruyi venv-llvm-plct» debian@revyos-pioneer:~$ clang hello.c -o hello-llvm
«Ruyi venv-llvm-plct» debian@revyos-pioneer:~$ ./hello-llvm
Hello, World!
«Ruyi venv-llvm-plct» debian@revyos-pioneer:~$

```

Exit the ruyi LLVM virtual environment

```
cd ..; ruyi-deactivate
```
