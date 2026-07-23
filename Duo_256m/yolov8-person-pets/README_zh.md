---
sys: buildroot
sys_ver: v2.0.0
sys_var: v1

status: AI
last_update: 2026-06-17

model: Milk-V Duo (256M)
profile: Yolov8-Person-Pets
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
##  Yolov8-Person-Pets
### 示例描述和硬件环境准备
基于 TDL SDK 实现yolov8 人形及猫狗侦测，读取图像并进行推理，验证 Ruyi 工具链在 Duo 256M（RISC-V）上的交叉编译能力。   
硬件环境：Milk-V Duo 256M （SG2002 )，CAM-GC2083    
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
下载人形及猫狗检测程序源码  sample_vi_od.c   
```bash
git clone https://github.com/milkv-duo/duo-tdl-examples.git
```
进入目录，激活环境：  
```bash
cd duo-tdl-examples
source envsetup.sh
```
在终端显示如下：  
```bash
«Ruyi milkv-venv» duo256@duo256-virtual-machine:~$ cd duo-tdl-examples
«Ruyi milkv-venv» duo256@duo256-virtual-machine:~/duo-tdl-examples$ source envsetup.sh
script_dir: /home/duo256/duo-tdl-examples
Select Product:
1. Duo (CV1800B)
2. Duo256M (SG2002) or DuoS (SG2000)
Which would you like: 2
Select Arch:
1. ARM64
2. RISCV64
Which would you like: 2
CHIP: CV181X
ARCH: riscv64
~/duo-tdl-examples ~/duo-tdl-examples
~/duo-tdl-examples
Environment is ready.
```
之后，进行编译，生成sample_vi_od：  
```bash 
 cd sample_vi_od
 make sample_vi_od \
  CHIP=CV181X \
  COMMON_DIR=../common \
  TOOLCHAIN_PREFIX=riscv64-unknown-linux-musl- \
  CC=riscv64-unknown-linux-musl-gcc \
  CFLAGS="-I../include -I../include/isp/cv181x" \
  LDFLAGS="-L../libs"
```
### 运行示例并验证结果
duo256m连接上CAM-GC2083摄像头,确认排线插紧后再通电开机。     
将编译生成的 sample_vi_od 在电脑上通过 scp 命令上传到 Duo 开发板中:  
```bash
scp sample_vi_od root@192.168.42.1:/root/
```
下载用于人形及猫狗侦测检测的 cvimodel ,并传到开发板上  
```bash
wget https://github.com/sophgo/tdl_models/raw/refs/heads/main/cv181x/yolov8n_det_pet_person_384_640_INT8_cv181x.cvimodel
scp yolov8n_det_pet_person_384_640_INT8_cv181x.cvimodel root@192.168.42.1:/root/
```
执行以下命令，将电脑上的库文件夹传到板子上：   
```bash
scp -r ../libs root@192.168.42.1:/root/
```
给文件添加可执行的权限：  
```bash
chmod +x sample_vi_od
```
在duo256m终端执行以下命令：  
```bash
# 配置对应的 musl 和 cv181x_riscv64 路径
export LD_LIBRARY_PATH='/root/libs/system/musl_riscv64:/root/libs/tdl/cv181x_riscv64:/mnt/system/lib'

# 执行程序
./sample_vi_od yolov8-person-pets yolov8n_det_pet_person_384_640_INT8_cv181x.cvimodel
```
在终端显示如下：  
```bash
[root@milkv-duo]~# ./sample_vi_od yolov8-person-pets yolov8n_det_pet_person_384_640_INT8_cv181x.cvimodel
[SAMPLE_COMM_SNS_ParseIni]-2168: Parse /mnt/data/sensor_cfg.ini
[parse_source_devnum]-1761: devNum =  1
[parse_sensor_name]-1842: sensor =  GCORE_GC2083_MIPI_2M_30FPS_10BIT
[parse_sensor_busid]-1871: bus_id =  2
[parse_sensor_i2caddr]-1882: sns_i2c_addr =  37
[parse_sensor_mipidev]-1893: mipi_dev =  0
[parse_sensor_laneid]-1904: Lane_id =  1, 0, 2, -1, -1
[parse_sensor_pnswap]-1915: pn_swap =  0, 0, 0, 0, 0
MMF Version:d0c75d2ae-64bit
Create VBPool[0], size: (3110400 * 3) = 9331200 bytes
Create VBPool[1], size: (3110400 * 3) = 9331200 bytes
Create VBPool[2], size: (2359296 * 1) = 2359296 bytes
Total memory of VB pool: 21021696 bytes
Initialize SYS and VB
Cannot open '/dev/cvi-vo': 2, No such file or directory
Initialize VI
ISP Vipipe(0) Allocate pa(0x8c70e000) va(0x0x3fd8dac000) size(284096)
stSnsrMode.u16Width 1920 stSnsrMode.u16Height 1080 30.000000 wdrMode 0 pstSnsObj 0x3fd9ae83e8
[SAMPLE_COMM_VI_StartMIPI]-494: sensor 0 stDevAttr.devno 0
awbInit ver 6.9@2021500
0 R:1400 B:3100 CT:2850
1 R:1500 B:2500 CT:3900
2 R:2300 B:1600 CT:6500
Golden 1024 1024 1024
WB Quadratic:0
isWdr:0
ViPipe:0,===GC2083 1080P 30fps 10bit LINE Init OK!===
********************************************************************************
cvi_bin_isp message
gerritId:      NULL           commitId:      d0c75d2ae
md5:           9b60189725b5bcb970ec86e4bbdbf600
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
JSON_READ_ERR:DATA_TYPE 76(L) vc_motion.MotionThreshold

JSON_READ_ERR:NOT_EXIST 70(L) AWBAttrEx.u16MultiLSThr

JSON_READ_ERR:NOT_EXIST 70(L) AWBAttrEx.u16CALumaDiff

JSON_READ_ERR:NOT_EXIST 70(L) AWBAttrEx.u16CAAdjustRatio

JSON_READ_ERR:NOT_EXIST 70(L) AWBAttrEx.stInterference

[SAMPLE_COMM_ISP_Thread]-390: ISP Dev 0 running!
Initialize VPSS
---------VPSS[0]---------
Input size: (1920x1080)
Input format: (19)
VPSS physical device number: 1
Src Frame Rate: -1
Dst Frame Rate: -1
    --------CHN[0]-------
    Output size: (1920x1080)
    Depth: 1
    Do normalization: 0
        Src Frame Rate: -1
        Dst Frame Rate: -1
    ----------------------
    --------CHN[1]-------
    Output size: (1920x1080)
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
venc frame size: 1920x1080
Initialize RTSP
prio:0
Cannot open '/dev/cvi-vo': 2, No such file or directory
Enter TDL thread
Enter encoder thread
0 R:1165 B:3087 CT:2688
1 R:1464 B:2327 CT:3937
2 R:1974 B:1613 CT:7225
Golden 1464 1024 2327
wdrLEOnly:1
```
摄像头对准人和猫狗图片，终端打印如下：  
```bash
person: 866.44 38.92 1912.08 1059.29 2 0.59
cat:    1109.08 318.23 1491.49 721.45 0 0.58
person: 1146.97 582.40 1371.02 927.67 2 0.50
person: 1151.52 582.72 1371.98 927.56 2 0.50
dog:    948.55 718.26 1133.45 975.10 1 0.50
```
可以参考安装[使用VLC查看拉流效果](https://milkv.io/zh/docs/duo/application-development/tdl-sdk/yolov8-person-pets-detection)
