# 使用 RuyiSDK 在 Milk-V Duo256m 上编译blink教程
### LED 闪烁的脚本禁用
```bash
ssh root@192.168.42.1
mv /mnt/system/blink.sh /mnt/system/blink.sh_backup && sync
```
<img width="1153" height="152" alt="image" src="https://github.com/user-attachments/assets/1a4fb58e-42a3-45ec-87ce-d87e2c1a3c25" />


### 搭建编译环境


**安装基础依赖**

```bash
sudo apt update
sudo apt install git build-essential gcc make libncurses5-dev flex bison libssl-dev rsync
```
<img width="1504" height="255" alt="image" src="https://github.com/user-attachments/assets/5f5247c5-2a07-41d3-a261-69ada805cae3" />

<img width="1503" height="790" alt="image" src="https://github.com/user-attachments/assets/be03092d-8b57-4af0-b6ef-05058cc97765" />

**下载 RISC-V 交叉编译工具链**
```bash
# 创建一个工作目录
mkdir -p ~/milkv
cd ~/milkv
<img width="1715" height="307" alt="image" src="https://github.com/user-attachments/assets/2bbfa243-7cc2-48e9-8a23-c4a6c855e0a7" />

# 下载官方预编译的工具链 (可能需要几分钟，取决于网速)
wget https://sophon-file.sophon.cn/sophon-prod-s3/drive/23/03/07/16/host-tools.tar.gz
<img width="901" height="423" alt="image" src="https://github.com/user-attachments/assets/763b2f40-28f7-4a48-9947-3c10a30b281d" />

# 解压
tar -xf host-tools.tar.gz
```

**获取官方 Blink 裸机示例代码**

```bash
git clone https://github.com/milkv-duo/duo-examples.git
cd duo-examples
```
<img width="1438" height="190" alt="image" src="https://github.com/user-attachments/assets/3d45577e-a442-402b-88ee-f21d13ee8420" />


**先运行环境配置脚本**

```bash
cd ~/milkv/duo-examples
source envsetup.sh
```
<img width="1495" height="553" alt="image" src="https://github.com/user-attachments/assets/6affe553-7f66-4ff2-b5d6-fe6b50a47346" />

这个脚本会帮你**自动拉取交叉编译工具链**（不用你手动 wget 了），并配置好环境变量。观察输出，等它跑完。

**进入 blink 目录编译**

```bash
cd blink
make
```
<img width="1905" height="165" alt="image" src="https://github.com/user-attachments/assets/2c590e55-baac-418b-beed-925ea01a206b" />

### 将二进制文件传输至开发板并运行验证

**将编译好的二进制传输至开发板**

```bash
scp blink root@192.168.42.1:~
```
<img width="1290" height="75" alt="image" src="https://github.com/user-attachments/assets/f34e28e8-7468-4d0d-997f-a84becb3321b" />

**SSH连接到开发板**

```bash
ssh root@192.168.42.1
```

**运行官方逻辑验证程序**

```bash
./blink
```
<img width="905" height="670" alt="image" src="https://github.com/user-attachments/assets/f06b5ced-bbdb-4b6d-ab15-550201f10306" />
