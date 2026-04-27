---
sys: ubuntu
sys_ver: "24.04"
sys_var: null

status: basics
last_update: 2026-04-27

model: VisionFive2 Lite
profile: Coremark

---

# RuyiSDK 基础示例

可直接在开发板上进行编译和运行的示例，适合初学者快速上手。

安装ruyi包管理器

```
sudo apt update; sudo apt install -y wget tar zstd xz-utils git build-essential

wget https://mirror.iscas.ac.cn/ruyisdk/ruyi/tags/0.47.0/ruyi-0.47.0.riscv64
chmod +x ./ruyi-0.47.0.riscv64
sudo cp -v ./ruyi-0.47.0.riscv64 /usr/local/bin/ruyi
```

安装GCC和LLVM工具链

```
ruyi update
ruyi install gnu-plct llvm-plct
```

## Coremark (GCC版)

创建并激活ruyi虚拟环境（GCC）

```
ruyi venv -t toolchain/gnu-plct manual venv-gnu-plct
. venv-gnu-plct/bin/ruyi-activate
```

验证GCC版本

```
riscv64-plct-linux-gnu-gcc -v
```

编译并运行Coremark（GCC）

```
git clone https://github.com/eembc/coremark
cd coremark
make CC=riscv64-plct-linux-gnu-gcc XCFLAGS="-march=rv64gc_zba_zbb" compile

./coremark.exe
```

正常情况下，终端会看到类似如下输出：

```
«Ruyi venv-gnu-plct» user@starfive:~/hello/coremark$ ./coremark.exe
2K performance run parameters for coremark.
CoreMark Size    : 666
Total ticks      : 11120
Total time (secs): 11.120000
Iterations/Sec   : 2697.841727
Iterations       : 30000
Compiler version : GCC15.1.0 20250912 (experimental)
Compiler flags   : -O2 -march=rv64gc_zba_zbb  -lrt
Memory location  : Please put data memory location here
                        (e.g. code in flash, data on heap etc)
seedcrc          : 0xe9f5
[0]crclist       : 0xe714
[0]crcmatrix     : 0x1fd7
[0]crcstate      : 0x8e3a
[0]crcfinal      : 0x5275
Correct operation validated. See README.md for run and reporting rules.
CoreMark 1.0 : 2697.841727 / GCC15.1.0 20250912 (experimental) -O2 -march=rv64gc_zba_zbb  -lrt / Heap
«Ruyi venv-gnu-plct» user@starfive:~/hello/coremark$
```


退出ruyi GCC虚拟环境

```
cd ..; ruyi-deactivate
```

## Coremark (LLVM版)

创建并激活ruyi虚拟环境（LLVM）

```
ruyi venv -t toolchain/llvm-plct manual --sysroot-from gnu-plct venv-llvm-plct
. venv-llvm-plct/bin/ruyi-activate
```

验证LLVM版本

```
clang -v
```

编译并运行Coremark（LLVM）

```
cd coremark; make clean; make CC=clang XCFLAGS="-march=rv64gc_zba_zbb" compile

./coremark.exe
```

正常情况下，终端会看到类似如下输出：

```
«Ruyi venv-llvm-plct» user@starfive:~/hello/coremark$ ./coremark.exe
2K performance run parameters for coremark.
CoreMark Size    : 666
Total ticks      : 13100
Total time (secs): 13.100000
Iterations/Sec   : 3053.435115
Iterations       : 40000
Compiler version : RuyiSDK Clang 21.1.0 (https://github.com/ruyisdk/llvm-project 3623fe661ae35c6c80ac221f14d85be76aa870f RuyiSDK 20250915)
Compiler flags   : -O2 -march=rv64gc_zba_zbb  -lrt
Memory location  : Please put data memory location here
                        (e.g. code in flash, data on heap etc)
seedcrc          : 0xe9f5
[0]crclist       : 0xe714
[0]crcmatrix     : 0x1fd7
[0]crcstate      : 0x8e3a
[0]crcfinal      : 0x25b5
Correct operation validated. See README.md for run and reporting rules.
CoreMark 1.0 : 3053.435115 / RuyiSDK Clang 21.1.0 (https://github.com/ruyisdk/llvm-project 3623fe661ae35c6c80ac221f14d85be76aa870f RuyiSDK 20250915) -O2 -march=rv64gc_zba_zbb  -lrt / Heap
«Ruyi venv-llvm-plct» user@starfive:~/hello/coremark$
```

退出ruyi GCC虚拟环境

```
cd ..; ruyi-deactivate
```

