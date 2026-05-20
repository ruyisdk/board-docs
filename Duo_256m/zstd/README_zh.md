---
sys: buildroot
sys_ver: v1.1.4
sys_var: v1

status: Compression
last_update: 2026-05-03

model: Milk-V Duo (256M)
profile: zstd
---

# RuyiSDK 压缩示例

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
## zstd

本教程以在 Milk-V Duo256m 上编译运行官方原生 zstd 项目为例，基于仓库核心文件验证 RuyiSDK 对 RISC-V 架构的编译适配性，以及开发板在 zstd 压缩/解压缩场景下的基础算力与功能正确性。

### 1. 准备工作

* **开发板**：Milk-V Duo 256M (256M, SG2002)

* **其他**：microSD 卡、USB Type-C 数据线

#### 操作系统安装与启动验证

确保您的开发板已准备好系统。

参考文档： https://milkv.io/zh/docs/duo/getting-started/boot

### 2. 获取源码并编译

### 创建并激活ruyi虚拟环境（GCC）

```Plain Text
ruyi venv -t toolchain/gnu-plct milkv-duo venv-zstd
. ~/venv-zstd/bin/ruyi-activate
```

### 验证GCC版本

```Plain Text
riscv64-plct-linux-gnu-gcc -v
```

执行后应显示RISC-V架构的GCC工具链版本信息，确认工具链安装成功且激活生效。

### 克隆 zstd 项目源码

```Plain Text
git clone https://github.com/facebook/zstd.git
cd zstd
```

### 编译官方原生可执行程序（基础功能验证）

zstd 项目采用Makefile构建，需指定RISC-V交叉编译工具链：

```Plain Text
make -C lib CC=riscv64-plct-linux-gnu-gcc
make -C programs CC=riscv64-plct-linux-gnu-gcc LDFLAGS="-static"
```


### 3.将二进制文件传输至开发板并运行验证

#### 将编译好的二进制传输至开发板

```Plain Text
scp programs/zstd root@192.168.42.1:~
```

#### SSH连接到开发板

```Plain Text
ssh root@192.168.42.1
```

#### 运行基础功能验证

1. 查看zstd版本

```Plain Text
# 给程序开运行权限
chmod +x zstd

./zstd --version
```

执行后应输出zstd版本信息，确认程序可正常运行。

2. 压缩/解压缩测试

```Plain Text
# 创建测试文件
echo "Test zstd on Milk-V Duo256m" > test.txt

# 压缩文件
./zstd test.txt -o test.txt.zst

# 解压缩文件
./zstd -d test.txt.zst -o test_uncompressed.txt

# 验证内容一致性
cat test_uncompressed.txt

```
