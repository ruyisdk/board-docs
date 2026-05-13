---
sys: revyos
sys_ver: "20251226"
sys_var: null

status: AI
last_update: 2026-05-06

model: Lichee Pi 4A
profile: MobilenetV2
---

# **RuyiSDK示例 AI 示例**
本示例需要搭建好 NPU 使用相关环境，如没有搭建，请参考环境配置搭建。
## 环境配置
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

```bash
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
docker pull hhb4tools/hhb:2.6.17
```
创建容器，名字为hhb_env  
```bash
docker run -itd --name hhb_env hhb4tools/hhb:2.6.17
#进入容器
docker exec -it hhb_env /bin/bash
```
获取本节教程的模型
```bash
sudo mkdir -p /home/example/th1520_npu/onnx_mobilenetv2_c++
#修改权限让当前用户可读写
sudo chown -R licheepi:licheepi /home/example
#进入目录
cd /home/example/th1520_npu/onnx_mobilenetv2_c++
```
在该目录下下载模型mobilenetv2-12.onnx
```bash
wget https://github.com/onnx/models/blob/main/validated/vision/classification/mobilenet/model/mobilenetv2-12.onnx
```
终端显示如下：  
```text
licheepi@licheepi-virtual-machine:~$ docker start hhb_env
hhb_env
licheepi@licheepi-virtual-machine:~$ docker exec -it hhb_env /bin/bash
root@78776422f7c9:/# cd /home/example/th1520_npu
root@78776422f7c9:/home/example/th1520_npu# mkdir -p /home/example/th1520_npu/onnx_mobilenetv2_c++
root@78776422f7c9:/home/example/th1520_npu# cd onnx_mobilenetv2_c++

root@78776422f7c9:/home/example/th1520_npu/onnx_mobilenetv2_c++# wget https://github.com/onnx/models/raw/main/validated/vision/classification/mobilenet/model/mobilenetv2-12.onnx
--2026-04-28 06:33:19--  https://github.com/onnx/models/raw/main/validated/vision/classification/mobilenet/model/mobilenetv2-12.onnx
Resolving github.com (github.com)... 20.205.243.166
Connecting to github.com (github.com)|20.205.243.166|:443... connected.
HTTP request sent, awaiting response... 302 Found
Location: https://media.githubusercontent.com/media/onnx/models/main/validated/vision/classification/mobilenet/model/mobilenetv2-12.onnx [following]
--2026-04-28 06:33:20--  https://media.githubusercontent.com/media/onnx/models/main/validated/vision/classification/mobilenet/model/mobilenetv2-12.onnx
Resolving media.githubusercontent.com (media.githubusercontent.com)... 185.199.109.133, 185.199.111.133, 185.199.110.133, ...
Connecting to media.githubusercontent.com (media.githubusercontent.com)|185.199.109.133|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 13964571 (13M) [application/octet-stream]
Saving to: 'mobilenetv2-12.onnx'

mobilenetv2-12.onn 100%[==============>]  13.32M  1.80MB/s    in 7.6s    
2026-04-28 06:33:29 (1.76 MB/s) - 'mobilenetv2-12.onnx' saved [13964571/13964571]
```
使用以下 wget 命令直接下载 MobilenetV2 示例所需的文件到当前目录：  
```bash
wget https://raw.githubusercontent.com/zhangwm-pt/lpi4a-example/main/classification/mobilenetv2/main.cpp
wget https://raw.githubusercontent.com/zhangwm-pt/lpi4a-example/main/classification/mobilenetv2/synset.txt
wget https://raw.githubusercontent.com/zhangwm-pt/lpi4a-example/main/classification/mobilenetv2/persian_cat.jpg
```
获取本次教程所使用的优化版本 opencv 所需的库文件
```bash
cd /home/example/th1520_npu/
git clone https://github.com/zhangwm-pt/prebuilt_opencv.git
```
在终端显示如下：
```text
root@78776422f7c9:/home/example/th1520_npu/onnx_mobilenetv2_c++# cd ..
root@78776422f7c9:/home/example/th1520_npu# git clone https://github.com/zhangwm-pt/prebuilt_opencv.git
Cloning into 'prebuilt_opencv'...
remote: Enumerating objects: 461, done.
remote: Counting objects: 100% (4/4), done.
remote: Compressing objects: 100% (3/3), done.
remote: Total 461 (delta 0), reused 4 (delta 0), pack-reused 457 (from 1)
Receiving objects: 100% (461/461), 47.56 MiB | 8.72 MiB/s, done.
Resolving deltas: 100% (78/78), done.
Updating files: 100% (395/395), done.
```
```bash
# 进入示例目录
cd /home/example/th1520_npu/onnx_mobilenetv2_c++

# 执行 HHB 编译模型
hhb -D --model-file mobilenetv2-12.onnx \
  --data-scale 0.017 \
  --data-mean "124 117 104" \
  --board th1520 \
  --postprocess save_and_top5 \
  --input-name "input" \
  --output-name "output" \
  --input-shape "1 3 224 224" \
  --calibrate-dataset persian_cat.jpg \
  --quantization-scheme "int8_asym"
```
会在终端显示如下：  
```text
root@78776422f7c9:/home/example/th1520_npu# cd /home/example/th1520_npu/onnx_mobilenetv2_c++

root@78776422f7c9:/home/example/th1520_npu/onnx_mobilenetv2_c++
# hhb -D --model-file mobilenetv2-12.onnx \
>   --data-scale 0.017 \
>   --data-mean "124 117 104" \
>   --board th1520 \
>   --postprocess save_and_top5 \
>   --input-name "input" \
>   --output-name "output" \
>   --input-shape "1 3 224 224" \
>   --calibrate-dataset persian_cat.jpg \
>   --quantization-scheme "int8_asym"
[2026-04-30 03:20:38] (HHB LOG): Start import model.
[2026-04-30 03:20:38] (HHB LOG): Model import completed! 
[2026-04-30 03:20:38] (HHB LOG): Start quantization.
[2026-04-30 03:20:38] (HHB LOG): get calibrate dataset from persian_cat.jpg
[2026-04-30 03:20:38] (HHB LOG): Start optimization.
[2026-04-30 03:20:39] (HHB LOG): Optimization completed!
Calibrating: 100%|███████████| 153/153 [00:13<00:00, 11.76it/s]
[2026-04-30 03:20:52] (HHB LOG): Start conversion to csinn.
[2026-04-30 03:20:52] (HHB LOG): Conversion completed!
[2026-04-30 03:20:52] (HHB LOG): Start operator fusion.
[2026-04-30 03:20:52] (HHB LOG): Operator fusion completed!
[2026-04-30 03:20:52] (HHB LOG): Start operator split.
[2026-04-30 03:20:52] (HHB LOG): Operator split completed!
[2026-04-30 03:20:52] (HHB LOG): Start layout convert.
[2026-04-30 03:20:52] (HHB LOG): Layout convert completed!
[2026-04-30 03:20:52] (HHB LOG): Quantization completed!

```
退出docker环境：
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


