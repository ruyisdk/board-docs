---
sys: buildroot
sys_ver: v1.1.4
sys_var: v1

status: AI
last_update: 2026-05-28

model: Milk-V Duo (256M)
profile: YOLOv5
---

# RuyiSDK AI 示例
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
## YOLOv5
### 示例描述和硬件环境准备
基于 TDL SDK 实现 YOLOv5 目标检测，读取图像并进行推理，验证 Ruyi 工具链在 Duo256M（RISC-V）上的交叉编译能力。   
硬件环境：Milk-V Duo256M （SG2002 ）  
软件环境：Ubuntu，RuyiSDK 0.47.0，TDL SDK
### 创建并激活 ruyi 虚拟环境
```bash
# 创建虚拟环境
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
下载 TDL SDK 源码
```bash
git clone https://github.com/milkv-duo/cvitek-tdl-sdk-sg200x.git  
```
```bash
#进入代码目录进行编译，生成sample_yolov5 程序
cd cvitek-tdl-sdk-sg200x/sample/cvi_yolo
make sample_yolov5 \
  KERNEL_ROOT=$HOME/cvitek-tdl-sdk-sg200x/sample \
  MW_PATH=$HOME/cvitek-tdl-sdk-sg200x/sample/3rd/middleware/v2 \
  TPU_PATH=$HOME/cvitek-tdl-sdk-sg200x/sample/3rd/tpu \
  IVE_PATH=$HOME/cvitek-tdl-sdk-sg200x/sample/3rd/middleware/v2 \
  CHIP=CV181X \
  SDK_VER=musl_riscv64
```
在终端显示如下：  
```bash
«Ruyi milkv-venv» duo256@duo256-virtual-machine:~$ cd cvitek-tdl-sdk-sg200x/sample/cvi_yolo
«Ruyi milkv-venv» duo256@duo256-virtual-machine:~/cvitek-tdl-sdk-sg200x/sample/cvi_yolo$ make sample_yolov5 \
  KERNEL_ROOT=$HOME/cvitek-tdl-sdk-sg200x/sample \
  MW_PATH=$HOME/cvitek-tdl-sdk-sg200x/sample/3rd/middleware/v2 \
  TPU_PATH=$HOME/cvitek-tdl-sdk-sg200x/sample/3rd/tpu \
  IVE_PATH=$HOME/cvitek-tdl-sdk-sg200x/sample/3rd/middleware/v2 \
  CHIP=CV181X \
  SDK_VER=musl_riscv64
