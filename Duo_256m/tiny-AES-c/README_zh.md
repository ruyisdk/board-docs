---
sys: buildroot
sys_ver: v1.1.4
sys_var: v1

status: Crypto
last_update: 2026-05-03

model: Milk-V Duo (256M)
profile: tiny-AES-c
---

# RuyiSDK 加密示例

安装依赖包

```

sudo apt update; sudo apt install -y wget tar zstd xz-utils git build-essential

```
安装 ruyi 包管理器

```
wget https://mirror.iscas.ac.cn/ruyisdk/ruyi/tags/0.45.0/ruyi-0.45.0.amd64

chmod +x ruyi-0.45.0.amd64

sudo cp -v ruyi-0.45.0.amd64 /usr/local/bin/ruyi

```

安装工具链

```

ruyi update

ruyi install gnu-plct llvm-plct

```
## tiny-AES-c
本教程以在Milk-V Duo256m上编译运行官方原生tiny-AES-c项目为例，基于仓库自带核心文件验证RuyiSDK对RISC-V架构的编译适配性，以及开发板在AES加解密场景下的基础算力与逻辑运算正确性。

### 1. 准备工作

* **开发板**：Milk-V Duo 256M (256M, SG2002)

* **其他**：microSD 卡、USB Type-C 数据线

#### 操作系统安装与启动验证

确保您的开发板已准备好系统。

参考文档： https://milkv.io/zh/docs/duo/getting-started/boot



### 2.获取 tiny-AES-c 源码并编译（基于官方原生文件）

#### 创建并激活ruyi虚拟环境（GCC）

```Plain Text
ruyi venv -t toolchain/gnu-plct milkv-duo venv-aes
. ~/venv-aes/bin/ruyi-activate
```

#### 验证GCC版本

```Plain Text
riscv64-plct-linux-gnu-gcc -v
```


#### 克隆 tiny-AES-c 项目源码

```Plain Text
git clone https://github.com/kokke/tiny-AES-c.git
cd tiny-AES-c
```

#### 编译官方原生测试程序（验证逻辑运算）

```Plain Text
riscv64-plct-linux-gnu-gcc aes.c test.c -static -o aes-official-test -O2 -lm
```

编译算力测试程序：

```Plain Text
riscv64-plct-linux-gnu-gcc aes.c aes_official_test.c -static -o aes-perf-test -O2 -lm
```

### 3.将二进制文件传输至开发板并运行验证

#### 将编译好的二进制传输至开发板

```Plain Text
scp aes_official_test root@192.168.42.1:~
```

#### SSH连接到开发板

```Plain Text

ssh root@192.168.42.1
```


#### 运行官方逻辑验证程序

```Plain Text
./aes-official-test
```