## **MobilenetV2**
### **示例描述和硬件环境准备**
本教程是一个如何在 LicheePi4A 平台上部署 mobilenetv2 模型完成图像分类的示例。  
硬件环境：Lichee Pi 4A (16GB)    
软件环境：RuyiSDK：0.47.0  HHB：2.6.17  
### **环境配置**
首先获取本节教程的模型
```bash
sudo mkdir -p /home/example/th1520_npu/onnx_mobilenetv2_c++
#修改权限让当前用户可读写
sudo chown -R licheepi:licheepi /home/example
#进入目录
cd /home/example/th1520_npu/onnx_mobilenetv2_c++
```
在该目录下下载模型mobilenetv2-12.onnx
```bash
wget https://github.com/onnx/models/blob/main/validated/vision/classification/mobilenet/model/mobilenetv2-12.onnx
```
终端显示如下：  
```text
licheepi@licheepi-virtual-machine:~$ docker start hhb_env
hhb_env
licheepi@licheepi-virtual-machine:~$ docker exec -it hhb_env /bin/bash
root@78776422f7c9:/# cd /home/example/th1520_npu
root@78776422f7c9:/home/example/th1520_npu# mkdir -p /home/example/th1520_npu/onnx_mobilenetv2_c++
root@78776422f7c9:/home/example/th1520_npu# cd onnx_mobilenetv2_c++

root@78776422f7c9:/home/example/th1520_npu/onnx_mobilenetv2_c++# wget https://github.com/onnx/models/raw/main/validated/vision/classification/mobilenet/model/mobilenetv2-12.onnx
--2026-04-28 06:33:19--  https://github.com/onnx/models/raw/main/validated/vision/classification/mobilenet/model/mobilenetv2-12.onnx
Resolving github.com (github.com)... 20.205.243.166
Connecting to github.com (github.com)|20.205.243.166|:443... connected.
HTTP request sent, awaiting response... 302 Found
Location: https://media.githubusercontent.com/media/onnx/models/main/validated/vision/classification/mobilenet/model/mobilenetv2-12.onnx [following]
--2026-04-28 06:33:20--  https://media.githubusercontent.com/media/onnx/models/main/validated/vision/classification/mobilenet/model/mobilenetv2-12.onnx
Resolving media.githubusercontent.com (media.githubusercontent.com)... 185.199.109.133, 185.199.111.133, 185.199.110.133, ...
Connecting to media.githubusercontent.com (media.githubusercontent.com)|185.199.109.133|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 13964571 (13M) [application/octet-stream]
Saving to: 'mobilenetv2-12.onnx'

mobilenetv2-12.onn 100%[==============>]  13.32M  1.80MB/s    in 7.6s    
2026-04-28 06:33:29 (1.76 MB/s) - 'mobilenetv2-12.onnx' saved [13964571/13964571]
```

