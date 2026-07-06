---
sys: ubuntu
sys_ver: 24.04
sys_var: 

status: basics
last_update: 2026-07-06

model: EBC7700
profile: Hello World
---

#  RuyiSDK 基础示例

安装依赖包

```bash
sudo apt update
sudo apt install -y wget tar zstd xz-utils git build-essential
```

安装ruyi包管理器

```bash
wget https://mirror.iscas.ac.cn/ruyisdk/ruyi/tags/0.47.0/ruyi.riscv64

chmod +x ruyi.riscv64

sudo cp -v ruyi.riscv64 /usr/local/bin/ruyi
```

安装GCC和LLVM工具链

```bash
ruyi update

ruyi install gnu-ruyisdk llvm-ruyisdk
```

## Hello World (GCC版) 

创建并激活ruyi虚拟环境（GCC）
```bash
ruyi venv -t toolchain/gnu-ruyisdk manual venv-gnu-ruyisdk

. venv-gnu-ruyisdk/bin/ruyi-activate
```

验证GCC版本

```bash
riscv64-ruyisdk-linux-gnu-gcc -v
```

编译Hello World（GCC）

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
运行生成的文件   

```bash
./hello-gcc
```

正常情况下，终端会看到类似如下输出：

```text
«Ruyi venv-gnu-ruyisdk» ubuntu@ubuntu:~$ ./hello-gcc
Hello, World!
«Ruyi venv-gnu-ruyisdk» ubuntu@ubuntu:~$
```
退出ruyi GCC虚拟环境

```bash
ruyi-deactivate
```

## Hello World (LLVM版) 
创建并激活ruyi虚拟环境（LLVM）

```bash
ruyi venv -t toolchain/llvm-ruyisdk manual --sysroot-from gnu-ruyisdk venv-llvm-ruyisdk

. venv-llvm-ruyisdk/bin/ruyi-activate
```
验证LLVM版本

```bash
clang -v
```

编译 Hello World（LLVM）

```bash
clang hello.c -o hello-llvm
```

运行生成的文件：   
```bash
./hello-llvm
```

正常情况下，终端会看到类似如下输出：

```text
«Ruyi venv-llvm-ruyisdk» ubuntu@ubuntu:~$ ./hello-llvm
Hello, World!
«Ruyi venv-llvm-ruyisdk» ubuntu@ubuntu:~$
```
退出ruyi LLVM虚拟环境

```bash
ruyi-deactivate
```
