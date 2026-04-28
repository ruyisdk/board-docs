---
sys: revyos
sys_ver: "20250110"
sys_var: null

status: AI
last_update: 2026-04-27

model: Lichee Pi 4A
profile: YOLOv5n
---

# **RuyiSDK AI示例**
本示例暂未验证，只描述过程
## **安装依赖包**
### **安装docker**
```bash
sudo apt update
sudo apt install -y ca-certificates curl
```
```bash
# 下载 Docker 官方安装脚本并执行

curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```
安装成功后查看docker及其状态:
``bash
docker --version
sudo systemctl status docker
```

在终端显示如下：
```text
licheepi@licheepi-virtual-machine:~$ docker --version
Docker version 29.4.1, build 055a478
licheepi@licheepi-virtual-machine:~$ sudo systemctl status docker
● docker.service - Docker Application Container Engine
     Loaded: loaded (/lib/systemd/system/docker.service; enabled;>
     Active: active (running) since Fri 2026-04-24 13:35:46 CST; 
```
将当前用户加入 docker 组（免 sudo 运行）
```bash
sudo usermod -aG docker $USER
newgrp docker
```

拉取 HHB Docker 镜像
```bash
docker pull hhb4tools/hhb:latest
```
创建容器，名字为hhb_env  
```bash
docker run -itd --name hhb_env hhb4tools/hhb:latest
#进入容器
docker exec -it hhb_env /bin/bash
```

在终端显示如下：
```text
licheepi@licheepi-virtual-machine:~$ docker run -itd --name hhb_env hhb4tools/hhb:latest
78776422f7c978472da9c903bcba5804cae8c7f83f410a5b7fbd2989dbc2e877
licheepi@licheepi-virtual-machine:~$ docker exec -it hhb_env /bin/bash
root@78776422f7c9:/# 

```
下载Yolov5n模型    
下载到示例目录 /home/example/th1520_npu/yolov5n 下：  
```bash
mkdir -p /home/example/th1520_npu/yolov5n
cd /home/example/th1520_npu/yolov5n
git clone https://gitclone.com/github.com/ultralytics/yolov5.git
cd yolov5
pip3 install ultralytics
```
如果遇到版本冲突的问题，强制重装torch和torchvision
```bash
pip3 install --upgrade torch==2.4.1 torchvision==0.19.1
```
安装所需依赖
```bash
pip3 install pandas
pip3 install seaborn
```

```bash
python3 export.py --weights yolov5n.pt --include onnx --imgsz 384 640
# 将导出的 ONNX 文件复制到示例目录
cp yolov5n.onnx ../
```

HHB编译模型：  
将 ONNX 模型交叉编译成 NPU 上可执行的程序，需要使用 hhb 命令。  
编译时需要先进入到示例所在目录 /home/example/th1520_npu/yolov5n  
```bash
cd /home/example/th1520_npu/yolov5n
hhb -D --model-file yolov5n.onnx --data-scale-div 255 --board th1520 --input-name "images" --output-name "/model.24/m.0/Conv_output_0;/model.24/m.1/Conv_output_0;/model.24/m.2/Conv_output_0" --input-shape "1 3 384 640" --calibrate-dataset kite.jpg  --quantization-scheme "int8_asym"
```
在终端显示如下：
```text
root@78776422f7c9:/home/example/th1520_npu/yolov5n# hhb -D --model-file yolov5n.onnx --data-scale-div 255 --board th1520 --input-name "images" --output-name "/model.24/m.0/Conv_output_0;/model.24/m.1/Conv_output_0;/model.24/m.2/Conv_output_0" --input-shape "1 3 384 640" --calibrate-dataset kite.jpg  --quantization-scheme "int8_asym"
[2026-04-27 06:12:54] (HHB LOG): Start import model.
[2026-04-27 06:12:55] (HHB LOG): Model import completed! 
[2026-04-27 06:12:55] (HHB LOG): Start quantization.
[2026-04-27 06:12:55] (HHB LOG): get calibrate dataset from kite.jpg
[2026-04-27 06:12:55] (HHB LOG): Start optimization.
[2026-04-27 06:12:55] (HHB LOG): Optimization completed!
Calibrating: 100%|██████████████████| 316/316 [00:23<00:00, 13.21it/s]
[2026-04-27 06:13:19] (HHB LOG): Start conversion to csinn.
[2026-04-27 06:13:20] (HHB LOG): Conversion completed!
[2026-04-27 06:13:20] (HHB LOG): Start operator fusion.
[2026-04-27 06:13:20] (HHB LOG): Operator fusion completed!
[2026-04-27 06:13:21] (HHB LOG): Start operator split.
[2026-04-27 06:13:21] (HHB LOG): Operator split completed!
[2026-04-27 06:13:21] (HHB LOG): Start layout convert.
[2026-04-27 06:13:21] (HHB LOG): Layout convert completed!
[2026-04-27 06:13:21] (HHB LOG): Quantization completed!

```

### **安装 RuyiSDK**
```bash
# 下载并安装 ruyi
wget https://mirror.iscas.ac.cn/ruyisdk/ruyi/tags/0.47.0/ruyi-0.47.0.amd64
chmod +x ruyi-0.47.0.amd64
sudo cp ruyi-0.47.0.amd64 /usr/local/bin/ruyi
```
### **安装工具链**
```bash
ruyi update
ruyi install gnu-plct-xthead
```

会在终端看到如下输出：  
```text

info: skipping already installed package gnu-plct-xthead-3.1.0-ruyi.20250526

```
### **创建并激活 ruyi 虚拟环境**

```bash
# 创建虚拟环境 venv-sipeed
ruyi venv -t gnu-plct-xthead sipeed-lpi4a venv-sipeed 
#激活虚拟环境
. venv-sipeed/bin/ruyi-activate 
#查看当前虚拟环境下的 gcc 是否可用
riscv64-plctxthead-linux-gnu-gcc --version
```
在终端显示如下：
```text
licheepi@licheepi-virtual-machine:~$ . venv-sipeed/bin/ruyi-activate 
«Ruyi venv-sipeed» licheepi@licheepi-virtual-machine:~$ riscv64-plctxthead-linux-gnu-gcc --version 
riscv64-plctxthead-linux-gnu-gcc (RuyiSDK 20250526 Xuantie-Sources Xuantie-binutils-8ee62aac8606 Xuantie-gcc-c2e0bcc86d1f Xuantie-glibc-29dd660835c5) 14.1.1 20240710
Copyright (C) 2024 Free Software Foundation, Inc.
This is free software; see the source for copying conditions.  There is NO
warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

```

## **YOLOV5n**
### **示例描述和硬件环境准备**
示例描述：YOLOv5n 是轻量级目标检测模型，本示例在 Lichee Pi 4A 上运行 YOLOv5n，验证 RuyiSDK 工具链的 NPU 交叉编译能力。  
硬件环境：Lichee Pi 4A (16GB)   
软件环境：RuyiSDK 0.47.0，HHB 2.6.17

### **创建并激活 ruyi 虚拟环境**

创建虚拟环境 venv-sipeed  
```bash
ruyi venv -t gnu-plct-xthead sipeed-lpi4a venv-sipeed 
```
激活虚拟环境  
```bash
. venv-sipeed/bin/ruyi-activate 
```
终端显示如下：  
```bash
licheepi@licheepi-virtual-machine:~$ ruyi venv -t gnu-plct-xthead sipeed-lpi4a venv-sipeed 
info: Creating a Ruyi virtual environment at venv-sipeed...
info: The virtual environment is now created.

You may activate it by sourcing the appropriate activation script in the
bin directory, and deactivate by invoking `ruyi-deactivate`.

A fresh sysroot/prefix is also provisioned in the virtual environment.
It is available at the following path:

    /home/licheepi/venv-sipeed/sysroot

The virtual environment also comes with ready-made CMake toolchain file
and Meson cross file. Check the virtual environment root for those;
comments in the files contain usage instructions.

licheepi@licheepi-virtual-machine:~$ . venv-sipeed/bin/ruyi-activate 
«Ruyi venv-sipeed» licheepi@licheepi-virtual-machine:~$ 
```

### **使用 ruyi 工具链编译示例代码**
确认交叉编译器可用  
```bash
riscv64-plctxthead-linux-gnu-gcc --version
```

复制必要的文件到宿主机  
```bash
# 复制 hhb_out 目录（包含 io.c, model.c, process.c 等）
docker cp hhb_env:/home/example/th1520_npu/yolov5n/hhb_out ./

# 复制 NPU SDK（头文件和静态库）
docker cp hhb_env:/usr/local/lib/python3.8/dist-packages/hhb/install_nn2/th1520 ./th1520_npu_sdk

# 复制 c920 的静态库
docker cp hhb_env:/usr/local/lib/python3.8/dist-packages/hhb/install_nn2/c920/lib/. ./th1520_npu_sdk/lib/

# 复制主程序文件
docker cp hhb_env:/home/example/th1520_npu/yolov5n/yolov5n.c ./
```
交叉编译libjpeg  
```bash
cd /home/licheepi
git clone https://github.com/libjpeg-turbo/libjpeg-turbo.git
cd libjpeg-turbo
mkdir build && cd build

cmake .. \
    -DCMAKE_C_COMPILER=riscv64-plctxthead-linux-gnu-gcc \
    -DCMAKE_INSTALL_PREFIX=/home/licheepi/venv-sipeed/sysroot.riscv64-plctxthead-linux-gnu/usr \
    -DENABLE_SHARED=OFF \
    -DWITH_JPEG8=ON

make -j$(nproc)
make install
```
交叉编译zlib
```bash
cd /home/licheepi
wget https://github.com/madler/zlib/archive/refs/tags/v1.3.1.tar.gz -O zlib-1.3.1.tar.gz
tar -xzvf zlib-1.3.1.tar.gz
cd zlib-1.3.1

export CC=riscv64-plctxthead-linux-gnu-gcc
export AR=riscv64-plctxthead-linux-gnu-ar

./configure --prefix=/home/licheepi/venv-sipeed/sysroot.riscv64-plctxthead-linux-gnu/usr --static
make -j$(nproc)
make install
```
交叉编译 libpng  
```bash
cd /home/licheepi
wget https://download.sourceforge.net/libpng/libpng-1.6.40.tar.gz
tar -xzvf libpng-1.6.40.tar.gz
cd libpng-1.6.40

./configure \
    --host=riscv64-plctxthead-linux-gnu \
    --prefix=/home/licheepi/venv-sipeed/sysroot.riscv64-plctxthead-linux-gnu/usr \
    --enable-static \
    --disable-shared \
    CPPFLAGS="-I/home/licheepi/venv-sipeed/sysroot.riscv64-plctxthead-linux-gnu/usr/include" \
    LDFLAGS="-L/home/licheepi/venv-sipeed/sysroot.riscv64-plctxthead-linux-gnu/usr/lib"

make -j$(nproc)
make install
```
解决 omp.h 缺失问题
```bash
mkdir -p /home/licheepi/venv-sipeed/sysroot.riscv64-plctxthead-linux-gnu/usr/include
docker cp hhb_env:/usr/lib/gcc/x86_64-linux-gnu/9/include/omp.h \
    /home/licheepi/venv-sipeed/sysroot.riscv64-plctxthead-linux-gnu/usr/include/
```
修复 yolov5n.c 中的函数名问题
```bash
# 替换不兼容的函数名
sed -i 's/shl_ref_f32_to_input_dtype/shl_c920_f32_to_input_dtype/g' yolov5n.c
```

最终编译命令：  
```bash
riscv64-plctxthead-linux-gnu-gcc \
  yolov5n.c \
  hhb_out/io.c \
  hhb_out/model.c \
  hhb_out/process.c \
  -o yolov5n_example \
  -I hhb_out/ \
  -I th1520_npu_sdk/include/ \
  -I th1520_npu_sdk/include/shl_public/ \
  -I th1520_npu_sdk/include/csinn/ \
  -I . \
  th1520_npu_sdk/lib/libshl_c920.a \
  /home/licheepi/venv-sipeed/sysroot.riscv64-plctxthead-linux-gnu/usr/lib/libjpeg.a \
  /home/licheepi/venv-sipeed/sysroot.riscv64-plctxthead-linux-gnu/usr/lib/libpng.a \
  /home/licheepi/venv-sipeed/sysroot.riscv64-plctxthead-linux-gnu/usr/lib/libz.a \
  -lstdc++ -lpthread -ldl -lm \
  -mabi=lp64d -march=rv64gcv0p7_zfh_xtheadc \
  -Wl,--gc-sections -O2 -g
```
检查生成的文件：  
```bash
ls -la yolov5n_example
# 查看文件类型
file yolov5n_example
```
终端显示如下：  
```text
«Ruyi venv-sipeed» licheepi@licheepi-virtual-machine:~$ ls -la yolov5n_example
-rwxrwxr-x 1 licheepi licheepi 9640776  4月 27 15:25 yolov5n_example
«Ruyi venv-sipeed» licheepi@licheepi-virtual-machine:~$ file yolov5n_example
yolov5n_example: ELF 64-bit LSB executable, UCB RISC-V, RVC, double-float ABI, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux-riscv64-lp64d.so.1, BuildID[sha1]=a581dfa6e00424f79d7da7b9659cd5fbb5172789, for GNU/Linux 4.15.0, with debug_info, not stripped

```

### **运行示例并验证结果**
暂未验证
