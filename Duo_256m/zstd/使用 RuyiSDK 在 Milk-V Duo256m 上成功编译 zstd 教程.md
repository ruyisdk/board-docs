# 使用 RuyiSDK 在 Milk-V Duo256m 上成功编译 zstd 教程

本教程以在Milk-V Duo256m上编译运行官方原生zstd项目为例，基于仓库核心文件验证RuyiSDK对RISC-V架构的编译适配性，以及开发板在zstd压缩/解压缩场景下的基础算力与功能正确性。

## 1.准备工作

### 下载系统镜像

```Plain Text
https://github.com/milkv-duo/duo-buildroot-sdk-v2/releases/download/v2.0.1/milkv-duo256m-musl-riscv64-sd_v2.0.1.img.zip
```

### 解压系统镜像

```Plain Text
unzip milkv-duo256m-musl-riscv64-sd_v2.0.1.img.zip
```

### 系统镜像烧录进存储卡

```Plain Text
sudo dd if=milkv-duo256m-musl-riscv64-sd_v2.0.1.img of=/dev/sdX bs=1M; sync
```

<img width="995" height="610" alt="image" src="https://github.com/user-attachments/assets/32a83ae4-dd5b-40e7-953e-8fae7a9e04d0" />


### 安装依赖包

```Plain Text
sudo apt update; sudo apt install -y wget tar zstd xz-utils git build-essential
```

### 安装ruyi包管理器

```Plain Text
wget https://mirror.iscas.ac.cn/ruyisdk/ruyi/tags/0.45.0/ruyi-0.45.0.amd64
chmod +x ruyi-0.45.0.amd64
sudo cp -v ruyi-0.45.0.amd64 /usr/local/bin/ruyi
```
<img width="1462" height="619" alt="image" src="https://github.com/user-attachments/assets/e0e38d7c-2e2e-475e-bf97-80bfec29a533" />

### 安装GCC工具链

```Plain Text
ruyi update
ruyi install gnu-plct 
```
<img width="1432" height="933" alt="image" src="https://github.com/user-attachments/assets/0ebebe4f-fad4-4177-8825-ce82890c1431" />
## 2.获取 zstd 源码并编译（基于官方原生文件）

### 创建并激活ruyi虚拟环境（GCC）

```Plain Text
ruyi venv -t toolchain/gnu-plct milkv-duo venv-zstd
. ~/venv-zstd/bin/ruyi-activate
```
<img width="971" height="419" alt="image" src="https://github.com/user-attachments/assets/f0bba235-dc03-4f70-b7a2-31a2f3b5570c" />

### 验证GCC版本

```Plain Text
riscv64-plct-linux-gnu-gcc -v
```
<img width="1068" height="629" alt="image" src="https://github.com/user-attachments/assets/e0328416-28a1-4ea6-876c-520fd586c5f9" />

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
<img width="1153" height="622" alt="image" src="https://github.com/user-attachments/assets/ba5c75b9-2a53-4df2-bddf-0894e0d35ac8" />

<img width="1461" height="622" alt="image" src="https://github.com/user-attachments/assets/f0310835-0980-416a-a06d-1d15c642c77d" />

<img width="1417" height="624" alt="image" src="https://github.com/user-attachments/assets/12508a51-74eb-41a9-bc18-d3df030591cd" />

<img width="968" height="478" alt="image" src="https://github.com/user-attachments/assets/9bbb4b54-8564-4d6c-ab6b-8b17634768ed" />

## 3.将二进制文件传输至开发板并运行验证

### 将编译好的二进制传输至开发板

```Plain Text
scp programs/zstd root@192.168.42.1:~
```

### SSH连接到开发板

```Plain Text
ssh root@192.168.42.1
```
<img width="974" height="142" alt="image" src="https://github.com/user-attachments/assets/65d43c31-e5c1-476c-a967-32092b044d51" />

### 运行基础功能验证

#### 1. 查看zstd版本

```Plain Text
# 给程序开运行权限
chmod +x zstd

./zstd --version
```

执行后应输出zstd版本信息，确认程序可正常运行。

#### 2. 压缩/解压缩测试

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
<img width="1058" height="163" alt="image" src="https://github.com/user-attachments/assets/531bf269-1046-4b45-a09a-e21b00fd8a4b" />

### 