获取本次教程所使用的优化版本 opencv 所需的库文件
```bash
cd /home/example/th1520_npu/
git clone https://github.com/zhangwm-pt/prebuilt_opencv.git
```
在终端显示如下：
```text
root@78776422f7c9:/home/example/th1520_npu/onnx_mobilenetv2_c++# cd ..
root@78776422f7c9:/home/example/th1520_npu# git clone https://github.com/zhangwm-pt/prebuilt_opencv.git
Cloning into 'prebuilt_opencv'...
remote: Enumerating objects: 461, done.
remote: Counting objects: 100% (4/4), done.
remote: Compressing objects: 100% (3/3), done.
remote: Total 461 (delta 0), reused 4 (delta 0), pack-reused 457 (from 1)
Receiving objects: 100% (461/461), 47.56 MiB | 8.72 MiB/s, done.
Resolving deltas: 100% (78/78), done.
Updating files: 100% (395/395), done.
```
```bash
# 进入示例目录
cd /home/example/th1520_npu/onnx_mobilenetv2_c++

# 执行 HHB 编译模型
hhb -D --model-file mobilenetv2-12.onnx \
  --data-scale 0.017 \
  --data-mean "124 117 104" \
  --board th1520 \
  --postprocess save_and_top5 \
  --input-name "input" \
  --output-name "output" \
  --input-shape "1 3 224 224" \
  --calibrate-dataset persian_cat.jpg \
  --quantization-scheme "int8_asym"
```
会在终端显示如下：  
```text
root@78776422f7c9:/home/example/th1520_npu# cd /home/example/th1520_npu/onnx_mobilenetv2_c++

root@78776422f7c9:/home/example/th1520_npu/onnx_mobilenetv2_c++
# hhb -D --model-file mobilenetv2-12.onnx \
>   --data-scale 0.017 \
>   --data-mean "124 117 104" \
>   --board th1520 \
>   --postprocess save_and_top5 \
>   --input-name "input" \
>   --output-name "output" \
>   --input-shape "1 3 224 224" \
>   --calibrate-dataset persian_cat.jpg \
>   --quantization-scheme "int8_asym"
[2026-04-30 03:20:38] (HHB LOG): Start import model.
[2026-04-30 03:20:38] (HHB LOG): Model import completed! 
[2026-04-30 03:20:38] (HHB LOG): Start quantization.
[2026-04-30 03:20:38] (HHB LOG): get calibrate dataset from persian_cat.jpg
[2026-04-30 03:20:38] (HHB LOG): Start optimization.
[2026-04-30 03:20:39] (HHB LOG): Optimization completed!
Calibrating: 100%|███████████| 153/153 [00:13<00:00, 11.76it/s]
[2026-04-30 03:20:52] (HHB LOG): Start conversion to csinn.
[2026-04-30 03:20:52] (HHB LOG): Conversion completed!
[2026-04-30 03:20:52] (HHB LOG): Start operator fusion.
[2026-04-30 03:20:52] (HHB LOG): Operator fusion completed!
[2026-04-30 03:20:52] (HHB LOG): Start operator split.
[2026-04-30 03:20:52] (HHB LOG): Operator split completed!
[2026-04-30 03:20:52] (HHB LOG): Start layout convert.
[2026-04-30 03:20:52] (HHB LOG): Layout convert completed!
[2026-04-30 03:20:52] (HHB LOG): Quantization completed!

```
退出docker环境：
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

