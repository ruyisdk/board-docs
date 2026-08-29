---
sys: Ubuntu 20.04.4 LTS in Docker
sys_ver: v1.9
sys_var: null

category: benchmark
last_update: 2026-06-14

model: Canaan K510-CRB-V1.2 KIT
profile: Coremark

---

# RuyiSDK Performance Test Example

This example uses the RuyiSDK GCC and LLVM toolchains on a PC to cross-compile Coremark, then transfers the binaries to the development board for execution.

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

## Coremark (GCC)

Create and activate a ruyi virtual environment (GCC)

```bash
ruyi venv -t gnu-ruyisdk generic gcc-env
. gcc-env/bin/ruyi-activate
```

Verify the GCC version

```bash
riscv64-ruyisdk-linux-gnu-gcc -v
```

Compile Coremark (GCC)

```bash
git clone https://github.com/eembc/coremark
cd coremark
make CC=riscv64-ruyisdk-linux-gnu-gcc XCFLAGS="-static -march=rv64imafd" compile
mv coremark.exe coremark-gcc
riscv64-ruyisdk-linux-gnu-objcopy --remove-section=.riscv.attributes coremark-gcc coremark-gcc
```

Transfer the file from the PC

```bash
python3 -m http.server 8000
```

Run the following commands in the development board's `minicom` terminal:

```bash
wget http://10.13.61.37:8000/coremark-gcc -O /root/coremark-gcc
chmod +x /root/coremark-gcc
/root/coremark-gcc
```

Output

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

Exit the ruyi GCC virtual environment

```bash
cd ..; ruyi-deactivate
```

## Coremark (LLVM)

Create and activate a ruyi virtual environment (LLVM)

```bash
ruyi venv -t llvm-ruyisdk generic --sysroot-from gnu-ruyisdk llvm-env
. llvm-env/bin/ruyi-activate
```

Verify the LLVM version

```bash
clang -v
```

Compile Coremark (LLVM)

```bash
cd coremark
make clean
make CC=clang XCFLAGS="-static --target=riscv64-linux-gnu -march=rv64imafdc -Iposix" compile
mv coremark.exe coremark-llvm
```

Strip the attributes section

```bash
OBJCOPY=~/tes/k510_buildroot/k510_crb_lp3_v1_2_defconfig/host/bin/riscv64-buildroot-linux-gnu-objcopy
if [ ! -f "$OBJCOPY" ]; then
    OBJCOPY=/opt/riscv64-lp64d--glibc--stable-2025.08-1/bin/riscv64-linux-objcopy
fi

$OBJCOPY --remove-section=.riscv.attributes coremark-llvm coremark_llvm
```

Transfer the file from the PC

```bash
python3 -m http.server 8000
```

Run the following commands in the development board's `minicom` terminal:

```bash
wget http://10.13.61.37:8000/coremark_llvm -O /root/coremark_llvm
chmod +x /root/coremark_llvm
/root/coremark_llvm
```

Output

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

Exit the ruyi LLVM virtual environment

```bash
cd ..; ruyi-deactivate
```
