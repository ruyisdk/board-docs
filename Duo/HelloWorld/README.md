---
sys: buildroot
sys_ver: v1.1.4
sys_var: v1

category: getting-started
last_update: 2026-04-03

model: Milk-V Duo (64M)
profile: Hello World
---

# RuyiSDK Getting Started Example

Install dependencies

```
sudo apt update; sudo apt install -y wget tar zstd xz-utils git build-essential
```

Install the ruyi package manager

```
wget https://mirror.iscas.ac.cn/ruyisdk/ruyi/tags/0.47.0/ruyi-0.47.0.amd64

chmod +x ./ruyi-0.47.0.amd64

sudo cp -v ./ruyi-0.47.0.amd64 /usr/local/bin/ruyi
```

Install the GCC and LLVM toolchains

```
ruyi update

ruyi install gnu-plct llvm-plct
```

## Hello World (GCC)

Create and activate the ruyi virtual environment (GCC)
```
ruyi venv -t toolchain/gnu-plct generic venv-gnu-plct-duo

. ~/venv-gnu-plct-duo/bin/ruyi-activate
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

Transfer the GCC-built binary to the development board

```
scp ../hello-gcc root@192.168.42.1:~
```

Return to the parent directory and exit the ruyi GCC virtual environment

```
cd ..; ruyi-deactivate
```

Connect to the development board over SSH and run the compiled binary

```
ssh root@192.168.42.1

# If you see Host key verification failed:

# Open the .ssh/known_hosts file in the current user's home directory and delete the line corresponding to 192.168.42.1

# The login password is milkv; when prompted with Are you sure you want to continue connecting, enter yes and press Enter

./hello-gcc
```

Under normal circumstances, the terminal displays output similar to:

```
[root@milkv-duo]~# ./hello-gcc
Hello, World!
[root@milkv-duo]~#
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
clang hello.c -o hello-llvm;
```

Transfer the LLVM-built binary to the development board
```
scp ../hello-llvm root@192.168.42.1:~
```

Return to the parent directory and exit the ruyi LLVM virtual environment

```
cd ..; ruyi-deactivate
```

Connect to the development board over SSH and run the compiled binary
```
ssh root@192.168.42.1

# If you see Host key verification failed：

# Open the .ssh/known_hosts file in the current user's home directory and delete the line corresponding to 192.168.42.1

# The login password is milkv; when prompted with Are you sure you want to continue connecting, enter yes and press Enter

./hello-llvm
```


Under normal circumstances, the terminal displays output similar to:

```
[root@milkv-duo]~# ./hello-llvm
Hello, World!
[root@milkv-duo]~#
```
