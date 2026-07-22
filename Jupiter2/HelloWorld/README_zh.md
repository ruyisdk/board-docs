---
sys: Bianbu
sys_ver: 4.0.1
sys_var: null

status: basics
last_update: 2026-07-22

model: 	Milk-V Jupiter2
profile: Hello World
---

#  RuyiSDK 基础示例
安装依赖包

```
sudo apt update; sudo apt install -y wget tar zstd xz-utils git build-essential
```

安装ruyi包管理器

```
wget https://mirror.iscas.ac.cn/ruyisdk/ruyi/tags/0.51.0/ruyi-0.51.0.riscv64

chmod +x ./ruyi-0.51.0.riscv64

sudo cp -v ./ruyi-0.51.0.riscv64 /usr/local/bin/ruyi
```

安装GCC和LLVM工具链

```
ruyi update

ruyi install gnu-ruyisdk llvm-ruyisdk
```

## Hello World (GCC版)

创建并激活ruyi虚拟环境（GCC）
```
ruyi venv -t gnu-ruyisdk manual venv-gnu-ruyisdk-jupiter2

. venv-gnu-ruyisdk-jupiter2/bin/ruyi-activate
```

验证GCC版本

```
riscv64-ruyisdk-linux-gnu-gcc -v
```

编译并运行Hello World（GCC）

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


正常情况下，终端会看到类似如下输出：

```
«Ruyi venv-gnu-ruyisdk-jupiter2» jupiter2@k3:~$ ./hello-gcc
Hello, World!
«Ruyi venv-gnu-ruyisdk-jupiter2» jupiter2@k3:~$
```

退出ruyi GCC虚拟环境

```
ruyi-deactivate
```

## Hello World (LLVM版)
创建并激活ruyi虚拟环境（LLVM）

```
ruyi venv -t llvm-ruyisdk manual --sysroot-from gnu-ruyisdk venv-llvm-ruyisdk-jupiter2

. venv-llvm-ruyisdk-jupiter2/bin/ruyi-activate
```
验证LLVM版本

```
clang -v
```

编译并运行 Hello World（LLVM）

```
clang hello.c -o hello-llvm; ./hello-llvm

```


正常情况下，终端会看到类似如下输出：

```
«Ruyi venv-llvm-ruyisdk-jupiter2» jupiter2@k3:~$ clang hello.c -o hello-llvm; ./hello-llvm
Hello, World!
«Ruyi venv-llvm-ruyisdk-jupiter2» jupiter2@k3:~$

```
退出ruyi LLVM虚拟环境

```
ruyi-deactivate
```
