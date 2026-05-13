---
sys: revyos
sys_ver: "20251226"
sys_var: null

status: AI
last_update: 2026-05-11

model: Lichee Pi 4A
profile: YOLOV5s
---


# **RuyiSDK示例**
## **环境配置**
### **开发板配置**
安装python虚拟环境  
```bash
sudo -i
apt install python3.11-venv
cd /root
python3 -m venv ort
source /root/ort/bin/activate
#下载python依赖包
cd /home/debian
git clone -b python3.11 https://github.com/zhangwm-pt/prebuilt\_whl.git
cd prebuilt\_whl
pip install \*.whl
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
下载Yolov5s模型    
下载到示例目录 /home/example/th1520_npu/yolov5s 下：  
```bash
mkdir -p /home/example/th1520_npu/yolov5s
cd /home/example/th1520_npu/yolov5s
#使用 wget 命令，从官方示例仓库中下载运行推理所必需的文件。  
wget https://raw.githubusercontent.com/zhangwm-pt/lpi4a-example/main/detection/yolov5/coco.names
wget https://raw.githubusercontent.com/zhangwm-pt/lpi4a-example/main/detection/yolov5/inference.py
wget https://raw.githubusercontent.com/zhangwm-pt/lpi4a-example/main/detection/yolov5/kite.jpg
wget https://raw.githubusercontent.com/zhangwm-pt/lpi4a-example/main/detection/yolov5/yolov5n.c
#克隆官方仓库并安装依赖 
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
```

```bash
cd /home/example/th1520_npu/yolov5s/yolov5
# 导出模型
python3 export.py --weights yolov5s.pt --include onnx --imgsz 384 640  
```
退出虚拟环境：  
```bash
deactivate
```
HHB编译模型：  
将 ONNX 模型交叉编译成CPU上可执行的程序，需要使用 hhb 命令。  
编译时需要先进入到示例所在目录 /home/example/th1520_npu/yolov5s  
 ```bash
cd  /home/example/th1520_npu/yolov5s 
cp yolov5/yolov5s.onnx .
hhb -D \
  --model-file yolov5s.onnx \
  --data-scale-div 255 \
  --board c920 \
  --input-name "images" \
  --output-name "/model.24/m.0/Conv_output_0;/model.24/m.1/Conv_output_0;/model.24/m.2/Conv_output_0" \
  --input-shape "1 3 384 640" \
  --quantization-scheme float16
```
在终端显示如下：
```text
root@78776422f7c9:/home/example/th1520_npu/yolov5s# hhb -D \
>   --model-file yolov5s.onnx \
>   --data-scale-div 255 \
>   --board c920 \
>   --input-name "images" \
>   --output-name "/model.24/m.0/Conv_output_0;/model.24/m.1/Conv_output_0;/model.24/m.2/Conv_output_0" \
>   --input-shape "1 3 384 640" \
>   --quantization-scheme float16
[2026-05-11 07:45:33] (HHB LOG): Start import model.
[2026-05-11 07:45:34] (HHB LOG): Model import completed! 
[2026-05-11 07:45:34] (HHB LOG): Start quantization.
[2026-05-11 07:45:34] (HHB LOG): Start optimization.
[2026-05-11 07:45:34] (HHB LOG): Optimization completed!
[2026-05-11 07:45:35] (HHB LOG): Start conversion to csinn.
[2026-05-11 07:45:35] (HHB LOG): Conversion completed!
[2026-05-11 07:45:35] (HHB LOG): Start operator fusion.
[2026-05-11 07:45:35] (HHB LOG): Operator fusion completed!
[2026-05-11 07:45:35] (HHB LOG): Start operator split.
[2026-05-11 07:45:35] (HHB LOG): Operator split completed!
[2026-05-11 07:45:35] (HHB LOG): Start layout convert.
[2026-05-11 07:45:35] (HHB LOG): Layout convert completed!
[2026-05-11 07:45:35] (HHB LOG): Quantization completed!

```
退出docker环境。  
```bash
exit
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

