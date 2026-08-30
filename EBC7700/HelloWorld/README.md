---
sys: ubuntu
sys_ver: 24.04
sys_var: null

category: getting-started
last_update: 2026-07-06

model: EBC7700
profile: Hello World
---

# RuyiSDK Getting Started Example

Install dependencies

```bash
sudo apt update
sudo apt install -y wget tar zstd xz-utils git build-essential
```

Install the ruyi package manager (see the [official installation guide](https://ruyisdk.org/docs/Package-Manager/installation) for other methods)

```bash
wget https://mirror.iscas.ac.cn/ruyisdk/ruyi/tags/0.51.0/ruyi-0.51.0.riscv64
chmod +x ./ruyi-0.51.0.riscv64
sudo cp -v ./ruyi-0.51.0.riscv64 /usr/local/bin/ruyi
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

Compile Hello World (GCC)

```bash
cat > hello.c << 'EOF'
#include <stdio.h>

int main() {
    printf("Hello, World!\n");
    return 0;
}
EOF

riscv64-ruyisdk-linux-gnu-gcc hello.c -o hello-gcc

```
Run the generated file

```bash
./hello-gcc
```

Under normal circumstances, the terminal displays output similar to:

```text
«Ruyi venv-gnu-ruyisdk» ubuntu@ubuntu:~$ ./hello-gcc
Hello, World!
«Ruyi venv-gnu-ruyisdk» ubuntu@ubuntu:~$
```
Exit the ruyi GCC virtual environment

```bash
ruyi-deactivate
```

## Hello World (LLVM)
Create and activate the ruyi virtual environment (LLVM)

```bash
ruyi venv -t toolchain/llvm-ruyisdk manual --sysroot-from gnu-ruyisdk venv-llvm-ruyisdk

. venv-llvm-ruyisdk/bin/ruyi-activate
```
Verify the LLVM version

```bash
clang -v
```

Compile Hello World (LLVM)

```bash
clang hello.c -o hello-llvm
```

Run the generated file:
```bash
./hello-llvm
```

Under normal circumstances, the terminal displays output similar to:

```text
«Ruyi venv-llvm-ruyisdk» ubuntu@ubuntu:~$ ./hello-llvm
Hello, World!
«Ruyi venv-llvm-ruyisdk» ubuntu@ubuntu:~$
```
Exit the ruyi LLVM virtual environment

```bash
ruyi-deactivate
```
