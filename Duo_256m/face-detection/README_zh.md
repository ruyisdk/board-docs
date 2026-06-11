---
sys: buildroot
sys_ver: v1.1.4
sys_var: v1

status: AI
last_update: 2026-06-11

model: Milk-V Duo (256M)
profile: Face-Detection
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
## Face-Detection
### 示例描述和硬件环境准备
基于 TDL SDK 实现人脸检测，读取图像并进行推理，验证 Ruyi 工具链在 Duo 256M（RISC-V）上的交叉编译能力。   
硬件环境：Milk-V Duo 256M （SG2002 ),CAM-GC2083    
软件环境：Ubuntu，RuyiSDK 0.47.0，TDL SDK   

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
获取 TDL-SDK 示例源码    
```bash
git clone https://github.com/milkv-duo/cvitek-tdl-sdk-sg200x.git
```
进行交叉编译，生成sample_vi_fd文件：  
```bash
cd cvitek-tdl-sdk-sg200x/sample/cvi_tdl
make sample_vi_fd \
  KERNEL_ROOT=$HOME/cvitek-tdl-sdk-sg200x/sample \
  MW_PATH=$HOME/cvitek-tdl-sdk-sg200x/sample/3rd/middleware/v2 \
  TPU_PATH=$HOME/cvitek-tdl-sdk-sg200x/sample/3rd/tpu \
  IVE_PATH=$HOME/cvitek-tdl-sdk-sg200x/sample/3rd/middleware/v2 \
  CHIP=CV181X \
  SDK_VER=musl_riscv64
```
正确运行后在终端显示如下：  
```text
«Ruyi milkv-venv» duo256@duo256-virtual-machine:~/cvitek-tdl-sdk-sg200x/sample/cvi_tdl$ make sample_vi_fd \
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
CFLAGS: -mcpu=c906fdv -march=rv64imafdcv0p7xthead -mcmodel=medany -mabi=lp64d -O3 -DNDEBUG -D_MIDDLEWARE_V2_ -DCV181X -std=gnu11 -Wno-pointer-to-int-cast -fsigned-char -Werror=all -Wno-format-truncation -fdiagnostics-color=always -s -I/home/duo256/cvitek-tdl-sdk-sg200x/include -I/home/duo256/cvitek-tdl-sdk-sg200x/include/cvi_tdl -I/home/duo256/cvitek-tdl-sdk-sg200x/include/cvi_tdl_app -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/include -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/utils -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/rtsp/include/cvi_rtsp -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/middleware/v2/include -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/opencv/include -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/stb/include -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/middleware/v2/sample/common -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/middleware/v2/include/isp/cv181x/ -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/middleware/v2/include/panel -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/middleware/v2/include -I -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/middleware/v2/include -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/middleware/v2/include/linux -I/include/stb
CC: riscv64-unknown-linux-musl-gcc
CXX: riscv64-unknown-linux-musl-g++
USE_TPU_IVE: 
---------------------------------------
riscv64-unknown-linux-musl-gcc  -mcpu=c906fdv -march=rv64imafdcv0p7xthead -mcmodel=medany -mabi=lp64d -O3 -DNDEBUG -D_MIDDLEWARE_V2_ -DCV181X -std=gnu11 -Wno-pointer-to-int-cast -fsigned-char -Werror=all -Wno-format-truncation -fdiagnostics-color=always -s -I/home/duo256/cvitek-tdl-sdk-sg200x/include -I/home/duo256/cvitek-tdl-sdk-sg200x/include/cvi_tdl -I/home/duo256/cvitek-tdl-sdk-sg200x/include/cvi_tdl_app -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/include -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/utils -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/rtsp/include/cvi_rtsp -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/middleware/v2/include -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/opencv/include -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/stb/include -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/middleware/v2/sample/common -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/middleware/v2/include/isp/cv181x/ -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/middleware/v2/include/panel -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/middleware/v2/include -I -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/middleware/v2/include -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/middleware/v2/include/linux -I/include/stb -o /home/duo256/cvitek-tdl-sdk-sg200x/sample/cvi_tdl/sample_vi_fd.o -c /home/duo256/cvitek-tdl-sdk-sg200x/sample/cvi_tdl/sample_vi_fd.c
In file included from /home/duo256/cvitek-tdl-sdk-sg200x/include/cvi_tdl/cvi_tdl.h:5,
                 from /home/duo256/cvitek-tdl-sdk-sg200x/sample/utils/sample_utils.h:5,
                 from /home/duo256/cvitek-tdl-sdk-sg200x/sample/cvi_tdl/sample_vi_fd.c:5:
/home/duo256/cvitek-tdl-sdk-sg200x/include/cvi_tdl/core/cvi_tdl_core.h:173:79: warning: backslash and newline separated by space
  173 |   CVI_TDL_NAME_WRAP(CVI_TDL_SUPPORTED_MODEL_YOLOV8_HARDHAT)                   \
      |                                                                                
In file included from /home/duo256/cvitek-tdl-sdk-sg200x/include/cvi_tdl/core/cvi_tdl_custom.h:3,
                 from /home/duo256/cvitek-tdl-sdk-sg200x/include/cvi_tdl/cvi_tdl.h:6,
                 from /home/duo256/cvitek-tdl-sdk-sg200x/sample/utils/sample_utils.h:5,
                 from /home/duo256/cvitek-tdl-sdk-sg200x/sample/cvi_tdl/sample_vi_fd.c:5:
/home/duo256/cvitek-tdl-sdk-sg200x/include/cvi_tdl/core/cvi_tdl_core.h:173:79: warning: backslash and newline separated by space
  173 |   CVI_TDL_NAME_WRAP(CVI_TDL_SUPPORTED_MODEL_YOLOV8_HARDHAT)                   \
      |                                                                                
In file included from /home/duo256/cvitek-tdl-sdk-sg200x/include/cvi_tdl/core/cvi_tdl_utils.h:3,
                 from /home/duo256/cvitek-tdl-sdk-sg200x/include/cvi_tdl/cvi_tdl.h:7,
                 from /home/duo256/cvitek-tdl-sdk-sg200x/sample/utils/sample_utils.h:5,
                 from /home/duo256/cvitek-tdl-sdk-sg200x/sample/cvi_tdl/sample_vi_fd.c:5:
/home/duo256/cvitek-tdl-sdk-sg200x/include/cvi_tdl/core/cvi_tdl_core.h:173:79: warning: backslash and newline separated by space
  173 |   CVI_TDL_NAME_WRAP(CVI_TDL_SUPPORTED_MODEL_YOLOV8_HARDHAT)                   \
      |                                                                                
riscv64-unknown-linux-musl-gcc  -mcpu=c906fdv -march=rv64imafdcv0p7xthead -mcmodel=medany -mabi=lp64d -O3 -DNDEBUG -D_MIDDLEWARE_V2_ -DCV181X -std=gnu11 -Wno-pointer-to-int-cast -fsigned-char -Werror=all -Wno-format-truncation -fdiagnostics-color=always -s -I/home/duo256/cvitek-tdl-sdk-sg200x/include -I/home/duo256/cvitek-tdl-sdk-sg200x/include/cvi_tdl -I/home/duo256/cvitek-tdl-sdk-sg200x/include/cvi_tdl_app -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/include -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/utils -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/rtsp/include/cvi_rtsp -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/middleware/v2/include -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/opencv/include -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/stb/include -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/middleware/v2/sample/common -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/middleware/v2/include/isp/cv181x/ -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/middleware/v2/include/panel -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/middleware/v2/include -I -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/middleware/v2/include -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/middleware/v2/include/linux -I/include/stb -o /home/duo256/cvitek-tdl-sdk-sg200x/sample/utils/vi_vo_utils.o -c /home/duo256/cvitek-tdl-sdk-sg200x/sample/utils/vi_vo_utils.c
/home/duo256/cvitek-tdl-sdk-sg200x/sample/utils/vi_vo_utils.c: In function 'InitOutput':
/home/duo256/cvitek-tdl-sdk-sg200x/sample/utils/vi_vo_utils.c:688:13: warning: statement will never be executed [-Wswitch-unreachable]
  688 |     CVI_S32 s32Ret = CVI_SUCCESS;
      |             ^~~~~~
riscv64-unknown-linux-musl-gcc  -mcpu=c906fdv -march=rv64imafdcv0p7xthead -mcmodel=medany -mabi=lp64d -O3 -DNDEBUG -D_MIDDLEWARE_V2_ -DCV181X -std=gnu11 -Wno-pointer-to-int-cast -fsigned-char -Werror=all -Wno-format-truncation -fdiagnostics-color=always -s -I/home/duo256/cvitek-tdl-sdk-sg200x/include -I/home/duo256/cvitek-tdl-sdk-sg200x/include/cvi_tdl -I/home/duo256/cvitek-tdl-sdk-sg200x/include/cvi_tdl_app -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/include -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/utils -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/rtsp/include/cvi_rtsp -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/middleware/v2/include -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/opencv/include -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/stb/include -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/middleware/v2/sample/common -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/middleware/v2/include/isp/cv181x/ -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/middleware/v2/include/panel -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/middleware/v2/include -I -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/middleware/v2/include -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/middleware/v2/include/linux -I/include/stb -o /home/duo256/cvitek-tdl-sdk-sg200x/sample/utils/sample_utils.o -c /home/duo256/cvitek-tdl-sdk-sg200x/sample/utils/sample_utils.c
In file included from /home/duo256/cvitek-tdl-sdk-sg200x/include/cvi_tdl/cvi_tdl.h:5,
                 from /home/duo256/cvitek-tdl-sdk-sg200x/sample/utils/sample_utils.h:5,
                 from /home/duo256/cvitek-tdl-sdk-sg200x/sample/utils/sample_utils.c:1:
/home/duo256/cvitek-tdl-sdk-sg200x/include/cvi_tdl/core/cvi_tdl_core.h:173:79: warning: backslash and newline separated by space
  173 |   CVI_TDL_NAME_WRAP(CVI_TDL_SUPPORTED_MODEL_YOLOV8_HARDHAT)                   \
      |                                                                                
In file included from /home/duo256/cvitek-tdl-sdk-sg200x/include/cvi_tdl/core/cvi_tdl_custom.h:3,
                 from /home/duo256/cvitek-tdl-sdk-sg200x/include/cvi_tdl/cvi_tdl.h:6,
                 from /home/duo256/cvitek-tdl-sdk-sg200x/sample/utils/sample_utils.h:5,
                 from /home/duo256/cvitek-tdl-sdk-sg200x/sample/utils/sample_utils.c:1:
/home/duo256/cvitek-tdl-sdk-sg200x/include/cvi_tdl/core/cvi_tdl_core.h:173:79: warning: backslash and newline separated by space
  173 |   CVI_TDL_NAME_WRAP(CVI_TDL_SUPPORTED_MODEL_YOLOV8_HARDHAT)                   \
      |                                                                                
In file included from /home/duo256/cvitek-tdl-sdk-sg200x/include/cvi_tdl/core/cvi_tdl_utils.h:3,
                 from /home/duo256/cvitek-tdl-sdk-sg200x/include/cvi_tdl/cvi_tdl.h:7,
                 from /home/duo256/cvitek-tdl-sdk-sg200x/sample/utils/sample_utils.h:5,
                 from /home/duo256/cvitek-tdl-sdk-sg200x/sample/utils/sample_utils.c:1:
/home/duo256/cvitek-tdl-sdk-sg200x/include/cvi_tdl/core/cvi_tdl_core.h:173:79: warning: backslash and newline separated by space
  173 |   CVI_TDL_NAME_WRAP(CVI_TDL_SUPPORTED_MODEL_YOLOV8_HARDHAT)                   \
      |                                                                                
riscv64-unknown-linux-musl-gcc  -mcpu=c906fdv -march=rv64imafdcv0p7xthead -mcmodel=medany -mabi=lp64d -O3 -DNDEBUG -D_MIDDLEWARE_V2_ -DCV181X -std=gnu11 -Wno-pointer-to-int-cast -fsigned-char -Werror=all -Wno-format-truncation -fdiagnostics-color=always -s -I/home/duo256/cvitek-tdl-sdk-sg200x/include -I/home/duo256/cvitek-tdl-sdk-sg200x/include/cvi_tdl -I/home/duo256/cvitek-tdl-sdk-sg200x/include/cvi_tdl_app -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/include -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/utils -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/rtsp/include/cvi_rtsp -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/middleware/v2/include -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/opencv/include -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/stb/include -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/middleware/v2/sample/common -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/middleware/v2/include/isp/cv181x/ -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/middleware/v2/include/panel -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/middleware/v2/include -I -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/middleware/v2/include -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/middleware/v2/include/linux -I/include/stb -o /home/duo256/cvitek-tdl-sdk-sg200x/sample/utils/middleware_utils.o -c /home/duo256/cvitek-tdl-sdk-sg200x/sample/utils/middleware_utils.c
riscv64-unknown-linux-musl-gcc -mcpu=c906fdv -march=rv64imafdcv0p7xthead -mcmodel=medany -mabi=lp64d -O3 -DNDEBUG -D_MIDDLEWARE_V2_ -DCV181X -std=gnu11 -Wno-pointer-to-int-cast -fsigned-char -Werror=all -Wno-format-truncation -fdiagnostics-color=always -s -I/home/duo256/cvitek-tdl-sdk-sg200x/include -I/home/duo256/cvitek-tdl-sdk-sg200x/include/cvi_tdl -I/home/duo256/cvitek-tdl-sdk-sg200x/include/cvi_tdl_app -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/include -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/utils -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/rtsp/include/cvi_rtsp -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/middleware/v2/include -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/opencv/include -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/stb/include -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/middleware/v2/sample/common -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/middleware/v2/include/isp/cv181x/ -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/middleware/v2/include/panel -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/middleware/v2/include -I -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/middleware/v2/include -I/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/middleware/v2/include/linux -I/include/stb -L/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/middleware/v2/lib -L/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/middleware/v2/lib/3rd -lini -lsns_full -lsample -lisp -lvdec -lvenc -lawb -lae -laf -lcvi_bin -lcvi_bin_isp -lmisc -lisp_algo -lsys -lvpu -L/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/opencv/lib -lopencv_core -lopencv_imgproc -lopencv_imgcodecs -L/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/tpu/lib -lcnpy  -lcvikernel  -lcvimath  -lcviruntime  -lz -lm -L/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/middleware/v2/lib -lcvi_ive -L/home/duo256/cvitek-tdl-sdk-sg200x/lib -lcvi_tdl -L/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/lib -lpthread -latomic -L/home/duo256/cvitek-tdl-sdk-sg200x/sample/3rd/rtsp/lib -lcvi_rtsp -lcvi_tdl_app -o sample_vi_fd /home/duo256/cvitek-tdl-sdk-sg200x/sample/cvi_tdl/sample_vi_fd.o /home/duo256/cvitek-tdl-sdk-sg200x/sample/utils/vi_vo_utils.o /home/duo256/cvitek-tdl-sdk-sg200x/sample/utils/sample_utils.o /home/duo256/cvitek-tdl-sdk-sg200x/sample/utils/middleware_utils.o
rm /home/duo256/cvitek-tdl-sdk-sg200x/sample/utils/middleware_utils.o /home/duo256/cvitek-tdl-sdk-sg200x/sample/cvi_tdl/sample_vi_fd.o /home/duo256/cvitek-tdl-sdk-sg200x/sample/utils/sample_utils.o /home/duo256/cvitek-tdl-sdk-sg200x/sample/utils/vi_vo_utils.o
```
查看文件是否生成成功：  
```bash
 ls sample_vi_fd
```
```text
«Ruyi milkv-venv» duo256@duo256-virtual-machine:~/cvitek-tdl-sdk-sg200x/sample/cvi_tdl$ ls sample_vi_fd
sample_vi_fd
```
### 运行示例并验证结果
duo256m连接上CAM-GC2083摄像头。  
把sample_vi_fd文件传到开发板上：  
```bash
scp sample_vi_fd root@192.168.42.1:/root/
#把cvi_model文件传到开发板上
cd ~/cvitek-tdl-sdk-sg200x/cvimodel
scp scrfd_768_432_int8_1x.cvimodel root@192.168.42.1:/root/
```
在 Duo 的终端中为测试程序添加可执行权限  
```bash
chmod +x sample_vi_fd
```
在终端执行测试程序：  
```bash
./sample_vi_fd scrfd_768_432_int8_1x.cvimodel
```
在终端显示如下：  
```bash
[root@milkv-duo]~# ./sample_vi_fd scrfd_768_432_int8_1x.cvimodel
[SAMPLE_COMM_SNS_ParseIni]-1950: Parse /mnt/data/sensor_cfg.ini
[parse_source_devnum]-1605: devNum =  1
[parse_sensor_name]-1686: sensor =  GCORE_GC2083_MIPI_2M_30FPS_10BIT
[parse_sensor_busid]-1714: bus_id =  2
[parse_sensor_i2caddr]-1725: sns_i2c_addr =  37
[parse_sensor_mipidev]-1736: mipi_dev =  0
[parse_sensor_laneid]-1747: Lane_id =  1, 0, 2, -1, -1
[parse_sensor_pnswap]-1758: pn_swap =  0, 0, 0, 0, 0
MMF Version:7e0cc6a08-musl_riscv64
Create VBPool[0], size: (3110400 * 5) = 15552000 bytes
Create VBPool[1], size: (1382400 * 5) = 6912000 bytes
Create VBPool[2], size: (2764800 * 3) = 8294400 bytes
Total memory of VB pool: 30758400 bytes
Initialize SYS and VB
Initialize VI
ISP Vipipe(0) Allocate pa(0x8d056000) va(0x0x3fd8468000) size(291120)
stSnsrMode.u16Width 1920 stSnsrMode.u16Height 1080 25.000000 wdrMode 0 pstSnsObj 0x3fd92ba860
[SAMPLE_COMM_VI_StartMIPI]-483: sensor 0 stDevAttr.devno 0
awbInit ver 6.8@2021500
0 R:1400 B:3100 CT:2850
1 R:1500 B:2500 CT:3900
2 R:2300 B:1600 CT:6500
Golden 1024 1024 1024
WB Quadratic:0
isWdr:0
ViPipe:0,===GC2083 1080P 30fps 10bit LINE Init OK!===
********************************************************************************
cvi_bin_isp message
gerritId:      36403          commitId:      c69c5863e      
md5:           cab880835a2ad5184de5ed7762404b84
sensorNum      1              
sensorName0    2083           

PQBIN message
gerritId:      80171          commitId:      5c9d8fc5d      
md5:           ba5a510e093ad42db6788e6c2d13169e
sensorNum      3              
sensorName0    2053           

author:        wanqiang.he    desc:          思博慧CV1812H_GC2083_RGB_mode_V1.0.0
createTime:    2023-08-04 16:48:08version:       V1.1           
tool Version:       v3.0.5.24           mode:      
********************************************************************************
sensorName(0) mismatch, mwSns:2083 != pqBinSns:2053
[SAMPLE_COMM_ISP_Thread]-95: ISP Dev 0 running!
Initialize VPSS
---------VPSS[0]---------
Input size: (1920x1080)
Input format: (19)
VPSS physical device number: 1
Src Frame Rate: -1
Dst Frame Rate: -1
    --------CHN[0]-------
    Output size: (1280x720)
    Depth: 1
    Do normalization: 0
        Src Frame Rate: -1
        Dst Frame Rate: -1
    ----------------------
    --------CHN[1]-------
    Output size: (1280x720)
    Depth: 1
    Do normalization: 0
        Src Frame Rate: -1
        Dst Frame Rate: -1
    ----------------------
------------------------
Bind VI with VPSS Grp(0), Chn(0)
Attach VBPool(0) to VPSS Grp(0) Chn(0)
Attach VBPool(1) to VPSS Grp(0) Chn(1)
Initialize VENC
venc codec: h264
venc frame size: 1280x720
Initialize RTSP
rtsp://127.0.1.1/h264
prio:0
version: 1.4.0
scrfd768432 Build at 2023-12-25 01:21:44 For platform cv181x
Max SharedMem size:1658880
anchor:-8,-8,8,8
anchor:-16,-16,16,16
bbox:bbox_8_Conv_dequant
landmark:kps_8_Conv_dequant
score:score_8_Sigmoid_dequant
anchor:-32,-32,32,32
anchor:-64,-64,64,64
bbox:bbox_16_Conv_dequant
landmark:kps_16_Conv_dequant
score:score_16_Sigmoid_dequant
anchor:-128,-128,128,128
anchor:-256,-256,256,256
bbox:bbox_32_Conv_dequant
landmark:kps_32_Conv_dequant
score:score_32_Sigmoid_dequant
Enter TDL thread
Enter encoder thread
0 R:1165 B:3087 CT:2688
1 R:1464 B:2327 CT:3937
2 R:1974 B:1613 CT:7225
Golden 1464 1024 2327
wdrLEOnly:1
```
将摄像头对准人脸，实时检测 ，终端显示如下：  
```bash
face count: 6
face count: 5
face count: 6
face count: 5
face count: 4
face count: 3
face count: 2
face count: 1
face count: 0
```
可以安装[使用VLC查看拉流效果](https://milkv.io/zh/docs/duo/application-development/tdl-sdk/tdl-sdk-face-detection)