---------------------------------------
CHIP: CV181X
SDK_VER: musl_riscv64
TDL SDK library path: /home/duo256/cvitek-tdl-sdk-sg200x/lib
TDL SDK include path: /home/duo256/cvitek-tdl-sdk-sg200x/include
Middleware include path: /home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/middleware/v2/include
Middleware library path: /home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/middleware/v2/lib
IVE library path: /home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/middleware/v2/lib
IVE include path: /home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/middleware/v2/include
TPU library path: /home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/tpu/lib
CFLAGS: -mcpu=c906fdv -march=rv64imafdcv0p7xthead -mcmodel=medany -mabi=lp64d -O3 -DNDEBUG -D_MIDDLEWARE_V2_ -Wno-maybe-uninitialized -DCV181X -std=gnu11 -Wno-pointer-to-int-cast -fsigned-char -Wno-format-truncation -fdiagnostics-color=always -s -lpthread -latomic -I/home/duo256/cvitek-tdl-sdk-sg200x/include -I/home/duo256/cvitek-tdl-sdk-sg200x/include/cvi_tdl -I/home/duo256/cvitek-tdl-sdk-sg200x/include/cvi_tdl_app -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/include -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/utils -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/rtsp/include/cvi_rtsp -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/middleware/v2/include -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/opencv/include -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/stb/include -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/middleware/v2/sample/common -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/middleware/v2/include/isp/cv181x/ -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/middleware/v2/include/panel -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/middleware/v2/include -I -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/middleware/v2/include -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/middleware/v2/include/linux -I/include/stb
CC: riscv64-unknown-linux-musl-gcc
CXX: riscv64-unknown-linux-musl-g++
USE_TPU_IVE: 
SAMPLW_MW_LIB: -L/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/middleware/v2/lib -L/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/middleware/v2/lib/3rd -lini -lsns_full -lsample -lisp -lvdec -lvenc -lawb -lae -laf -lcvi_bin -lcvi_bin_isp -lmisc -lisp_algo -lsys -lvpu -L/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/lib
SAMPLE_AUD_LIBS: -L/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/middleware/v2/lib -L/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/middleware/v2/lib/3rd -lini -lsns_full -lsample -lisp -lvdec -lvenc -lawb -lae -laf -lcvi_bin -lcvi_bin_isp -lmisc -lisp_algo -lsys -lvpu -L/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/lib -L/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/tpu/lib -lcnpy  -lcvikernel  -lcvimath  -lcviruntime  -lz -lm -L/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/middleware/v2/lib -lcvi_ive -L/home/duo256/cvitek-tdl-sdk-sg200x/lib -lcvi_tdl  -lcvi_audio -lcvi_vqe -lcvi_ssp -ltinyalsa -lcvi_VoiceEngine -lcvi_RES1 -lcli
---------------------------------------
riscv64-unknown-linux-musl-g++ -mcpu=c906fdv -march=rv64imafdcv0p7xthead -mcmodel=medany -mabi=lp64d -O3 -DNDEBUG -D_MIDDLEWARE_V2_ -Wno-maybe-uninitialized -DCV181X -std=gnu11 -Wno-pointer-to-int-cast -fsigned-char -Wno-format-truncation -fdiagnostics-color=always -s -lpthread -latomic -I/home/duo256/cvitek-tdl-sdk-sg200x/include -I/home/duo256/cvitek-tdl-sdk-sg200x/include/cvi_tdl -I/home/duo256/cvitek-tdl-sdk-sg200x/include/cvi_tdl_app -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/include -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/utils -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/rtsp/include/cvi_rtsp -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/middleware/v2/include -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/opencv/include -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/stb/include -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/middleware/v2/sample/common -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/middleware/v2/include/isp/cv181x/ -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/middleware/v2/include/panel -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/middleware/v2/include -I -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/middleware/v2/include -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/middleware/v2/include/linux -I/include/stb -o /home/duo256/cvitek-tdl-sdk-sg200x/sample/cvi_yolo/sample_yolov5.o -c /home/duo256/cvitek-tdl-sdk-sg200x/sample/cvi_yolo/sample_yolov5.cpp
cc1plus: warning: command-line option '-Wno-pointer-to-int-cast' is valid for C/ObjC but not for C++
cc1plus: warning: command-line option '-std=gnu11' is valid for C/ObjC but not for C++
/home/duo256/cvitek-tdl-sdk-sg200x/sample/cvi_yolo/sample_yolov5.cpp:1: warning: "_GNU_SOURCE" redefined
    1 | #define _GNU_SOURCE
      | 
<command-line>: note: this is the location of the previous definition
In file included from /home/duo256/cvitek-tdl-sdk-sg200x/include/cvi_tdl/cvi_tdl.h:5,
                 from /home/duo256/cvitek-tdl-sdk-sg200x/sample/cvi_yolo/sample_yolov5.cpp:14:
/home/duo256/cvitek-tdl-sdk-sg200x/include/cvi_tdl/core/cvi_tdl_core.h:173:79: warning: backslash and newline separated by space
  173 | L_SUPPORTED_MODEL_YOLOV8_HARDHAT)                   \
      |                                                      

In file included from /home/duo256/cvitek-tdl-sdk-sg200x/include/cvi_tdl/core/cvi_tdl_custom.h:3,
                 from /home/duo256/cvitek-tdl-sdk-sg200x/include/cvi_tdl/cvi_tdl.h:6,
                 from /home/duo256/cvitek-tdl-sdk-sg200x/sample/cvi_yolo/sample_yolov5.cpp:14:
/home/duo256/cvitek-tdl-sdk-sg200x/include/cvi_tdl/core/cvi_tdl_core.h:173:79: warning: backslash and newline separated by space
  173 | L_SUPPORTED_MODEL_YOLOV8_HARDHAT)                   \
      |                                                      

In file included from /home/duo256/cvitek-tdl-sdk-sg200x/include/cvi_tdl/core/cvi_tdl_utils.h:3,
                 from /home/duo256/cvitek-tdl-sdk-sg200x/include/cvi_tdl/cvi_tdl.h:7,
                 from /home/duo256/cvitek-tdl-sdk-sg200x/sample/cvi_yolo/sample_yolov5.cpp:14:
/home/duo256/cvitek-tdl-sdk-sg200x/include/cvi_tdl/core/cvi_tdl_core.h:173:79: warning: backslash and newline separated by space
  173 | L_SUPPORTED_MODEL_YOLOV8_HARDHAT)                   \
      |                                                      

