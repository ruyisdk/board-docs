---
sys: Bianbu
sys_ver: 4.0.6
sys_var: LXQt

category: getting-started
last_update: 2026-09-17

model: CoM260 Kit
profile: Hello World
---

# Getting Started with RuyiSDK
Install the required packages

```
sudo apt update; sudo apt install -y wget tar zstd xz-utils git build-essential
```

Install the ruyi package manager (see the [official installation guide](https://ruyisdk.org/docs/Package-Manager/installation) for other methods)

```bash
wget https://mirror.iscas.ac.cn/ruyisdk/ruyi/tags/0.52.0/ruyi-0.52.0.riscv64
chmod +x ./ruyi-0.52.0.riscv64
sudo cp -v ./ruyi-0.52.0.riscv64 /usr/local/bin/ruyi
```

Install the GCC and LLVM toolchains

```
ruyi update

ruyi install gnu-ruyisdk llvm-ruyisdk
```

## Hello World (GCC)

Create and activate the ruyi virtual environment (GCC)
```
ruyi venv -t gnu-ruyisdk manual venv-gnu-ruyisdk-com260-kit

. venv-gnu-ruyisdk-com260-kit/bin/ruyi-activate
```

Verify the GCC version

```
riscv64-ruyisdk-linux-gnu-gcc -v
```

Compile and run Hello World (GCC)

```
cat << EOF > hello.c
#include <stdio.h>
int main() {
printf("Hello, World!\n");
return 0;
}
EOF
riscv64-ruyisdk-linux-gnu-gcc hello.c -o hello-gcc
./hello-gcc
```

Normally, the terminal displays output similar to the following:

```
Hello, World!
```

Exit the ruyi GCC virtual environment

```
ruyi-deactivate
```

## Hello World (LLVM)

Create and activate the ruyi virtual environment (LLVM)

```
ruyi venv -t llvm-ruyisdk manual --sysroot-from gnu-ruyisdk venv-llvm-ruyisdk-com260-kit

. venv-llvm-ruyisdk-com260-kit/bin/ruyi-activate
```

Verify the LLVM version

```
clang -v
```

Compile and run Hello World (LLVM)

```
clang hello.c -o hello-llvm; ./hello-llvm
```

Normally, the terminal displays output similar to the following:

```
Hello, World!
```

Exit the ruyi LLVM virtual environment

```
ruyi-deactivate
```
