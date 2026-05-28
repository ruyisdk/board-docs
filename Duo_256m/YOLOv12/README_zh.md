---
sys: buildroot
sys_ver: v1.1.4
sys_var: v1

status: AI
last_update: 2026-05-28

model: Milk-V Duo (256M)
profile: YOLOv12
---

# RuyiSDK  AI 示例
### 安装依赖库
```bash
sudo apt update
sudo apt install git make build-essential
```
### 安装 RuyiSDK
```bash
# 下载并安装 ruyi
wget https://mirror.iscas.ac.cn/ruyisdk/ruyi/tags/0.47.0/ruyi-0.47.0.amd64
chmod +x ruyi-0.47.0.amd64
sudo cp ruyi-0.47.0.amd64 /usr/local/bin/ruyi
```
### 安装工具链
```bash
#初始化并更新 Ruyi 仓库
ruyi update
#下载 Duo 256M 专属工具链
ruyi install gnu-milkv-milkv-duo-musl-bin
```
## YOLOv12
### 示例描述和硬件环境准备
基于 TDL SDK 实现 YOLOv12 目标检测，读取图像并进行推理，验证 Ruyi 工具链在 Duo 256M（RISC-V）上的交叉编译能力。   
硬件环境：Milk-V Duo 256M （SG2002 ）  
软件环境：Ubuntu，RuyiSDK 0.47.0，TDL SDK  
### 模型准备与编译
可以直接点击下载预编译好的[yolo12n_cv181x_int8_sym.cvimodel](https://github.com/TOT2232/yolo12-object-detection.git)
或者根据本节文档步骤自己生成。 

生成 .cvimodel,首先下载 yolov12 仓库    
```bash
git clone https://github.com/sunsmarterjie/yolov12.git
```
创建 yolov12 的 python 虚拟化环境：  
```bash
sudo apt update
sudo apt install python3-venv
python3 -m venv yolo12_env
source yolo12_env/bin/activate
```
安装依赖：  
```bash
pip install --upgrade pip
pip install ultralytics onnx onnxsim opencv-python numpy
```
下载YOLOv12n权重：  
```bash
cd ~
mkdir -p yolo_export_work
cd yolo_export_work
wget https://github.com/ultralytics/assets/releases/download/v8.3.0/yolo12n.pt
```
获取 TDL-SDK 示例源码     
```bash
git clone https://github.com/milkv-duo/cvitek-tdl-sdk-sg200x.git
``` 
将 cvitek-tdl-sdk-sg200x/sample/yolo_export/yolov8_export.py 代码复制到 当前文件夹，yolo12 可兼容 yolov8 。     
```bash
cp ~/cvitek-tdl-sdk-sg200x/sample/yolo_export/yolov8_export.py .
python3 yolov8_export.py --weights ./yolo12n.pt --img-size 640 640
```
生成 yolo12n.onnx  
在终端显示如下：  
```bash
(yolo12_env) duo256@duo256-virtual-machine:~/yolo_export_work$ python3 yolov8_export.py --weights ./yolo12n.pt --img-size 640 640
Ultralytics 8.4.52 🚀 Python-3.10.12 torch-2.2.2+cu121 CPU (11th Gen Intel Core i7-11800H @ 2.30GHz)
YOLOv12n summary (fused): 159 layers, 2,590,824 parameters, 0 gradients, 6.5 GFLOPs

PyTorch: starting from 'yolo12n.pt' with input shape (1, 3, 640, 640) BCHW and output shape(s) ((1, 64, 80, 80), (1, 64, 40, 40), (1, 64, 20, 20), (1, 80, 80, 80), (1, 80, 40, 40), (1, 80, 20, 20)) (5.3 MB)

ONNX: starting export with onnx 1.14.0 opset 11...
ONNX: slimming with onnxslim 0.1.93...
ONNX: export success ✅ 1.7s, saved as 'yolo12n.onnx' (10.0 MB)

Export complete (2.1s)
Results saved to /home/duo256/yolo_export_work/yolo12n.onnx
Predict:         yolo predict task=detect model=yolo12n.onnx imgsz=640 
Validate:        yolo val task=detect model=yolo12n.onnx imgsz=640 data=None  
Visualize:       https://netron.app
```
首先请参考 [TPU-MLIR](https://github.com/sophgo/tpu-mlir) 文档 配置好 TPU-MLIR 工作环境  
配置好工作环境后,在与本项目同级目录下创建一个model_yolo12目录,将模型和图片文件放入其中。
```bash
mkdir -p ~/model_yolo12/image
```
下载一张测试图片  
```bash
cd ~/model_yolo12/image
wget https://raw.githubusercontent.com/ultralytics/ultralytics/main/ultralytics/assets/bus.jpg
```
下载COCO2017数据集，用于 INT8 量化校准。  
```bash
cd ~/model_yolo12
mkdir -p dataset/COCO2017
cd dataset/COCO2017
wget http://images.cocodataset.org/zips/val2017.zip
unzip val2017.zip
```
model_transform.py 将 onnx 模型转化成 mlir 中间格式模型,使用如下命令：  
```bash
model_transform.py \
    --model_name yolo12n \
    --model_def ../yolo_export_work/yolo12n.onnx \
    --input_shapes [[1,3,640,640]] \
    --mean 0.0,0.0,0.0 \
    --scale 0.0039216,0.0039216,0.0039216 \
    --keep_aspect_ratio \
    --pixel_format rgb \
    --test_input ./image/bus.jpg \
    --test_result yolov12n_top_outputs.npz \
    --mlir yolov12n.mlir
```
转换成 mlir 文件之后，会生成一个 yolo12n.mlir 文件。  
在终端显示如下：  
```text
root@b0ac5095de2b:/workspace/model_yolo12# ls
dataset                    yolo12n_top_f32_all_weight.npz
image                      yolov12n.mlir
yolo12n.ref_files.json     yolov12n_origin.mlir
yolo12n_in_f32.npz         yolov12n_top_outputs.npz
yolo12n_opt.onnx.prototxt
```
量化成 INT8 模型前需要运行 calibration.py，得到校准表，输入数据的数量根据情况准备 100~1000 张左右  

```bash
run_calibration.py yolov12n.mlir \
--dataset ./dataset/COCO2017/val2017 \
--input_num 100 \
-o yolo12n_cali_table
```
用校准表生成 int8 对称 cvimodel:  
```bash
model_deploy.py \
--mlir yolov12n.mlir \
--quant_input --quant_output \
--quantize INT8 \
--calibration_table yolo12n_cali_table \
--processor cv181x \
--model yolo12n_cv181x_int8_sym.cvimodel
```
编译完成后，会生成名为 yolo12n_cv181x_int8_sym.cvimodel 的文件。  
把该文件复制到  cvitek-tdl-sdk-sg200x/sample/cvi_yolo/下：  
```bash
cp yolo12n_cv181x_int8_sym.cvimodel /workspace/cvitek-tdl-sdk-sg200x/sample/cvi_yolo/
```
退出 Docker 环境
```bash
exit
```
### 创建并激活 ruyi 虚拟环境
```bash
# 创建虚拟环境
cd ~
ruyi venv -t gnu-milkv-milkv-duo-musl-bin generic milkv-venv

# 激活
source milkv-venv/bin/ruyi-activate

# 验证
which riscv64-unknown-linux-musl-gcc
```
在终端显示如下：  
```text
«Ruyi milkv-venv» duo256@duo256-virtual-machine:~$ which riscv64-unknown-linux-musl-gcc
/home/duo256/milkv-venv/bin/riscv64-unknown-linux-musl-gcc
```
### 使用 ruyi 工具链编译示例代码 
```bash
#进入TDL-SDK 示例源码目录，在该目录下下载v12.cpp,并命名为sample_v12.cpp
cd cvitek-tdl-sdk-sg200x/sample/cvi_yolo
wget -O sample_yolov12.cpp https://raw.githubusercontent.com/Arielfoever/milkv-yolo12/master/duo/v12.cpp
```
进行交叉编译生成,sample_yolov12
```bash
make sample_yolov12 \
  KERNEL_ROOT=$HOME/cvitek-tdl-sdk-sg200x/sample \
  MW_PATH=$HOME/cvitek-tdl-sdk-sg200x/sample/3rd/middleware/v2 \
  TPU_PATH=$HOME/cvitek-tdl-sdk-sg200x/sample/3rd/tpu \
  IVE_PATH=$HOME/cvitek-tdl-sdk-sg200x/sample/3rd/middleware/v2 \
  CHIP=CV181X \
  SDK_VER=musl_riscv64
```
从coco2017选择一张图片作为测试图片，复制到当前文件夹：  
```bash
cp ~/model_yolo12/dataset/COCO2017/val2017/000000000632.jpg .
```
### 运行示例并验证结果
将编译好的 sample_yolov12、yolo12n_cv181x_int8_sym.cvimodel、要推理的 jpg 图片，拷贝到板端然后执行二进制程序:    
```bash
scp sample_yolov12 yolo12n_cv181x_int8_sym.cvimodel 000000000632.jpg  root@192.168.42.1:/root/
```
执行以下命令运行：  
```bash
export LD_LIBRARY_PATH='/mnt/system/lib'
./sample_yolov12 yolo12n_cv181x_int8_sym.cvimodel 000000000632.jpg result.jpg
```
在终端显示如下：  
```text
[root@milkv-duo]~# ./sample_yolov12 yolo12n_cv181x_int8_sym.cvimodel 0000
00000632.jpg result.jpg
enter CVI_TDL_Get_YOLO_Preparam...
asign val 0 
asign val 1 
asign val 2 
setup yolov8 param 
enter CVI_TDL_Get_YOLO_Preparam...
setup yolov8 algorithm param 
yolov8 algorithm parameters setup success!
---------------------openmodel-----------------------
version: 1.4.0
yolo12n Build at 2026-05-21 17:30:20 For platform cv181x
Max SharedMem size:6553600
---------------------to do detection-----------------------
image read,width:640
image read,hidth:483
objnum:3
Detect bed(59): 0.000000 276.222504 401.405090 476.725952 0.880519
Detect potted plant(58): 338.550415 214.713257 431.708557 351.635864 0.849975
Detect potted plant(58): 183.956451 128.000290 239.281891 228.029083 0.640638
```
