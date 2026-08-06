---
sys: Ubuntu 20.04.4 LTS in Docker
sys_ver: v1.9
sys_var: null

category: benchmark
last_update: 2026-06-14

model: Canaan K510-CRB-V1.2 KIT
profile: Coremark

---

# RuyiSDK 性能测试示例

可直接在开发板上进行编译和运行的示例，适合初学者快速上手。

安装ruyi包管理器

```bash
sudo apt update; sudo apt install wget

wget https://mirror.iscas.ac.cn/ruyisdk/ruyi/tags/0.49.0/ruyi-0.49.0.riscv64
chmod +x ./ruyi-0.49.0.riscv64
sudo cp -v ./ruyi-0.49.0.riscv64 /usr/local/bin/ruyi
```

安装GCC和LLVM工具链

```bash
ruyi update
ruyi install gnu-plct llvm-plct
```

## Coremark (GCC版)

创建并激活ruyi虚拟环境（GCC）

```bash
ruyi venv --toolchain gnu-plct generic gcc-env
. gcc-env/bin/ruyi-activate
```

验证GCC版本

```bash
riscv64-plct-linux-gnu-gcc -v
```

编译Coremark（GCC）

```bash
git clone https://github.com/eembc/coremark
cd coremark

make CC=riscv64-linux-gcc XCFLAGS="-static -march=rv64imafdc" compile
mv coremark.exe coremark_gcc
```

PC端传输

```bash
python3 -m http.server 8000
```

在开发板的`minicom`终端里运行：

```bash
wget http://10.13.61.37:8000/coremark_gcc -O /root/coremark_
gcc
chmod +x /root/coremark_gcc
/root/coremark_gcc
```

输出结果

```bash
[root@canaan ~ ]$ wget http://10.13.61.37:8000/coremark_gcc -O /root/coremark_
gcc                                                                             
Connecting to 10.13.61.37:8000 (10.13.61.37:8000)                               
saving to '/root/coremark_gcc'                                                  
coremark_gcc         100% |********************************| 4202k  0:00:00 ETA 
'/root/coremark_gcc' saved                                                      
[root@canaan ~ ]$ chmod +x /root/coremark_gcc
[root@canaan ~ ]$ /root/coremark_gcc
2K performance run parameters for coremark.                                     
CoreMark Size    : 666                                                          
Total ticks      : 17932                                                        
Total time (secs): 17.932000                                                    
Iterations/Sec   : 1672.986839                                                  
Iterations       : 30000                                                        
Compiler version : GCC7.3.0                                                     
Compiler flags   : -O2 -static -march=rv64imafdc  -lrt                          
Memory location  : Please put data memory location here                         
                        (e.g. code in flash, data on heap etc)                  
seedcrc          : 0xe9f5                                                       
[0]crclist       : 0xe714                                                       
[0]crcmatrix     : 0x1fd7                                                       
[0]crcstate      : 0x8e3a                                                       
[0]crcfinal      : 0x5275                                                       
Correct operation validated. See README.md for run and reporting rules.         
CoreMark 1.0 : 1672.986839 / GCC7.3.0 -O2 -static -march=rv64imafdc  -lrt / Heap
[root@canaan ~ ]$ 
```

退出ruyi GCC虚拟环境

```
cd ..; ruyi-deactivate
```

## Coremark (LLVM版)

创建并激活ruyi虚拟环境（LLVM）

```bash
ruyi venv -t toolchain/llvm-plct --sysroot-from gnu-plct generic llvm-env
. llvm-env/bin/ruyi-activate
```

验证LLVM版本

```
clang-14 -v
```

编译Coremark（LLVM）

```bash
git clone https://github.com/eembc/coremark.git
cd coremark

make CC=clang-14 XCFLAGS="-static --target=riscv64-linux-gnu -march=rv64imafdc -mabi=lp64d -Iposix" compile
mv coremark.exe coremark_k510
```

剥离属性段

```bash
OBJCOPY=~/tes/k510_buildroot/k510_crb_lp3_v1_2_defconfig/host/bin/riscv64-buildroot-linux-gnu-objcopy
if [ ! -f "$OBJCOPY" ]; then
    OBJCOPY=/opt/riscv64-lp64d--glibc--stable-2025.08-1/bin/riscv64-linux-objcopy
fi
$OBJCOPY --remove-section=.riscv.attributes coremark_k510 coremark_k510_stripped
```

PC端传输

```bash
python3 -m http.server 8000
```

在开发板的`minicom`终端里运行：

```bash
wget http://10.13.61.37:8000/coremark_k510_stripped -O /root/coremark_k510_stripped
chmod +x /root/coremark_k510_stripped
/root/coremark_k510_stripped
```

输出结果

```bash
[root@canaan ~ ]$ wget http://10.13.61.37:8000/coremark_k510_stripped -O /root/c
oremark_k510_stripped                                                           
Connecting to 10.13.61.37:8000 (10.13.61.37:8000)                               
saving to '/root/coremark_k510_stripped'                                        
coremark_k510_stripp 100% |********************************|  561k  0:00:00 ETA 
'/root/coremark_k510_stripped' saved                                            
[root@canaan ~ ]$ chmod +x /root/coremark_k510_stripped                         
[root@canaan ~ ]$ /root/coremark_k510_stripped                                  
2K performance run parameters for coremark.                                     
CoreMark Size    : 666                                                          
Total ticks      : 14388                                                        
Total time (secs): 14.388000                                                    
Iterations/Sec   : 1390.047262                                                  
Iterations       : 20000                                                        
Compiler version : Ubuntu Clang 14.0.6                                          
Compiler flags   : -O2 -static --target=riscv64-linux-gnu -march=rv64imafdc -mat
Memory location  : Please put data memory location here                         
                        (e.g. code in flash, data on heap etc)                  
seedcrc          : 0xe9f5                                                       
[0]crclist       : 0xe714                                                       
[0]crcmatrix     : 0x1fd7                                                       
[0]crcstate      : 0x8e3a                                                       
[0]crcfinal      : 0x382f                                                       
Correct operation validated. See README.md for run and reporting rules.         
CoreMark 1.0 : 1390.047262 / Ubuntu Clang 14.0.6 -O2 -static --target=riscv64-lp
[root@canaan ~ ]$ 
```

退出ruyi GCC虚拟环境

```bash
cd ..; ruyi-deactivate
```

