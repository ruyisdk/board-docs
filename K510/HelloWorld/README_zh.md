---
sys: Ubuntu 20.04.4 LTS in Docker
sys_ver: v1.9
sys_var: null

category: getting-started
last_update: 2026-06-14

model: Canaan K510 CRB-V1.2 KIT
profile: Hello World

---

# RuyiSDK 入门示例

可直接在开发板上进行编译和运行的示例，适合初学者快速上手。

安装ruyi包管理器

```bash
sudo apt update; sudo apt install -y wget tar zstd xz-utils git build-essential

wget https://mirror.iscas.ac.cn/ruyisdk/ruyi/tags/0.50.0/ruyi-0.50.0.amd64
chmod +x ./ruyi-0.50.0.amd64
sudo cp -v ./ruyi-0.50.0.amd64 /usr/local/bin/ruyi
```

安装GCC和LLVM工具链

```bash
ruyi update
ruyi install gnu-ruyisdk llvm-ruyisdk
```

## Hello World (GCC版)

创建并激活ruyi虚拟环境（GCC）

```bash
ruyi venv -t gnu-ruyisdk generic gcc-env
. gcc-env/bin/ruyi-activate
```

验证GCC版本

```bash
riscv64-ruyisdk-linux-gnu-gcc -v
```

编译Hello World（GCC）

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

PC端传输

```bash
python3 -m http.server 8000
```

在开发板的`minicom`终端里运行：

```bash
wget http://10.13.61.37:8000/hello-gcc -O /root/hello-gcc
chmod +x /root/hello-gcc
/root/hello-gcc
```

输出结果

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

编译CoreMark（GCC）

```bash
git clone https://github.com/eembc/coremark
cd coremark
make CC=riscv64-ruyisdk-linux-gnu-gcc XCFLAGS="-static -march=rv64imafd" compile
mv coremark.exe coremark-gcc
riscv64-ruyisdk-linux-gnu-objcopy --remove-section=.riscv.attributes coremark-gcc coremark-gcc
```

PC端传输CoreMark

```bash
python3 -m http.server 8000
```

在开发板的`minicom`终端里运行：

```bash
wget http://10.13.61.37:8000/coremark-gcc -O /root/coremark-gcc
chmod +x /root/coremark-gcc
/root/coremark-gcc
```

CoreMark结果节选

```text
2K performance run parameters for coremark.
CoreMark Size    : 666
Total ticks      : 15336
Total time (secs): 15.336000
Iterations/Sec   : 1956.181534
Iterations       : 30000
Memory location  : Please put data memory location here
                  (e.g. code in flash, data on heap etc)
seedcrc          : 0xe9f5
[0]crclist       : 0xe714
[0]crcmatrix     : 0x1fd7
[0]crcstate      : 0x8e3a
[0]crcfinal      : 0x5275
Correct operation validated. See README.md for run and reporting rules.
```

退出ruyi GCC虚拟环境

```
cd ..; ruyi-deactivate
```

## Hello World (LLVM版)

创建并激活ruyi虚拟环境（LLVM）

```bash
ruyi venv -t llvm-ruyisdk generic --sysroot-from gnu-ruyisdk llvm-env
. llvm-env/bin/ruyi-activate
```

验证LLVM版本

```
clang -v
```

编译Hello World（LLVM）

```bash
cat > hello_k510.c << "EOF"
#include <stdio.h>
int main() {
    printf("Hello from K510 with Clang!\n");
    return 0;
}
EOF

#静态交叉编译
clang -static --target=riscv64-linux-gnu -march=rv64imafdc hello_k510.c -o hello_k510
```

剥离属性段

```bash
OBJCOPY=~/tes/k510_buildroot/k510_crb_lp3_v1_2_defconfig/host/bin/riscv64-buildroot-linux-gnu-objcopy
if [ ! -f "$OBJCOPY" ]; then
    OBJCOPY=/opt/riscv64-lp64d--glibc--stable-2025.08-1/bin/riscv64-linux-objcopy
fi

$OBJCOPY --remove-section=.riscv.attributes hello_k510 hello_k510_stripped
```

PC端传输

```bash
python3 -m http.server 8000
```

在开发板的`minicom`终端里运行：

```bash
wget http://10.13.61.37:8000/hello_k510_stripped -O /root/hello_k510_stripped
chmod +x /root/hello_k510_stripped
/root/hello_k510_stripped
```

输出结果

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

编译CoreMark（LLVM）

```bash
cd coremark
make clean
make CC=clang XCFLAGS="-static --target=riscv64-linux-gnu -march=rv64imafdc -Iposix" compile
mv coremark.exe coremark-llvm
```

剥离CoreMark属性段

```bash
OBJCOPY=~/tes/k510_buildroot/k510_crb_lp3_v1_2_defconfig/host/bin/riscv64-buildroot-linux-gnu-objcopy
if [ ! -f "$OBJCOPY" ]; then
    OBJCOPY=/opt/riscv64-lp64d--glibc--stable-2025.08-1/bin/riscv64-linux-objcopy
fi

$OBJCOPY --remove-section=.riscv.attributes coremark-llvm coremark_llvm
```

PC端传输CoreMark

```bash
python3 -m http.server 8000
```

在开发板的`minicom`终端里运行：

```bash
wget http://10.13.61.37:8000/coremark_llvm -O /root/coremark_llvm
chmod +x /root/coremark_llvm
/root/coremark_llvm
```

CoreMark结果节选

```text
2K performance run parameters for coremark.
CoreMark Size    : 666
Total ticks      : 17325
Total time (secs): 17.325000
Iterations/Sec   : 1731.601732
Iterations       : 30000
Memory location  : Please put data memory location here
                  (e.g. code in flash, data on heap etc)
seedcrc          : 0xe9f5
[0]crclist       : 0xe714
[0]crcmatrix     : 0x1fd7
[0]crcstate      : 0x8e3a
[0]crcfinal      : 0x5275
Correct operation validated. See README.md for run and reporting rules.
```

退出ruyi LLVM虚拟环境

```bash
cd ..; ruyi-deactivate
```
