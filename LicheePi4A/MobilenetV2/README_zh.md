| sys\_ver | RevyOS 20250110 |

| :--- | :--- |

| sys\_var | - |

| provider | RevyOS |

| status | AI |

| last\_update | 2026-04-23|

| model | Lichee Pi 4A |

| profile | MobilenetV2 |



# **RuyiSDK示例 AI 示例**
本示例在 Ruyi 环境下运行验证，但不涉及 Ruyi 工具链编译流程
## **安装依赖包**
### **安装Docker**
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

## **MobilenetV2测试示例**
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

终端显示如下：  
```text
licheepi@licheepi:~$ ls -la /home/example/th1520_npu/onnx_mobilenetv2_c++/
total 13648
drwxr-xr-x 2 licheepi licheepi     4096  4月 23 15:07 .
drwxr-xr-x 3 licheepi licheepi     4096  4月 23 14:27 ..
-rwxrwxr-x 1 licheepi licheepi 13964571  4月 23 15:07 mobilenetv2-12.onnx
text

获取本次教程所使用的优化版本 opencv 所需的库文件
```bash
cd /home/example/th1520_npu/
git clone https://github.com/zhangwm-pt/prebuilt_opencv.git
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
root@cebba2cbd428:/workspace# hhb -D --model-file mobilenetv2-12.onnx \
>       --data-scale 0.017 \
>       --data-mean "124 117 104" \
>       --board c920 \
>       --input-name "input" \
>       --output-name "output" \
>       --input-shape "1 3 224 224" \
>       --calibrate-dataset persian_cat.jpg \
>       --quantization-scheme "int8_asym"
[2026-04-23 09:35:53] (HHB LOG): Start import model.
[2026-04-23 09:35:54] (HHB LOG): Model import completed! 
[2026-04-23 09:35:54] (HHB LOG): Start quantization.
[2026-04-23 09:35:54] (HHB LOG): get calibrate dataset from persian_cat.jpg
[2026-04-23 09:35:54] (HHB LOG): Start optimization.
[2026-04-23 09:35:54] (HHB LOG): Optimization completed!
Calibrating: 100%|████████████████████████████████████████████| 153/153 [00:13<00:00, 11.10it/s]
[2026-04-23 09:36:08] (HHB LOG): Start conversion to csinn.
[2026-04-23 09:36:08] (HHB LOG): Conversion completed!
[2026-04-23 09:36:08] (HHB LOG): Start operator fusion.
[2026-04-23 09:36:09] (HHB LOG): Operator fusion completed!
[2026-04-23 09:36:09] (HHB LOG): Start operator split.
[2026-04-23 09:36:09] (HHB LOG): Operator split completed!
[2026-04-23 09:36:09] (HHB LOG): Start layout convert.
[2026-04-23 09:36:09] (HHB LOG): Layout convert completed!
[2026-04-23 09:36:09] (HHB LOG): Quantization completed!

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
### **运行示例并验证结果**

把生成的hhb_out传到开发板：  
```bash
scp -r /home/example/th1520_npu/onnx_mobilenetv2_c++/hhb_out debian@172.16.60.217:/home/debian/
cd /home/debian/hhb_out
./hhb_runtime hhb.bm input.0.tensor
```
在终端输出
```text

«Ruyi yolox-venv» debian@revyos-lpi4a:~$ cd /home/debian/hhb_out
«Ruyi yolox-venv» debian@revyos-lpi4a:~/hhb_out$ chmod +x hhb_runtime
«Ruyi yolox-venv» debian@revyos-lpi4a:~/hhb_out$ ./hhb_runtime
Please set valide args: ./model.elf hhb.bm [data1 data2 ...]|[.txt]
«Ruyi yolox-venv» debian@revyos-lpi4a:~/hhb_out$ ls -la
total 24596
drwxr-xr-x  2 debian debian    4096 Apr 23 16:52 .
drwxr-xr-x 12 debian debian    4096 Apr 23 16:52 ..
-rw-r--r--  1 debian debian     361 Apr 23 16:52 graph_info.bin
-rw-r--r--  1 debian debian 3555144 Apr 23 17:37 hhb.bm
-rwxr-xr-x  1 debian debian 5247952 Apr 23 17:37 hhb_jit
-rw-r--r--  1 debian debian     244 Apr 23 17:37 hhb_origin_cmd.txt
-rwxr-xr-x  1 debian debian 6362848 Apr 23 17:37 hhb_runtime
-rwxr-xr-x  1 debian debian  209976 Apr 23 16:52 hhb_th1520_x86_jit
-rwxr-xr-x  1 debian debian  783312 Apr 23 16:52 hhb_th1520_x86_runtime
-rw-r--r--  1 debian debian  602112 Apr 23 17:37 input.0.bin
-rw-r--r--  1 debian debian 2941691 Apr 23 17:37 input.0.tensor
-rw-r--r--  1 debian debian    4936 Apr 23 17:37 io.c
-rw-r--r--  1 debian debian    1539 Apr 23 17:37 io.h
-rw-r--r--  1 debian debian    1943 Apr 23 17:37 jit.c
-rw-r--r--  1 debian debian   18872 Apr 23 17:37 jit.o
-rw-r--r--  1 debian debian    7522 Apr 23 17:37 main.c
-rw-r--r--  1 debian debian   78816 Apr 23 17:37 main.o
-rw-r--r--  1 debian debian  137776 Apr 23 17:37 model.c
-rw-r--r--  1 debian debian 1609752 Apr 23 17:37 model.o
-rw-r--r--  1 debian debian 3546952 Apr 23 17:37 model.params
-rw-r--r--  1 debian debian   20086 Apr 23 17:37 process.c
-rw-r--r--  1 debian debian    2040 Apr 23 17:37 process.h                                              ./hhb_runtime hhb.bm input.0.tensori4a:~/hhb_out$ ./hhb_runtime hhb.bm input.0.tensor
Run graph execution time: 5087.07324ms, FPS=0.20

=== tensor info ===
shape: 1 3 224 224
data pointer: 0x3fb7ff6010

=== tensor info ===
shape: 1 1000
data pointer: 0x1cde30
The max_value of output: 10.065117
The min_value of output: -9.073855
The mean_value of output: -0.000381
The std_value of output: 8.266551
 ============ top5: ===========
716: 10.065117
794: 8.158845
489: 7.853841
549: 7.625089
695: 7.625089

```