## **MobilenetV2测试示例**
### **示例描述和硬件环境准备**
本教程是一个如何在 LicheePi4A 平台上部署 mobilenetv2 模型完成图像分类的示例。  
硬件环境：Lichee Pi 4A (16GB)    
软件环境：RuyiSDK：0.47.0  HHB：2.6.17  

### **创建并激活 ruyi 虚拟环境**

创建虚拟环境，命名为 yolox-venv，使用 sipeed-lpi4a profile。  

```bash

ruyi venv -t gnu-plct-xthead sipeed-lpi4a yolox-venv


```

进入虚拟环境目录  

```bash

cd yolox-venv

```

激活虚拟环境  ，该虚拟环境为后续开发板的运行提供了统一的运行环境。

```bash

source ./bin/ruyi-activate

```

### **使用 ruyi 工具链编译示例代码**

确认交叉编译器可用：
```bash
riscv64-plctxthead-linux-gnu-g++ --version
```
```bash
# 复制整个 onnx_mobilenetv2_c++ 目录（包含 main.cpp, hhb_out 等）
docker cp hhb_env:/home/example/th1520_npu/onnx_mobilenetv2_c++ .
# 复制 prebuilt_opencv 目录（交叉编译所需 OpenCV 库）
docker cp hhb_env:/home/example/th1520_npu/prebuilt_opencv .
```
交叉编译：
```bash
riscv64-plctxthead-linux-gnu-g++ \
  main.cpp \
  -I../prebuilt_opencv/include/opencv4 \
  -L../prebuilt_opencv/lib \
  -L../prebuilt_opencv/lib/opencv4/3rdparty \
  -lopencv_imgproc -lopencv_imgcodecs -lopencv_core \
  -llibjpeg-turbo -llibwebp -llibpng -llibtiff -llibopenjp2 \
  -lzlib -lcsi_cv -latomic -ldl -lpthread -lrt \
  -o mobilenetv2_example_ruyi
```

在终端显示如下：
```text
«Ruyi venv-sipeed» licheepi@licheepi-virtual-machine:~$ docker cp hhb_env:/home/example/th1520_npu/onnx_mobilenetv2_c++ .
Successfully copied 40.3MB to /home/licheepi/.
«Ruyi venv-sipeed» licheepi@licheepi-virtual-machine:~$ cd onnx_mobilenetv2_c++
«Ruyi venv-sipeed» licheepi@licheepi-virtual-machine:~/onnx_mobilenetv2_c++$ riscv64-plctxthead-linux-gnu-g++ \
  main.cpp \
  -I../prebuilt_opencv/include/opencv4 \
  -L../prebuilt_opencv/lib \
  -L../prebuilt_opencv/lib/opencv4/3rdparty \
  -lopencv_imgproc -lopencv_imgcodecs -lopencv_core \
  -llibjpeg-turbo -llibwebp -llibpng -llibtiff -llibopenjp2 \
  -lzlib -lcsi_cv -latomic -ldl -lpthread -lrt \
  -o mobilenetv2_example_ruyi

```

### **运行示例并验证结果**
把生成文件传递到开发板上：  
```bash
scp -r /home/licheepi/onnx_mobilenetv2_c++ debian@172.16.60.209:~/
```