riscv64-unknown-linux-musl-g++ -mcpu=c906fdv -march=rv64imafdcv0p7xthead -mcmodel=medany -mabi=lp64d -O3 -DNDEBUG -D_MIDDLEWARE_V2_ -Wno-maybe-uninitialized -DCV181X -std=gnu11 -Wno-pointer-to-int-cast -fsigned-char -Wno-format-truncation -fdiagnostics-color=always -s -lpthread -latomic -I/home/duo256/cvitek-tdl-sdk-sg200x/include -I/home/duo256/cvitek-tdl-sdk-sg200x/include/cvi_tdl -I/home/duo256/cvitek-tdl-sdk-sg200x/include/cvi_tdl_app -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/include -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/utils -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/rtsp/include/cvi_rtsp -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/middleware/v2/include -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/opencv/include -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/stb/include -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/middleware/v2/sample/common -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/middleware/v2/include/isp/cv181x/ -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/middleware/v2/include/panel -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/middleware/v2/include -I -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/middleware/v2/include -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/middleware/v2/include/linux -I/include/stb -L/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/middleware/v2/lib -L/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/middleware/v2/lib/3rd -lini -lsns_full -lsample -lisp -lvdec -lvenc -lawb -lae -laf -lcvi_bin -lcvi_bin_isp -lmisc -lisp_algo -lsys -lvpu -L/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/lib -L/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/tpu/lib -lcnpy  -lcvikernel  -lcvimath  -lcviruntime  -lz -lm -L/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/middleware/v2/lib -lcvi_ive -L/home/duo256/cvitek-tdl-sdk-sg200x/lib -lcvi_tdl  -L/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/opencv/lib -lopencv_core -lopencv_imgproc -lopencv_imgcodecs -o sample_yolov5 /home/duo256/cvitek-tdl-sdk-sg200x/sample/cvi_yolo/sample_yolov5.o
rm /home/duo256/cvitek-tdl-sdk-sg200x/sample/cvi_yolo/sample_yolov5.o
```
模型准备  
可以直接点击下载本文文档预编译好的[yolov5_cv181x_int8_sym.cvimodel](https://raw.githubusercontent.com/TOT2232/yolov5-object-detection/main/yolov5_cv181x_int8_sym.cvimodel)
或者参考 [TPU-MLIR](https://github.com/sophgo/tpu-mlir) 文档自己生成。  

测试图片准备  
从coco2017选择一张图片作为测试图片，复制到当前文件夹：  
```bash
cp dataset/COCO2017/val2017/000000000632.jpg .
```
### 运行示例并验证结果
将编译好的 sample_yolov5、cvimodel、要推理的 jpg 图片，拷贝到板端然后执行二进制程序：：  
```bash
scp sample_yolov5 yolov5_cv181x_int8_sym.cvimodel 000000000632.jpg root@192.168.42.1:/root/
```
在终端显示如下：  
```text
duo256@duo256-virtual-machine:~/yolov5$ scp sample_yolov5 yolov5_cv181x_int8_sym.cvimodel 000000000632.jpg root@192.168.42.1:/root/
root@192.168.42.1's password: 
sample_yolov5               100%   14KB   1.3MB/s   00:00    
yolov5_cv181x_int8_sym.cvim 100% 8005KB   3.1MB/s   00:02    
000000000632.jpg            100%  152KB   3.1MB/s   00:00    
duo256@duo256-virtual-machine:~/yolov5$ 
```
在板端上执行以下命令：  
```bash
export LD_LIBRARY_PATH='/mnt/system/lib'
./sample_yolov5 ./yolov5_cv181x_int8_sym.cvimodel  000000000632.jpg
```
在终端显示如下：  
```text
[root@milkv-duo]~# ./sample_yolov5 ./yolov5_cv181x_int8_sym.cvimodel  000000000632.jpg
version: 1.4.0
yolov5s Build at 2026-05-28 10:19:59 For platform cv181x
Max SharedMem size:5734400
model opened:./yolov5_cv181x_int8_sym.cvimodel
detect res: 338.046265 215.812744 427.360474 347.613159 0.897093 58
detect res: 0.000000 292.178070 408.717834 478.821899 0.871600 59
detect res: 183.598511 120.470505 240.307343 234.079102 0.806835 58
detect res: 253.451004 232.237274 342.765228 314.312286 0.742620 56
```