## **YOLOV5s测试示例（CPU）**
### **示例描述和硬件环境准备**
本示例基于 LicheePi 4A（TH1520）平台，使用 HHB 工具链将 YOLOv5s 模型从 ONNX 格式转换为适用于 RISC-V 架构的可执行程序，并在开发板的 C920 CPU 上运行推理任务。  
硬件环境：Lichee Pi 4A (16GB)     
软件环境：RuyiSDK 0.47.0，HHB 2.6.17  
### **创建并激活 ruyi 虚拟环境**
如果没有ruyi虚拟环境，则创建虚拟环境 venv-sipeed  
```bash
ruyi venv -t gnu-plct-xthead sipeed-lpi4a venv-sipeed 
```
激活虚拟环境  
```bash
. venv-sipeed/bin/ruyi-activate 
```
### **使用 ruyi 工具链编译示例代码**
确认交叉编译器可用
```bash
riscv64-plctxthead-linux-gnu-g++ --version
# 复制整个yolov5s 目录
docker cp hhb_env:/home/example/th1520_npu/yolov5s .
```
把 Docker 里的官方库复制到宿主机
```bash
docker cp hhb_env:/usr/local/lib/python3.8/dist-packages/hhb/install_nn2/c920 ./hhb_c920
docker cp hhb_env:/usr/local/lib/python3.8/dist-packages/hhb/prebuilt/runtime/riscv_linux ./hhb_runtime
docker cp hhb_env:/usr/local/lib/python3.8/dist-packages/hhb/prebuilt/decode/install/lib/rv ./hhb_decode_lib
```
HHB 命令中截取到最后的卷积层为止，卷积层之后的后处理，由 yolov5s.c 文件处理。yolov5s.c 可以参考 yolov5n 示例下的 yolov5n.c 文件,这里直接使用yolov5n.c  
修改yolov5n.c源码：
```bash
cd ~/yolov5s
sed -i 's/shl_ref_f32_to_input_dtype/shl_c920_f32_to_input_dtype/g' yolov5n.c
```
最终交叉编译命令：  
```bash
riscv64-plctxthead-linux-gnu-gcc \
  yolov5n.c \
  -o yolov5s_example \
  hhb_out/io.c \
  hhb_out/model.c \
  -Wl,--gc-sections \
  -O2 -g \
  -mabi=lp64d \
  -I . \
  -I hhb_out/ \
  -I ~/hhb_c920/include/ \
  -I ~/hhb_c920/include/shl_public/ \
  -I ~/hhb_c920/include/csinn/ \
  -L ~/hhb_c920/lib/ \
  -lshl \
  -L ~/hhb_decode_lib/ \
  -L ~/hhb_runtime/ \
  -lprebuilt_runtime \
  -ljpeg -lpng -lz -lstdc++ -lm \
  -march=rv64gcv0p7_zfh_xtheadc \
  -Wl,-unresolved-symbols=ignore-in-shared-libs

```
生成的可执行文件 yolov5s_example 用于在开发板上运行模型推理  
交叉编译如果遇到 omp.h 缺失问题，进行如下操作：  
```bash
mkdir -p /home/licheepi/venv-sipeed/sysroot.riscv64-plctxthead-linux-gnu/usr/include
docker cp hhb_env:/usr/lib/gcc/x86_64-linux-gnu/9/include/omp.h \
    /home/licheepi/venv-sipeed/sysroot.riscv64-plctxthead-linux-gnu/usr/include/
cp ~/omp.h ~/yolov5s/
```
### **运行示例并验证结果**
把生成文件传递到开发板上：  
```bash
scp -r /home/licheepi/yolov5s debian@172.16.60.209:~/
```
激活开发板上的python虚拟环境  
```bash
source /home/debian/ort/bin/activate
```
运行程序  
```bash
cd yolov5s
python3 inference.py 

```
在终端显示如下：
```text
(ort) debian@revyos-lpi4a:~$ cd yolov5s
(ort) debian@revyos-lpi4a:~/yolov5s$ python3 inference.py
 ********** preprocess image **********
 ******* run yolov5 and postprocess *******
Run graph execution time: 821.27191ms, FPS=1.22
detect num: 4
id:     label   score           x1              y1              x2              y2
[0]:    0       0.932408        275.601013      159.205383      359.273254      329.114441
[1]:    0       0.888973        219.926437      221.956558      285.267334      334.161072
[2]:    0       0.840365        85.160255       184.234299      186.821136      346.101379
[3]:    33      0.785501        70.201889       176.143921      202.697464      218.391815
 ********** draw bbox **********
[275.601013, 159.205383, 359.273254, 329.114441, 0.932408, 0]
[219.926437, 221.956558, 285.267334, 334.161072, 0.888973, 0]
[85.160255, 184.234299, 186.821136, 346.101379, 0.840365, 0]
[70.201889, 176.143921, 202.697464, 218.391815, 0.785501, 33]

```
