---
sys: Ubuntu 20.04.4 LTS in Docker
sys_ver: v1.9
sys_var: null

category: getting-started
last_update: 2026-06-14

model: Canaan K510 CRB-V1.2 KIT
profile: Hello World

---

# RuyiSDK Getting Started Example

This example can be compiled and run directly on the development board, making it suitable for beginners to get started quickly.

Install the ruyi package manager

```bash
sudo apt update; sudo apt install -y wget tar zstd xz-utils git build-essential

wget https://mirror.iscas.ac.cn/ruyisdk/ruyi/tags/0.50.0/ruyi-0.50.0.amd64
chmod +x ./ruyi-0.50.0.amd64
sudo cp -v ./ruyi-0.50.0.amd64 /usr/local/bin/ruyi
```

Install the GCC and LLVM toolchains

```bash
ruyi update
ruyi install gnu-ruyisdk llvm-ruyisdk
```

## Hello World (GCC)

Create and activate a ruyi virtual environment (GCC)

```bash
ruyi venv -t gnu-ruyisdk generic gcc-env
. gcc-env/bin/ruyi-activate
```

Verify the GCC version

```bash
riscv64-ruyisdk-linux-gnu-gcc -v
```

Compile Hello World (GCC)

```bash
cat << EOF > hello.c
#include <stdio.h>

int main() {
printf("Hello, World!\n");
return 0;
}
EOF

riscv64-ruyisdk-linux-gnu-gcc -static -march=rv64imafdc hello.c -o hello-gcc
riscv64-ruyisdk-linux-gnu-objcopy --remove-section=.riscv.attributes hello-gcc hello-gcc
```

Transfer the file from the PC

```bash
python3 -m http.server 8000
```

Run the following commands in the development board's `minicom` terminal:

```bash
wget http://10.13.61.37:8000/hello-gcc -O /root/hello-gcc
chmod +x /root/hello-gcc
/root/hello-gcc
```

Output

```bash
[root@canaan ~ ]$ wget http://10.13.61.37:8000/hello-gcc -O /root/hello-gcc
Connecting to 10.13.61.37:8000 (10.13.61.37:8000)
saving to '/root/hello-gcc'
hello-gcc            100% |********************************| 4150k  0:00:00 ETA
'/root/hello-gcc' saved
[root@canaan ~ ]$ chmod +x /root/hello-gcc
[root@canaan ~ ]$ /root/hello-gcc
Hello, World!
```

Exit the ruyi GCC virtual environment

```
cd ..; ruyi-deactivate
```

## Hello World (LLVM)

Create and activate a ruyi virtual environment (LLVM)

```bash
ruyi venv -t llvm-ruyisdk generic --sysroot-from gnu-ruyisdk llvm-env
. llvm-env/bin/ruyi-activate
```

Verify the LLVM version

```
clang -v
```

Compile Hello World (LLVM)

```bash
cat > hello_k510.c << "EOF"
#include <stdio.h>
int main() {
    printf("Hello from K510 with Clang!\n");
    return 0;
}
EOF

# Static cross-compilation
clang -static --target=riscv64-linux-gnu -march=rv64imafdc hello_k510.c -o hello_k510
```

Strip the attributes section

```bash
OBJCOPY=~/tes/k510_buildroot/k510_crb_lp3_v1_2_defconfig/host/bin/riscv64-buildroot-linux-gnu-objcopy
if [ ! -f "$OBJCOPY" ]; then
    OBJCOPY=/opt/riscv64-lp64d--glibc--stable-2025.08-1/bin/riscv64-linux-objcopy
fi

$OBJCOPY --remove-section=.riscv.attributes hello_k510 hello_k510_stripped
```

Transfer the file from the PC

```bash
python3 -m http.server 8000
```

Run the following commands in the development board's `minicom` terminal:

```bash
wget http://10.13.61.37:8000/hello_k510_stripped -O /root/hello_k510_stripped
chmod +x /root/hello_k510_stripped
/root/hello_k510_stripped
```

Output

```bash
[root@canaan ~ ]$ wget http://10.13.61.37:8000/hello_k510_stripped -O /root/hell
o_k510_stripped
Connecting to 10.13.61.37:8000 (10.13.61.37:8000)
saving to '/root/hello_k510_stripped'
hello_k510_stripped  100% |********************************|  551k  0:00:00 ETA
'/root/hello_k510_stripped' saved
[root@canaan ~ ]$ chmod +x /root/hello_k510_stripped
[root@canaan ~ ]$ /root/hello_k510_stripped
Hello from K510 with Clang!
```

Exit the ruyi LLVM virtual environment

```bash
cd ..; ruyi-deactivate
```
