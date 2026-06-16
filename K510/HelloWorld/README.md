---
sys: Ubuntu 20.04.4 LTS in Docker
sys_ver: v1.9
sys_var: null

status: basics
last_update: 2026-06-14

model: Canaan K510 CRB-V1.2 KIT
profile: Hello World

---

# RuyiSDK 基础示例

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

## Hello World (GCC版)

创建并激活ruyi虚拟环境（GCC）

```bash
ruyi venv --toolchain gnu-plct generic gcc-env
. gcc-env/bin/ruyi-activate
```

验证GCC版本

```bash
riscv64-plct-linux-gnu-gcc -v
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

riscv64-linux-gcc -static hello.c -o hello-gcc
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

退出ruyi GCC虚拟环境

```
cd ..; ruyi-deactivate
```

## Hello World (LLVM版)

创建并激活ruyi虚拟环境（LLVM）

```bash
ruyi venv -t toolchain/llvm-plct --sysroot-from gnu-plct generic llvm-env
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
clang-14 -static --target=riscv64-linux-gnu hello_k510.c -o hello_k510
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

退出ruyi GCC虚拟环境

```bash
cd ..; ruyi-deactivate
```
