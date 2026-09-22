---
sys: fedora
sys_ver: "44"
sys_var: null

category: getting-started
last_update: 2026-09-17

model: Premier P550
profile: Hello World
---

# RuyiSDK 入门示例

本示例可直接在开发板上编译并运行，适合初学者快速上手。

安装依赖包

```bash
sudo dnf install -y git make wget tar zstd xz
```

安装 ruyi 包管理器（其他安装方式见[官方安装文档](https://ruyisdk.org/docs/Package-Manager/installation)）

```bash
wget https://mirror.iscas.ac.cn/ruyisdk/ruyi/tags/0.52.0/ruyi-0.52.0.riscv64
chmod +x ./ruyi-0.52.0.riscv64
sudo cp -v ./ruyi-0.52.0.riscv64 /usr/local/bin/ruyi
```

安装 GCC 和 LLVM 工具链

```bash
ruyi update

ruyi install gnu-ruyisdk llvm-ruyisdk
```

## Hello World（GCC 版）

创建并激活 ruyi 虚拟环境（GCC）

```bash
ruyi venv -t toolchain/gnu-ruyisdk manual venv-gnu-ruyisdk
. venv-gnu-ruyisdk/bin/ruyi-activate
```

验证 GCC 版本

```bash
riscv64-ruyisdk-linux-gnu-gcc -v
```

编译并运行 Hello World（GCC）

```bash
cat > hello.c << 'EOF'
#include <stdio.h>

int main(void)
{
    printf("Hello, World!\n");
    return 0;
}
EOF

riscv64-ruyisdk-linux-gnu-gcc hello.c -o hello-gcc
./hello-gcc
```

正常情况下，终端会看到类似如下输出：

```text
«Ruyi venv-gnu-ruyisdk» [fedora@localhost ~]$ riscv64-ruyisdk-linux-gnu-gcc hello.c -o hello-gcc
«Ruyi venv-gnu-ruyisdk» [fedora@localhost ~]$ ./hello-gcc
Hello, World!
«Ruyi venv-gnu-ruyisdk» [fedora@localhost ~]$
```

退出 ruyi GCC 虚拟环境

```bash
ruyi-deactivate
```

## Hello World（LLVM 版）

创建并激活 ruyi 虚拟环境（LLVM）

```bash
ruyi venv -t llvm-ruyisdk manual --sysroot-from gnu-ruyisdk venv-llvm-ruyisdk
. venv-llvm-ruyisdk/bin/ruyi-activate
```

验证 LLVM 版本

```bash
clang -v
```

编译并运行 Hello World（LLVM）

```bash
clang hello.c -o hello-llvm
./hello-llvm
```

正常情况下，终端会看到类似如下输出：

```text
«Ruyi venv-llvm-ruyisdk» [fedora@localhost ~]$ clang hello.c -o hello-llvm
«Ruyi venv-llvm-ruyisdk» [fedora@localhost ~]$ ./hello-llvm
Hello, World!
«Ruyi venv-llvm-ruyisdk» [fedora@localhost ~]$
```

退出 ruyi LLVM 虚拟环境

```bash
cd ..
ruyi-deactivate
```