终端显示如下：  
```text
«Ruyi venv-sipeed» licheepi@licheepi-virtual-machine:~/onnx_mobilenetv2_c++$ scp -r /home/licheepi/onnx_mobilenetv2_c++ debian@172.16.60.209:~/
debian@172.16.60.209's password: 
mobilenetv2_example                    100%   12MB 739.9KB/s   00:16    
synset.txt                             100%   31KB 834.8KB/s   00:00    
hhb_th1520_x86_jit                     100%  205KB   1.9MB/s   00:00    
io.c                                   100% 4936    98.8KB/s   00:00    
model.c                                100%  135KB   1.2MB/s   00:00    
input.0.bin                            100%  588KB   1.8MB/s   00:00    
hhb_th1520_x86_runtime                 100%  765KB   2.5MB/s   00:00    
jit.c                                  100% 1943    49.9KB/s   00:00    
hhb_jit                                100%  300KB   2.2MB/s   00:00    
hhb_runtime                            100%  705KB   2.2MB/s   00:00    
hhb_origin_cmd.txt                     100%  274    13.6KB/s   00:00    
hhb.bm                                 100% 3472KB   2.5MB/s   00:01    
model.params                           100% 3464KB   2.5MB/s   00:01    
model.o                                100%  284KB   1.9MB/s   00:00    
input.0.tensor                         100% 2794KB   2.6MB/s   00:01    
main.c                                 100% 7396   193.2KB/s   00:00    
main.o                                 100%   47KB   1.6MB/s   00:00    
process.h                              100% 2040    35.6KB/s   00:00    
jit.o                                  100%   13KB 121.8KB/s   00:00    
process.c                              100%   20KB 484.4KB/s   00:00    
io.h                                   100% 1539    32.0KB/s   00:00    
graph_info.bin                         100%  361    21.0KB/s   00:00    
mobilenetv2_example_ruyi               100% 4933KB   2.8MB/s   00:01    
mobilenetv2-12.onnx                    100%   13MB   2.6MB/s   00:05    
persian_cat.jpg                        100%  351KB   4.9MB/s   00:00    
main.cpp                               100% 3705   172.5KB/s   00:00 
```

先确认开发板驱动是否加载：  
```bah
lsmod
```
若在输出中有 img_mem，vha 和 vha_info 这三个模块，NPU驱动即加载成功。  
若没有加载，手动加载模块：  
```bash
sudo modprobe img_mem
sudo modprobe vha
sudo modprobe vha_info
```

运行程序：  
```bash
cd onnx_mobilenetv2_c++
./mobilenetv2_example_ruyi
```
如果遇到libshl_th1520.so.2 动态库加载失败问题，执行下面命令：  
```bash
#查找libshl_th1520.so.2
ls -la /usr/lib/riscv64-linux-gnu/libshl_th1520*
#  进入库目录
cd /usr/lib/riscv64-linux-gnu

# 创建软链接
sudo ln -sf libshl_th1520.so.3 libshl_th1520.so.2

# 验证链接已创建
ls -la libshl_th1520.so.2

# 更新动态链接库缓存
sudo ldconfig
```
然后重新运行程序。  

终端显示如下：
```text
(ort) debian@revyos-lpi4a:~/onnx_mobilenetv2_c++$ ./mobilenetv2_example_ruyi
 ********** preprocess image **********
 ********** run mobilenetv2 **********
INFO: NNA clock:426088 [kHz]
INFO: Heap :anonymous (0x2)
INFO: Heap :dmabuf (0x2)
INFO: Heap :unified (0x5)
[13595.961175] ax3xxx-nna fffc800000.vha: vha_map_to_onchip: moving a page to on chip ram failed!
WARNING: Mapping to the on chip ram failed (128 > 0), continuing...
[13595.978313] _img_mem_get_user_pages wrong alignment of 0xc639700 address!
[13595.985159] img_mem_import:701 getting user pages failed
FATAL: Importing 150528 bytes of CPU memory has failed (wrong memory alignment)
Run graph execution time: 15.00331ms, FPS=66.65

=== tensor info ===
shape: 1 3 224 224
data pointer: 0xc639700

=== tensor info ===
shape: 1 1000
data pointer: 0x3fb08a2000
The max_value of output: 16.053827
The min_value of output: -8.026914
The mean_value of output: -0.001889
The std_value of output: 9.203342
 ============ top5: ===========
283: 16.053827
281: 14.165141
287: 11.709850
285: 11.615416
282: 11.332113
 ********** postprocess result **********
 ********** probability top5: **********
n02123394 Persian cat
n02123045 tabby, tabby cat
n02127052 lynx, catamount
n02124075 Egyptian cat
n02123159 tiger cat
```
