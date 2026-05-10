---
sys: revyos
sys_ver: "20251226"
sys_var: null

status: AI
last_update: 2026-05-08

model: Lichee Pi 4A
profile: YOLOv5n
---


# **RuyiSDK示例**
本示例需要搭建好 NPU 使用相关环境，如没有搭建，请参考环境配置搭建。本示例暂未验证只描述过程  
## **环境配置**
### **开发板配置**
安装python虚拟环境  
```bash
sudo -i
apt install python3.11-venv
cd /root
python3 -m venv ort
source /root/ort/bin/activate
```
SHL库安装  
```bash
# 1. 安装 shl-python
pip3 install shl-python -i https://pypi.tuna.tsinghua.edu.cn/simple

# 2. 查看安装位置并复制动态库到系统目录
python3 -m shl --whereis th1520
# 假设输出为 /home/debian/ort/lib/python3.11/site-packages/shl/install_nn2/th1520

# 3. 根据输出路径复制动态库（注意替换实际路径）
sudo cp /home/debian/ort/lib/python3.11/site-packages/shl/install_nn2/th1520/lib/* /usr/lib/
sudo ldconfig
```
HHB-onnxruntime 安装  
HHB-onnxuruntime 是移植了 SHL 后端（execution providers），让 onnxruntime 能复用到 SHL 中针对玄铁 CPU 的高性能优化代码。  
CPU 版本  
```bash
wget https://github.com/zhangwm-pt/onnxruntime/releases/download/riscv_whl_v2.6.0/hhb_onnxruntime_c920-2.6.0-cp311-cp311-linux_riscv64.whl
pip install hhb_onnxruntime_c920-2.6.0-cp311-cp311-linux_riscv64.whl

```
NPU版本  
```bash
wget https://github.com/zhangwm-pt/onnxruntime/releases/download/riscv_whl_v2.6.0/hhb_onnxruntime_th1520-2.6.0-cp311-cp311-linux_riscv64.whl
pip install hhb_onnxruntime_th1520-2.6.0-cp311-cp311-linux_riscv64.whl
```
### **宿主机（x86）环境配置**
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
下载Yolov5n模型    
下载到示例目录 /home/example/th1520_npu/yolov5n 下：  
```bash
mkdir -p /home/example/th1520_npu/yolov5n
cd /home/example/th1520_npu/yolov5n
git clone https://gitclone.com/github.com/ultralytics/yolov5.git
cd yolov5
pip3 install ultralytics
```
如果遇到python版本不兼容的问题：  
在 Docker 容器内创建新的 Python 3.9 环境  
```bash
# 安装 python3.9 和 venv
apt update
apt install -y python3.9 python3.9-venv

# 创建虚拟环境
python3.9 -m venv /opt/yolo-venv

# 激活虚拟环境
source /opt/yolo-venv/bin/activate
```
 在新环境里安装依赖  
```bash
# 升级 pip
pip install --upgrade pip
# 安装 ultralytics
pip install ultralytics
pip install opencv-python-headless -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install pandas
pip install tqdm
pip install seaborn
#下载权重文件
wget https://github.com/ultralytics/yolov5/releases/download/v7.0/yolov5n.pt
```

```bashcd y
cd /home/example/th1520_npu/yolov5n/yolov5
# 导出模型
python3 export.py --weights yolov5n.pt --include onnx --imgsz 384 640  
```
退出虚拟环境：  
```bash
deactivate
```

