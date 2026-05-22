---
sys: buildroot
sys_ver: v1.1.4
sys_var: v1

status: AI
last_update: 2026-05-20

model: Milk-V Duo (256M)
profile: YOLOv8
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
## YOLOv8
### 示例描述和硬件环境准备
基于 TDL SDK 实现 YOLOv8 目标检测，读取图像并进行推理，验证 Ruyi 工具链在 Duo 256M（RISC-V）上的交叉编译能力。   
硬件环境：Milk-V Duo 256M （SG2002 ）  
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
获取 TDL-SDK 示例源码  
```bash
git clone https://github.com/milkv-duo/cvitek-tdl-sdk-sg200x.git
#进入代码目录进行编译，生成sample_yolov8 程序
cd cvitek-tdl-sdk-sg200x/sample/cvi_yolo
make sample_yolov8 \
  KERNEL_ROOT=$HOME/cvitek-tdl-sdk-sg200x/sample \
  MW_PATH=$HOME/cvitek-tdl-sdk-sg200x/sample/3rd/middleware/v2 \
  TPU_PATH=$HOME/cvitek-tdl-sdk-sg200x/sample/3rd/tpu \
  IVE_PATH=$HOME/cvitek-tdl-sdk-sg200x/sample/3rd/middleware/v2 \
  CHIP=CV181X \
  SDK_VER=musl_riscv64
```
在终端显示如下：  
```text
itek-tdl-sdk-sg200x/sample/cvi_yolo$ make sample_yolov8 \
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
riscv64-unknown-linux-musl-g++ -mcpu=c906fdv -march=rv64imafdcv0p7xthead -mcmodel=medany -mabi=lp64d -O3 -DNDEBUG -D_MIDDLEWARE_V2_ -Wno-maybe-uninitialized -DCV181X -std=gnu11 -Wno-pointer-to-int-cast -fsigned-char -Wno-format-truncation -fdiagnostics-color=always -s -lpthread -latomic -I/home/duo256/cvitek-tdl-sdk-sg200x/include -I/home/duo256/cvitek-tdl-sdk-sg200x/include/cvi_tdl -I/home/duo256/cvitek-tdl-sdk-sg200x/include/cvi_tdl_app -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/include -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/utils -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/rtsp/include/cvi_rtsp -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/middleware/v2/include -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/opencv/include -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/stb/include -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/middleware/v2/sample/common -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/middleware/v2/include/isp/cv181x/ -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/middleware/v2/include/panel -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/middleware/v2/include -I -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/middleware/v2/include -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/middleware/v2/include/linux -I/include/stb -o /home/duo256/cvitek-tdl-sdk-sg200x/sample/cvi_yolo/sample_yolov8.o -c /home/duo256/cvitek-tdl-sdk-sg200x/sample/cvi_yolo/sample_yolov8.cpp
cc1plus: warning: command-line option '-Wno-pointer-to-int-cast' is valid for C/ObjC but not for C++
cc1plus: warning: command-line option '-std=gnu11' is valid for C/ObjC but not for C++
/home/duo256/cvitek-tdl-sdk-sg200x/sample/cvi_yolo/sample_yolov8.cpp:1: warning: "_GNU_SOURCE" redefined
    1 | #define _GNU_SOURCE
      | 
<command-line>: note: this is the location of the previous definition
In file included from /home/duo256/cvitek-tdl-sdk-sg200x/include/cvi_tdl/cvi_tdl.h:5,
                 from /home/duo256/cvitek-tdl-sdk-sg200x/sample/cvi_yolo/sample_yolov8.cpp:13:
/home/duo256/cvitek-tdl-sdk-sg200x/include/cvi_tdl/core/cvi_tdl_core.h:173:79: warning: backslash and newline separated by space
  173 | D_MODEL_YOLOV8_HARDHAT)                   \
      |                                            

In file included from /home/duo256/cvitek-tdl-sdk-sg200x/include/cvi_tdl/core/cvi_tdl_custom.h:3,
                 from /home/duo256/cvitek-tdl-sdk-sg200x/include/cvi_tdl/cvi_tdl.h:6,
                 from /home/duo256/cvitek-tdl-sdk-sg200x/sample/cvi_yolo/sample_yolov8.cpp:13:
/home/duo256/cvitek-tdl-sdk-sg200x/include/cvi_tdl/core/cvi_tdl_core.h:173:79: warning: backslash and newline separated by space
  173 | D_MODEL_YOLOV8_HARDHAT)                   \
      |                                            

In file included from /home/duo256/cvitek-tdl-sdk-sg200x/include/cvi_tdl/core/cvi_tdl_utils.h:3,
                 from /home/duo256/cvitek-tdl-sdk-sg200x/include/cvi_tdl/cvi_tdl.h:7,
                 from /home/duo256/cvitek-tdl-sdk-sg200x/sample/cvi_yolo/sample_yolov8.cpp:13:
/home/duo256/cvitek-tdl-sdk-sg200x/include/cvi_tdl/core/cvi_tdl_core.h:173:79: warning: backslash and newline separated by space
  173 | D_MODEL_YOLOV8_HARDHAT)                   \
      |                                            

riscv64-unknown-linux-musl-g++ -mcpu=c906fdv -march=rv64imafdcv0p7xthead -mcmodel=medany -mabi=lp64d -O3 -DNDEBUG -D_MIDDLEWARE_V2_ -Wno-maybe-uninitialized -DCV181X -std=gnu11 -Wno-pointer-to-int-cast -fsigned-char -Wno-format-truncation -fdiagnostics-color=always -s -lpthread -latomic -I/home/duo256/cvitek-tdl-sdk-sg200x/include -I/home/duo256/cvitek-tdl-sdk-sg200x/include/cvi_tdl -I/home/duo256/cvitek-tdl-sdk-sg200x/include/cvi_tdl_app -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/include -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/utils -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/rtsp/include/cvi_rtsp -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/middleware/v2/include -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/opencv/include -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/stb/include -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/middleware/v2/sample/common -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/middleware/v2/include/isp/cv181x/ -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/middleware/v2/include/panel -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/middleware/v2/include -I -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/middleware/v2/include -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/middleware/v2/include/linux -I/include/stb -L/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/middleware/v2/lib -L/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/middleware/v2/lib/3rd -lini -lsns_full -lsample -lisp -lvdec -lvenc -lawb -lae -laf -lcvi_bin -lcvi_bin_isp -lmisc -lisp_algo -lsys -lvpu -L/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/lib -L/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/tpu/lib -lcnpy  -lcvikernel  -lcvimath  -lcviruntime  -lz -lm -L/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/middleware/v2/lib -lcvi_ive -L/home/duo256/cvitek-tdl-sdk-sg200x/lib -lcvi_tdl  -L/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/opencv/lib -lopencv_core -lopencv_imgproc -lopencv_imgcodecs -o sample_yolov8 /home/duo256/cvitek-tdl-sdk-sg200x/sample/cvi_yolo/sample_yolov8.o
rm /home/duo256/cvitek-tdl-sdk-sg200x/sample/cvi_yolo/sample_yolov8.o
```
下载预编译好的 cvimodel  
```bash
git clone https://github.com/zwyzwm/YOLOv8-Object-Detection.git
```
下载一张测试图片到当前文件夹，命名为test  
```bash
wget https://ultralytics.com/images/zidane.jpg -O test.jpg
```

