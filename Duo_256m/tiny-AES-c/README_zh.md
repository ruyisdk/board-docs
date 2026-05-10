# 使用 RuyiSDK 在 Milk-V Duo256m 上编译 tiny-AES-c 教程

本教程以在Milk-V Duo256m上编译运行官方原生tiny-AES-c项目为例，基于仓库自带核心文件验证RuyiSDK对RISC-V架构的编译适配性，以及开发板在AES加解密场景下的基础算力与逻辑运算正确性。

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
<img width="995" height="610" alt="image" src="https://github.com/user-attachments/assets/e2cf9798-190e-4715-a04a-95272761db92" />

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
<img width="1462" height="619" alt="image" src="https://github.com/user-attachments/assets/dfd42664-e5d7-4096-b639-1ba84637546f" />

### 安装GCC工具链

```Plain Text
ruyi update
ruyi install gnu-plct 
```
<img width="1432" height="933" alt="image" src="https://github.com/user-attachments/assets/0ebebe4f-fad4-4177-8825-ce82890c1431" />

## 2.获取 tiny-AES-c 源码并编译（基于官方原生文件）

### 创建并激活ruyi虚拟环境（GCC）

```Plain Text
ruyi venv -t toolchain/gnu-plct milkv-duo venv-aes
. ~/venv-aes/bin/ruyi-activate
```
<img width="961" height="446" alt="image" src="https://github.com/user-attachments/assets/d4dc376f-c968-4f5d-9ef4-bd67b92fb98a" />

### 验证GCC版本

```Plain Text
riscv64-plct-linux-gnu-gcc -v
```
<img width="951" height="650" alt="image" src="https://github.com/user-attachments/assets/c979b384-6703-4c6c-a2e8-fb52d584cd5e" />


### 克隆 tiny-AES-c 项目源码

```Plain Text
git clone https://github.com/kokke/tiny-AES-c.git
cd tiny-AES-c
```
<img width="933" height="256" alt="image" src="https://github.com/user-attachments/assets/b42d10b5-f73d-4cf4-aa60-a9912084c2b6" />

### 编译官方原生测试程序（验证逻辑运算）

```Plain Text
riscv64-plct-linux-gnu-gcc aes.c test.c -static -o aes-official-test -O2 -lm
```

编译算力测试程序：

```Plain Text
riscv64-plct-linux-gnu-gcc aes.c aes_official_test.c -static -o aes-perf-test -O2 -lm
```
<img width="953" height="262" alt="image" src="https://github.com/user-attachments/assets/60c60807-46cd-484a-a66f-eba67cd5d5ce" />

## 3.将二进制文件传输至开发板并运行验证

### 将编译好的二进制传输至开发板

```Plain Text
scp aes_official_test root@192.168.42.1:~
```

### SSH连接到开发板

```Plain Text

ssh root@192.168.42.1
```
<img width="966" height="703" alt="image" src="https://github.com/user-attachments/assets/21953143-4a20-49f9-b773-5e73ca02b895" />


### 运行官方逻辑验证程序

```Plain Text
./aes-official-test
```