HHB编译模型：  
将 ONNX 模型交叉编译成 NPU 上可执行的程序，需要使用 hhb 命令。  
编译时需要先进入到示例所在目录 /home/example/th1520_npu/yolov5n  
```bash
cd /home/example/th1520_npu/yolov5n
cp yolov5/yolov5n.onnx .
hhb -D \
  --model-file yolov5n.onnx \
  --board th1520 \
  --input-name "images" \
  --input-shape "1 3 384 640" \
  --data-scale-div 255 \
  --output-name "/model.24/m.0/Conv_output_0;/model.24/m.1/Conv_output_0;/model.24/m.2/Conv_output_0" \
  --calibrate-dataset kite.jpg \
  --quantization-scheme "int8_asym"
```
在终端显示如下：
```text
root@78776422f7c9:/home/example/th1520_npu/yolov5n# hhb -D \
>   --model-file yolov5n.onnx \
>   --data-scale-div 255 \
>   --board th1520 \
>   --input-name "images" \
>   --output-name "/model.24/m.0/Conv_output_0;/model.24/m.1/Conv_output_0;/model.24/m.2/Conv_output_0" \
>   --input-shape "1 3 384 640" \
>   --calibrate-dataset kite.jpg \
>   --quantization-scheme "int8_asym"
[2026-05-08 02:48:22] (HHB LOG): Start import model.
[2026-05-08 02:48:24] (HHB LOG): Model import completed! 
[2026-05-08 02:48:24] (HHB LOG): Start quantization.
[2026-05-08 02:48:24] (HHB LOG): get calibrate dataset from kite.jpg
[2026-05-08 02:48:24] (HHB LOG): Start optimization.
[2026-05-08 02:48:25] (HHB LOG): Optimization completed!
Calibrating: 100%|███████████████| 316/316 [00:37<00:00,  8.34it/s]
[2026-05-08 02:49:03] (HHB LOG): Start conversion to csinn.
[2026-05-08 02:49:04] (HHB LOG): Conversion completed!
[2026-05-08 02:49:04] (HHB LOG): Start operator fusion.
[2026-05-08 02:49:04] (HHB LOG): Operator fusion completed!
[2026-05-08 02:49:05] (HHB LOG): Start operator split.
[2026-05-08 02:49:05] (HHB LOG): Operator split completed!
[2026-05-08 02:49:05] (HHB LOG): Start layout convert.
[2026-05-08 02:49:05] (HHB LOG): Layout convert completed!
[2026-05-08 02:49:05] (HHB LOG): Quantization completed!

```
退出docker环境。  
```bash
exit
```
在终端显示如下：  
```bash
root@78776422f7c9:/home/example/th1520_npu/yolov5n# exit
exit
licheepi@licheepi-virtual-machine:~$ 
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

## **YOLOV5n测试示例**
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
riscv64-plctxthead-linux-gnu-g++ --version
# 复制整个yolov5n 目录
docker cp hhb_env:/home/example/th1520_npu/yolov5n .
```
把 Docker 里的官方库复制到宿主机
```bash
docker cp hhb_env:/usr/local/lib/python3.8/dist-packages/hhb/install_nn2/th1520 ./hhb_th1520

docker cp hhb_env:/usr/local/lib/python3.8/dist-packages/hhb/prebuilt/runtime/riscv_linux ./hhb_runtime

docker cp hhb_env:/usr/local/lib/python3.8/dist-packages/hhb/prebuilt/decode/install/lib/rv ./hhb_decode_lib
```
修改yolov5n.c源码：
```bash
cd ~/yolov5n
sed -i 's/shl_ref_f32_to_input_dtype/shl_c920_f32_to_input_dtype/g' yolov5n.c
```

最终编译命令：  
```bash
riscv64-plctxthead-linux-gnu-gcc \
  yolov5n.c \
  -o yolov5n_example \
  hhb_out/io.c \
  hhb_out/model.c \
  -Wl,--gc-sections \
  -O2 -g \
  -mabi=lp64d \
  -I . \
  -I hhb_out/ \
  -I /home/licheepi/hhb_th1520/include/ \
  -I /home/licheepi/hhb_th1520/include/shl_public/ \
  -I /home/licheepi/hhb_th1520/include/csinn/ \
  -L /home/licheepi/hhb_th1520/lib/ \
  -lshl \
  -L /home/licheepi/hhb_decode_lib/ \
  -L /home/licheepi/hhb_runtime/ \
  -lprebuilt_runtime \
  -ljpeg -lpng -lz -lstdc++ -lm \
  -march=rv64gcv0p7_zfh_xtheadc \
  -Wl,-unresolved-symbols=ignore-in-shared-libs

```
解决 omp.h 缺失问题
```bash
mkdir -p /home/licheepi/venv-sipeed/sysroot.riscv64-plctxthead-linux-gnu/usr/include
docker cp hhb_env:/usr/lib/gcc/x86_64-linux-gnu/9/include/omp.h \
    /home/licheepi/venv-sipeed/sysroot.riscv64-plctxthead-linux-gnu/usr/include/
cp ~/omp.h ~/yolov5n/
```

### **运行示例并验证结果**
暂未验证
