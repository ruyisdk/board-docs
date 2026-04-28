---
sys: revyos
sys_ver: "20250110"
sys_var: null

status: AI
last_update: 2026-04-27

model: Lichee Pi 4A
profile: MobilenetV2
---



# **RuyiSDK AI 示例**
本示例暂未验证只描述过程
## **安装依赖包**
### **安装Docker**
```bash
sudo apt update
sudo apt install -y ca-certificates curl
```

下载 Docker 官方安装脚本并执行
```bash
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
如果下载慢，可使用国内用户加速：
```bash
sudo mkdir -p /etc/docker
sudo tee /etc/docker/daemon.json <<-'EOF'
{
  "registry-mirrors": [
    "https://docker.1panel.live",
    "https://hub.rat.dev"
  ]
}
EOF
#重启docker服务
sudo systemctl daemon-reload
sudo systemctl restart docker
#拉取 HHB Docker 镜像
docker pull hhb4tools/hhb:2.6.17
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
# 1. 进入示例目录
cd /home/example/th1520_npu/onnx_mobilenetv2_c++

# 2. 进入 HHB Docker 容器（提示符会变成 root@...）
sudo docker run -it --rm -v $(pwd):/workspace hhb4tools/hhb:2.6.17 bash

# 3. 进入挂载的工作目录
cd /workspace

# 4. 执行 HHB 编译模型
hhb -D --model-file mobilenetv2-12.onnx \
      --data-scale 0.017 \
      --data-mean "124 117 104" \
      --board c920 \
      --input-name "input" \
      --output-name "output" \
      --input-shape "1 3 224 224" \
      --calibrate-dataset persian_cat.jpg \
      --quantization-scheme "int8_asym"
```
会在终端显示如下：  
```text
root@78776422f7c9:/home/example/th1520_npu# cd /home/example/th1520_npu/onnx_mobilenetv2_c++

root@78776422f7c9:/home/example/th1520_npu/onnx_mobilenetv2_c++# hhb -D --model-file mobilenetv2-12.onnx --data-scale 0.017 --data-mean "124 117 104"  --board th1520  --postprocess save_and_top5 --input-name "input" --output-name "output" --input-shape "1 3 224 224" --calibrate-dataset persian_cat.jpg  --quantization-scheme "int8_asym"
[2026-04-28 06:34:29] (HHB LOG): Start import model.
[2026-04-28 06:34:31] (HHB LOG): Model import completed! 
[2026-04-28 06:34:31] (HHB LOG): Start quantization.
[2026-04-28 06:34:31] (HHB LOG): get calibrate dataset from persian_cat.jpg
[2026-04-28 06:34:31] (HHB LOG): Start optimization.
[2026-04-28 06:34:31] (HHB LOG): Optimization completed!
Calibrating: 100%|██████████████████████| 153/153 [00:12<00:00, 11.78it/s]
[2026-04-28 06:34:44] (HHB LOG): Start conversion to csinn.
[2026-04-28 06:34:44] (HHB LOG): Conversion completed!
[2026-04-28 06:34:44] (HHB LOG): Start operator fusion.
[2026-04-28 06:34:45] (HHB LOG): Operator fusion completed!
[2026-04-28 06:34:45] (HHB LOG): Start operator split.
[2026-04-28 06:34:45] (HHB LOG): Operator split completed!
[2026-04-28 06:34:45] (HHB LOG): Start layout convert.
[2026-04-28 06:34:45] (HHB LOG): Layout convert completed!
[2026-04-28 06:34:45] (HHB LOG): Quantization completed!
```
退出docker环境：
```bash
exit
```

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

确认交叉编译器可用
```bash
riscv64-plctxthead-linux-gnu-g++ --version
# 复制整个 onnx_mobilenetv2_c++ 目录（包含 main.cpp, hhb_out 等）
docker cp hhb_env:/home/example/th1520_npu/onnx_mobilenetv2_c++ .

# 复制 prebuilt_opencv 目录（编译依赖）
docker cp hhb_env:/home/example/th1520_npu/prebuilt_opencv .
```
交叉编译：
```bash
riscv64-plctxthead-linux-gnu-g++ \
  main.cpp \
  -I../prebuilt_opencv/include/opencv4 \
  -L../prebuilt_opencv/lib \
  -L../prebuilt_opencv/lib/opencv4/3rdparty \
  -lopencv_imgproc \
  -lopencv_imgcodecs \
  -lopencv_core \
  -llibjpeg-turbo \
  -llibwebp \
  -llibpng \
  -llibtiff \
  -llibopenjp2 \
  -lzlib \
  -lcsi_cv \
  -latomic \
  -ldl \
  -lpthread \
  -lrt \
  -static \
  -o mobilenetv2_example
```

在终端显示如下：
```text
«Ruyi venv-sipeed» licheepi@licheepi-virtual-machine:~/onnx_mobilenetv2_c++$ riscv64-plctxthead-linux-gnu-g++ \
  main.cpp \
  -I../prebuilt_opencv/include/opencv4 \
  -L../prebuilt_opencv/lib \
  -L../prebuilt_opencv/lib/opencv4/3rdparty \
  -lopencv_imgproc \
  -lopencv_imgcodecs \
  -lopencv_core \
  -llibjpeg-turbo \
  -llibwebp \
  -llibpng \
  -llibtiff \
  -llibopenjp2 \
  -lzlib \
  -lcsi_cv \
  -latomic \
  -ldl \
  -lpthread \
  -lrt \
  -static \
  -o mobilenetv2_example
/home/licheepi/.local/share/ruyi/binaries/x86_64/gnu-plct-xthead-3.1.0-ruyi.20250526/bin/../lib/gcc/riscv64-plctxthead-linux-gnu/14.1.1/../../../../riscv64-plctxthead-linux-gnu/bin/ld: ../prebuilt_opencv/lib/libopencv_core.a(filesystem.cpp.o): in function `cv::plugin::impl::DynamicLib::libraryLoad(std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&)':
filesystem.cpp:(.text._ZN2cv6plugin4impl10DynamicLib11libraryLoadERKNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEE+0x4e): warning: Using 'dlopen' in statically linked applications requires at runtime the shared libraries from the glibc version used for linking
«Ruyi venv-sipeed» licheepi@licheepi-virtual-machine:~/onnx_mobilenetv2_c++$ ls -lh mobilenetv2_example
-rwxrwxr-x 1 licheepi licheepi 16M  4月 28 14:47 mobilenetv2_example
«Ruyi venv-sipeed» licheepi@licheepi-virtual-machine:~/onnx_mobilenetv2_c++$ 
```

### **运行示例并验证结果**
暂未验证
