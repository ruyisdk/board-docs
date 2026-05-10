# 使用RuyiSDK 编译 Milk-V Duo256m 示例程序教程

本教程以在Milk-v Duo256m上运行2048游戏为例，验证RuyiSDK的终端 IO、ANSI 转义码、单文件编译等功能



## 1.准备工作

### 下载系统镜像

```
https://github.com/milkv-duo/duo-buildroot-sdk-v2/releases/download/v2.0.1/milkv-duo256m-musl-riscv64-sd_v2.0.1.img.zip
```



### 解压系统镜像

```
unzip milkv-duo256m-musl-riscv64-sd_v2.0.1.img.zip
```



### 系统镜像烧录进存储卡

```
sudo dd if=milkv-duo256m-musl-riscv64-sd_v2.0.1.img of=/dev/sdX bs=1M; sync
```
<img width="995" height="610" alt="image" src="https://github.com/user-attachments/assets/12465727-3f4d-4df0-abc3-ad10ad13301a" />



### 安装依赖包

```
sudo apt update; sudo apt install -y wget tar zstd xz-utils git build-essential
```



### 安装ruyi包管理器

```
wget https://mirror.iscas.ac.cn/ruyisdk/ruyi/tags/0.45.0/ruyi-0.45.0.amd64
chmod +x ruyi-0.45.0.amd64
sudo cp -v ruyi-0.45.0.amd64 /usr/local/bin/ruyi
```
<img width="1462" height="619" alt="image" src="https://github.com/user-attachments/assets/0796fb33-8ea9-48f9-b986-5c0001140db4" />



### 安装GCC工具链

```
ruyi update
ruyi install gnu-plct 
```
<img width="1432" height="933" alt="image" src="https://github.com/user-attachments/assets/45ced5f7-f163-4fe0-ab6e-f8270421cc6b" />



## 2.在GCC虚拟环境中编译2048.c

### 创建并激活ruyi虚拟环境（GCC)

```
ruyi venv -t toolchain/gnu-plct milkv-duo venv-2048
. ~/venv-2048/bin/ruyi-activate
```

<img width="1426" height="103" alt="image" src="https://github.com/user-attachments/assets/cfce1d26-aaa6-4fa4-b03c-587031d7579e" />


### 验证GCC版本

```
riscv64-plct-linux-gnu-gcc -v
```



### 获取2048的源码

```
wget https://raw.githubusercontent.com/mevdschee/2048.c/master/2048.c
```
<img width="1442" height="284" alt="image" src="https://github.com/user-attachments/assets/02adbe5d-85d7-43c7-b96e-e11736975aca" />



### 编译2048.c

```
riscv64-plct-linux-gnu-gcc 2048.c -static -o 2048-gcc
```
<img width="1272" height="93" alt="image" src="https://github.com/user-attachments/assets/44f7a4d4-feaf-4e9a-a6ed-03b546da8efc" />



### 将GCC构建的二进制传输至开发板

```
scp 2048 root@192.168.42.1:~
```

 

### SSH连接到开发板并执行编译好的二进制

```
ssh root@192.168.42.1
```
<img width="1461" height="553" alt="image" src="https://github.com/user-attachments/assets/e64f5c4c-bfd3-40b9-b8ae-cfc86efdeb94" />



### 运行2048

```
./2048-gcc
```
<img width="616" height="529" alt="image" src="https://github.com/user-attachments/assets/a6c097cd-ca2a-4fe3-ab4f-147f30be3d60" />
