| sys\_ver | RevyOS 20250110 |

| :--- | :--- |

| sys\_var | - |

| provider | RevyOS |

| status | AI |

| last\_update | 2026-04-22 |

| model | Lichee Pi 4A |

| profile | YOLOX |



# **RuyiSDK示例AI示例**

Ruyi环境搭建  

更新ruyi软件包列表并安装编译工具链  

```bash

ruyi update

ruyi install gnu-plct-xthead

```

终端会看到如下输出：

```text

info: skipping already installed package gnu-plct-xthead-3.1.0-ruyi.20250526

```

## **YOLOX 目标检测示例**

### **示例描述和硬件环境准备**

示例描述  

YOLOX 是一个高性能的目标检测模型，本示例在 Lichee Pi 4A 上运行 YOLOX，对输入图片进行目标检测，输出带检测框的结果图片。  

硬件环境：Lichee Pi 4A (16GB)  

软件环境：RuyiSDK：0.47.0   Python：3.11.4   



### **创建并激活ruyi虚拟环境**

创建虚拟环境，命名为 yolox-venv，使用 sipeed-lpi4a profile。  

```bash

ruyi venv -t gnu-plct-xthead sipeed-lpi4a yolox-venv


```

进入虚拟环境目录  

```bash

cd yolox-venv

```



激活虚拟环境  

```bash

source ./bin/ruyi-activate

```

终端会显示如下输出  

```text

debian@revyos-lpi4a:\~$ ruyi venv -t gnu-plct-xthead sipeed-lpi4a yolox-venv

info: Creating a Ruyi virtual environment at yolox-venv...

info: The virtual environment is now created.



You may activate it by sourcing the appropriate activation script in the

bin directory, and deactivate by invoking `ruyi-deactivate`.



A fresh sysroot/prefix is also provisioned in the virtual environment.

It is available at the following path:



&#x20;   /home/debian/yolox-venv/sysroot



The virtual environment also comes with ready-made CMake toolchain file

and Meson cross file. Check the virtual environment root for those;

comments in the files contain usage instructions.



debian@revyos-lpi4a:\~$ cd yolox-venv

debian@revyos-lpi4a:\~/yolox-venv$ source ./bin/ruyi-activate

«Ruyi yolox-venv» debian@revyos-lpi4a:\~/yolox-venv$

```

本示例在 Ruyi 环境下运行验证，但不涉及 Ruyi 工具链编译流程，属于 Python + ONNXRuntime 的应用级推理示例。  



在Ruyi环境中配置Python并运行YOLOX  

安装pip  

```bash

sudo apt install python3-pip  -y

```



安装virtualenv  

```bash

sudo apt install python3-virtualenv -y

```

用virtualenv创建python3.11虚拟环境  

```bash

virtualenv -p python3.11 ort

```

激活虚拟环境  

```bash

source ort/bin/activate

```

在终端可以看到  

```text

«Ruyi yolox-venv» debian@revyos-lpi4a:\~/yolox-venv$ source ort/bin/activate

(ort) «Ruyi yolox-venv» debian@revyos-lpi4a:\~/yolox-venv$

```

至此python环境创建成功  



获取YOLOX模型  

在ruyi虚拟环境中下载github上的源码  

```bash

git clone https://github.com/Megvii-BaseDetection/YOLOX.git

cd YOLOX/demo/ONNXRuntime

wget https://github.com/Megvii-BaseDetection/YOLOX/releases/download/0.1.1rc0/yolox\_s.onnx

```

用 nano 编辑 onnx\_inference.py    

```bash

nano /home/debian/YOLOX/demo/ONNXRuntime/onnx\_inference.py

```

在 import argparse 之前添加：  

```bash

import sys

sys.path.insert(0, "../../")

```

最后完整的文件如下：  

