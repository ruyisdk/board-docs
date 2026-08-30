---
sys: debian
sys_ver: v1.6.35
sys_var: v1

category: getting-started
last_update: 2026-04-06

model: Milk-V Duo S
profile: Hello World
---

# RuyiSDK Getting Started Example

This example can be compiled and run directly on the development board, making it suitable for beginners.

Install dependencies

```
sudo apt update; sudo apt install -y wget tar zstd xz-utils git build-essential
```

Install the ruyi package manager (see the [official installation guide](https://ruyisdk.org/docs/Package-Manager/installation) for other methods)

```bash
wget https://mirror.iscas.ac.cn/ruyisdk/ruyi/tags/0.51.0/ruyi-0.51.0.riscv64
chmod +x ./ruyi-0.51.0.riscv64
sudo cp -v ./ruyi-0.51.0.riscv64 /usr/local/bin/ruyi
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

Compile Hello World (GCC)

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

Under normal circumstances, the terminal displays output similar to:

```
debian@duos-1cae:~$ source venv-gnu-plct/bin/ruyi-activate
<an@duos-1cae:~$ riscv64-plct-linux-gnu-gcc hello.c -o hello-gcc
«Ruyi venv-gnu-plct» debian@duos-1cae:~$
```

Run Hello World (GCC)

```
./hello-gcc
```

Under normal circumstances, the terminal displays output similar to:

```
debian@duos-1cae:~$ source venv-gnu-plct/bin/ruyi-activate
<an@duos-1cae:~$ riscv64-plct-linux-gnu-gcc hello.c -o hello-gcc
«Ruyi venv-gnu-plct» debian@duos-1cae:~$ ./hello-gcc
Hello, World!
«Ruyi venv-gnu-plct» debian@duos-1cae:~$
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

Compile Hello World (LLVM)

```
clang hello.c -static -o hello-llvm
```

Under normal circumstances, the terminal displays output similar to:

```
debian@duos-1cae:~$ source venv-llvm-plct/bin/ruyi-activate
«Ruyi venv-llvm-plct» debian@duos-1cae:~$ clang hello.c -o hello-llvm
«Ruyi venv-llvm-plct» debian@duos-1cae:~$
```

Run Hello World (LLVM)

```
./hello-llvm
```

Under normal circumstances, the terminal displays output similar to:

```
«Ruyi venv-llvm-plct» debian@duos-1cae:~$ ./hello-llvm
Hello, World!
«Ruyi venv-llvm-plct» debian@duos-1cae:~$
```

Return to the parent directory and exit the ruyi LLVM virtual environment

```
cd ..; ruyi-deactivate
```
