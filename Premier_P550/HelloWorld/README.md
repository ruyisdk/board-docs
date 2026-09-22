---
sys: fedora
sys_ver: "44"
sys_var: null

category: getting-started
last_update: 2026-09-17

model: Premier P550
profile: Hello World
---

# RuyiSDK Getting Started Example

This example can be compiled and run directly on the development board, making it suitable for beginners.

Install dependencies

```bash
sudo dnf install -y git make wget tar zstd xz
```

Install the ruyi package manager (see the [official installation guide](https://ruyisdk.org/docs/Package-Manager/installation) for other methods)

```bash
wget https://mirror.iscas.ac.cn/ruyisdk/ruyi/tags/0.52.0/ruyi-0.52.0.riscv64
chmod +x ./ruyi-0.52.0.riscv64
sudo cp -v ./ruyi-0.52.0.riscv64 /usr/local/bin/ruyi
```

Install the GCC and LLVM toolchains

```bash
ruyi update

ruyi install gnu-ruyisdk llvm-ruyisdk
```

## Hello World (GCC)

Create and activate the ruyi virtual environment (GCC)

```bash
ruyi venv -t toolchain/gnu-ruyisdk manual venv-gnu-ruyisdk
. venv-gnu-ruyisdk/bin/ruyi-activate
```

Verify the GCC version

```bash
riscv64-ruyisdk-linux-gnu-gcc -v
```

Compile and run Hello World (GCC)

```bash
cat > hello.c << 'EOF'
#include <stdio.h>

int main(void)
{
    printf("Hello, World!\n");
    return 0;
}
EOF

riscv64-ruyisdk-linux-gnu-gcc hello.c -o hello-gcc
./hello-gcc
```

Under normal circumstances, the terminal displays output similar to:

```text
«Ruyi venv-gnu-ruyisdk» [fedora@localhost ~]$ riscv64-ruyisdk-linux-gnu-gcc hello.c -o hello-gcc
«Ruyi venv-gnu-ruyisdk» [fedora@localhost ~]$ ./hello-gcc
Hello, World!
«Ruyi venv-gnu-ruyisdk» [fedora@localhost ~]$
```

Exit the ruyi GCC virtual environment

```bash
ruyi-deactivate
```

## Hello World (LLVM)

Create and activate the ruyi virtual environment (LLVM)

```bash
ruyi venv -t llvm-ruyisdk manual --sysroot-from gnu-ruyisdk venv-llvm-ruyisdk
. venv-llvm-ruyisdk/bin/ruyi-activate
```

Verify the LLVM version

```bash
clang -v
```

Compile and run Hello World (LLVM)

```bash
clang hello.c -o hello-llvm
./hello-llvm
```

Under normal circumstances, the terminal displays output similar to:

```text
«Ruyi venv-llvm-ruyisdk» [fedora@localhost ~]$ clang hello.c -o hello-llvm
«Ruyi venv-llvm-ruyisdk» [fedora@localhost ~]$ ./hello-llvm
Hello, World!
«Ruyi venv-llvm-ruyisdk» [fedora@localhost ~]$
```

Exit the ruyi LLVM virtual environment

```bash
cd ..
ruyi-deactivate
```