### 运行示例并验证结果
将编译好的 sample_yolov8、cvimodel 文件及测试图片拷贝到板端然后执行二进制程序:  
```bash
scp sample_yolov8 test.jpg root@192.168.42.1:/root/
cd YOLOv8-Object-Detection
scp yolov8n_cv181x_int8_sym.cvimodel root@192.168.42.1:/root/
```
执行以下命令：  
```bash
export LD_LIBRARY_PATH='/mnt/system/lib'
./sample_yolov8 ./yolov8n_cv181x_int8_sym.cvimodel  test.jpg 
```
在终端显示如下：  
```text
[root@milkv-duo]~# export LD_LIBRARY_PATH='/mnt/system/lib'
[root@milkv-duo]~# ./sample_yolov8 ./yolov8n_cv181x_int8_sym.
cvimodel test.jpg
enter CVI_TDL_Get_YOLO_Preparam...
asign val 0 
asign val 1 
asign val 2 
setup yolov8 param 
enter CVI_TDL_Get_YOLO_Preparam...
setup yolov8 algorithm param 
yolov8 algorithm parameters setup success!
---------------------openmodel-----------------------version: 1.4.0
yolov8n Build at 2024-07-31 14:30:32 For platform cv181x
Max SharedMem size:2048000
---------------------to do detection-----------------------
image read,width:1280
image read,hidth:720
objnum:2
boxes=[[107.747,197.723,1113.89,715.939,0,0.866496],[748.689,42.0825,1146.97,713.189,0,0.744361],]
```