```text

import sys

sys.path.insert(0, "../..")

import argparse

import os



import cv2

import numpy as np



import onnxruntime



from yolox.data.data\_augment import preproc as preprocess

from yolox.data.datasets import COCO\_CLASSES

from yolox.utils import mkdir, multiclass\_nms, demo\_postprocess, vis





def make\_parser():

&#x20;   parser = argparse.ArgumentParser("onnxruntime inference sample")

```

安装依赖包  

下载预编译好的python依赖包  

```bash

cd /home/debian

git clone -b python3.11 https://github.com/zhangwm-pt/prebuilt\_whl.git

cd prebuilt\_whl

pip install \*.whl

```

在终端会有如下显示：  

```text

(ort) «Ruyi yolox-venv» debian@revypip install numpy-1.25.0-cp311-cp311-linux\_riscv64.whl1-cp311-linux\_riProcessing ./numpy-1.25.0-cp311-cp311-linux\_riscv64.whl

Installing collected packages: numpy

Successfully installed numpy-1.25.0

(ort) «Ruyi yolox-venv» debian@revypip install opencv\_python-4.5.4+4cd224d-cp311-cp311-linux\_riscv64.whl1Processing ./opencv\_python-4.5.4+4cd224d-cp311-cp311-linux\_riscv64.whl

Requirement already satisfied: numpy>=1.21.2 in /home/debian/yolox-venv/ort/lib/python3.11/site-packages (from opencv-python==4.5.4+4cd224d) (1.25.0)

Installing collected packages: opencv-python

Successfully installed opencv-python-4.5.4+4cd224d

(ort) «Ruyi yolox-venv» debian@revypip install kiwisolver-1.4.4-cp311-cp311-linux\_riscv64.whl1-cp311-linuProcessing ./kiwisolver-1.4.4-cp311-cp311-linux\_riscv64.whl

Installing collected packages: kiwisolver

Successfully installed kiwisolver-1.4.4

(ort) «Ruyi yolox-venv» debian@revypip install Pillow-9.5.0-cp311-cp311-linux\_riscv64.whl1-cp311-linux\_riProcessing ./Pillow-9.5.0-cp311-cp311-linux\_riscv64.whl

Installing collected packages: pillow

Successfully installed pillow-9.5.0

```

安装 HHB-onnxruntime  

```bash

wget https://github.com/zhangwm-pt/onnxruntime/releases/download/riscv\_whl/onnxruntime-1.14.1-cp311-cp311-linux\_riscv64.whl

pip install onnxruntime-1.14.1-cp311-cp311-linux\_riscv64.whl

```

终端显示如下：  

```text

Successfully installed coloredlogs-15.0.1 flatbuffers-25.12.19 humanfriendly-10.0 onnxruntime-1.14.1 protobuf-7.34.1

```

### **运行示例并验证结果**



```bash

cd /home/debian/YOLOX/demo/ONNXRuntime

python3 onnx\_inference.py -m yolox\_s.onnx -i soccer.jpg -o outdir -s 0.3 --input\_shape 640,640

```



验证结果  

```text

(ort) «Ruyi yolox-venv» debian@revyos-lpi4a:\~/YOLOX/demo/ONNXRuntime$ python3 onnx\_inference.py -m yolox\_s.onnx -i soccer.jpg -o outdir -s 0.3 --input\_shape 640,640



2026-04-22 17:51:34.833501214 \[W:onnxruntime:, session\_state.cc:1136 VerifyEachNodeIsAssignedToAnEp] Some nodes were not assigned to the preferred execution providers which may or may not have an negative impact on performance. e.g. ORT explicitly assigns shape related ops to CPU to improve perf.



2026-04-22 17:51:34.833568883 \[W:onnxruntime:, session\_state.cc:1138 VerifyEachNodeIsAssignedToAnEp] Rerunning with verbose output on a non-minimal build will show node assignments.



(ort) «Ruyi yolox-venv» debian@revyos-lpi4a:\~/YOLOX/demo/ONNXRuntime$ ls outdir/

soccer.jpg

```

###### 

