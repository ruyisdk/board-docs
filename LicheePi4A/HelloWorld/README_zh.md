---
sys: revyos
sys_ver: "20250930"
sys_var: null

status: basics
last_update: 2026-04-03
---

# RuyiSDK 基础示例

安装依赖包

```
sudo apt update; sudo apt install -y wget tar zstd xz-utils git build-essential
```

安装ruyi包管理器

```
wget https://mirror.iscas.ac.cn/ruyisdk/ruyi/tags/0.41.0/ruyi-0.41.0.riscv64

chmod +x ruyi-0.41.0.riscv64

sudo cp -v ruyi-0.41.0.riscv64 /usr/local/bin/ruyi
```

安装GCC和LLVM工具链

```
ruyi update

ruyi install gnu-plct llvm-plct
```

## Hello World (GCC版)

创建并激活ruyi虚拟环境（GCC）

```
ruyi venv -t toolchain/gnu-plct manual venv-gnu-plct
. ~/venv-gnu-plct/bin/ruyi-activate
```



验证GCC版本

```
riscv64-plct-linux-gnu-gcc -v
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
riscv64-plct-linux-gnu-gcc hello.c -o hello-gcc
./hello-gcc
```

正常情况下，终端会看到类似如下输出：

```
debian@revyos-lpi4a:~$ source venv-gnu-plat/bin/ruyi-activate
<an@revyos-lpi4a:~$ riscv64-plat-linux-gnu-gcc hello.c -o hello-gcc
《Ruyi venv-gnu-plat》 debian@revyos-lpi4a:~$ ./hello-gcc
Hello, World!
《Ruyi venv-gnu-plat》 debian@revyos-lpi4a:~$ 
```


退出ruyi GCC虚拟环境

```
cd ..; ruyi-deactivate
```



## Hello World (LLVM版)

创建并激活ruyi虚拟环境（LLVM）

```
ruyi venv -t toolchain/llvm-plct manual --sysroot-from gnu-plct venv-llvm-plct
. ~/venv-llvm-plct/bin/ruyi-activate
```



验证LLVM版本

```
clang -v
```



编译并运行Hello World（LLVM）

```
clang hello.c -o hello-llvm; ./hello-llvm
```

正常情况下，终端会看到类似如下输出：

```
debian@revos:/home$ source venv-llvm-plct/bin/rui activate
《Rui venv-llvm-plct》 debian@revos:/home$ clang hello.c -o hello-llvm
《Rui venv-llvm-plct》 debian@revos:/home$ ./hello-llvm
Hello, World!
《Rui venv-llvm-plct》 debian@revos:/home$
```




退出ruyi GCC虚拟环境

```
cd ..; ruyi-deactivate
```


