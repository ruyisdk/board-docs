---
sys: bianbu
sys_ver: 4.0.1
sys_var: Desktop
category: ai
last_update: 2026-11-19
model: Milk-V Jupiter2
profile: YOLOv8
---

# RuyiSDK 人工智能示例

可直接在开发板上进行编译和运行的示例，适合初学者快速上手。

安装依赖包

```

sudo apt update; sudo apt install -y git make build-essential cmake wget spacemit-tcm

```

> Bianbu 4.0.1 出厂镜像已预装 OpenCV 5.0.0（位于 /opt/opencv-spacemit，apt 包名 opencv-spacemit），
> 示例编译时通过 -DOpenCV_DIR 指定使用它；可用 `ls /opt/opencv-spacemit/lib/cmake/` 确认，
> 若提示目录不存在，执行 `sudo apt install -y opencv-spacemit`。

安装 ruyi 包管理器

```

wget https://mirror.iscas.ac.cn/ruyisdk/ruyi/stable/latest/ruyi.riscv64
chmod +x ruyi.riscv64
sudo cp -v ruyi.riscv64 /usr/local/bin/ruyi

```

安装工具链

```

ruyi update

ruyi install gnu-ruyisdk llvm-ruyisdk

```

## YOLOv8

本文介绍如何使用 RuyiSDK 在 Milk-V Jupiter2 开发板上快速部署编译环境，并构建 YOLOv8 目标检测应用，验证端侧 AI 推理功能。

### 1. 准备工作

* **开发板**：Milk-V Jupiter2

* **其他**：USB Type-C 电源适配器（USB-PD 65W）或 ATX 2-pin 电源（12V 输入）、标准 HDMI 线缆、USB Type-C 拓展坞、USB Type-C 数据线、外接键盘、外接鼠标、USB 视频采集卡。

#### 操作系统安装与启动验证

确保您的开发板已准备好系统（本次测试使用出厂预装的 Bianbu 系统，未额外烧录）。

参考文档：https://milkv.io/zh/docs/jupiter2/getting-started/quick-start

### 2. 获取源码

#### 克隆源码

```bash
mkdir -p "$HOME/workspace" && cd "$HOME/workspace"

git clone https://gitee.com/bianbu/spacemit-demo.git
cd spacemit-demo/examples/CV/yolov8
```

#### 下载模型和测试数据

```bash
cd model
wget -O yolov8n.q.onnx.tmp https://archive.spacemit.com/spacemit-ai/BRDK/Model_Zoo/CV/YOLOv8/K3/yolov8n.q.onnx && \
mv yolov8n.q.onnx.tmp yolov8n.q.onnx
cd ..

cd data
sh download_data.sh
cd ..
```

#### 下载 SpacemiT ONNX Runtime 推理引擎

```bash
mkdir -p "$HOME/code/test_lib" && cd "$HOME/code/test_lib"
wget https://archive.spacemit.com/spacemit-ai/onnxruntime/spacemit-ort.riscv64.2.0.2.tar.gz -O spacemit-ort.riscv64.2.0.2.tar.gz.tmp && \
mv spacemit-ort.riscv64.2.0.2.tar.gz.tmp spacemit-ort.riscv64.2.0.2.tar.gz && \
tar -xzf spacemit-ort.riscv64.2.0.2.tar.gz
```

### 3. 编译应用与验证

#### 创建虚拟环境

```bash
cd "$HOME"

ruyi venv -t gnu-ruyisdk manual venv-gnu-ruyisdk-jupiter2
. venv-gnu-ruyisdk-jupiter2/bin/ruyi-activate
```

#### 验证工具链版本

```bash
riscv64-ruyisdk-linux-gnu-gcc -v
```

#### 源码修改与配置

```bash
cd "$HOME/workspace/spacemit-demo/examples/CV/yolov8/cpp"

python3 - <<'PY'
import os, re

p = 'CMakeLists.txt'
s = open(p, encoding='utf-8').read()
s = re.sub(r'find_package\s*\(\s*OpenCV[^)]*\)',
           'find_package(OpenCV REQUIRED COMPONENTS core imgproc imgcodecs)', s, count=1)

home = os.path.expanduser('~')
# 动态检测 SDK 版本
if os.path.isdir(home + '/code/test_lib/spacemit-ort.riscv64.2.0.2'):
    ver = '2.0.2'
elif os.path.isdir(home + '/code/test_lib/spacemit-ort.riscv64.2.0.1'):
    ver = '2.0.1'
else:
    print("Error: 未找到 SpacemiT ONNX Runtime SDK，请检查 ~/code/test_lib 目录。")
    exit(1)

s = re.sub(r'spacemit-ort\.riscv64\.2\.0\.\d', 'spacemit-ort.riscv64.' + ver, s)
open(p, 'w', encoding='utf-8').write(s)

print('SDK       :', ver)
print('OpenCV 行 :', [l.strip() for l in s.splitlines() if 'find_package(OpenCV' in l])

cc = 'yolov8.cc'
s_cc = open(cc, encoding='utf-8').read()
new = '''    // 不依赖 opencv_dnn：手动做 BGR->RGB、归一化、HWC->CHW
    cv::Mat rgb;
    cv::cvtColor(processed_image, rgb, cv::COLOR_BGR2RGB);
    cv::Mat blob(1, 3 * inputHeight * inputWidth, CV_32F);
    float* dst = blob.ptr<float>();
    for (int y = 0; y < inputHeight; ++y) {
        const cv::Vec3b* row = rgb.ptr<cv::Vec3b>(y);
        for (int x = 0; x < inputWidth; ++x) {
            dst[(0 * inputHeight + y) * inputWidth + x] = row[x][0] / 255.0f;
            dst[(1 * inputHeight + y) * inputWidth + x] = row[x][1] / 255.0f;
            dst[(2 * inputHeight + y) * inputWidth + x] = row[x][2] / 255.0f;
        }
    }
    return blob;
'''
pat = re.compile(r'return cv::dnn::blobFromImage\(.*?\);', re.S)
if pat.search(s_cc):
    open(cc, 'w', encoding='utf-8').write(pat.sub(new, s_cc, count=1))
    print('yolov8.cc : patched')
else:
    print('yolov8.cc : 已是修改后的版本')
PY
```

上面脚本应打印出：

```text
SDK       : 2.0.2
OpenCV 行 : ['find_package(OpenCV REQUIRED COMPONENTS core imgproc imgcodecs)']
yolov8.cc : patched
```

#### 编译 YOLOv8

```bash
cd "$HOME/workspace/spacemit-demo/examples/CV/yolov8/cpp"
rm -rf build && mkdir -p build && cd build

CV_DIR=$(ls -d /opt/opencv-spacemit/lib/cmake/opencv* | head -n1)
echo "OpenCV_DIR=$CV_DIR"

cmake .. \
  -DOpenCV_DIR="$CV_DIR" \
  -DCMAKE_C_COMPILER=riscv64-ruyisdk-linux-gnu-gcc \
  -DCMAKE_CXX_COMPILER=riscv64-ruyisdk-linux-gnu-g++ \
  -DCMAKE_DISABLE_FIND_PACKAGE_OpenCL=ON \
  -DCMAKE_EXE_LINKER_FLAGS="-Wl,--allow-shlib-undefined -Wl,-rpath-link,/opt/opencv-spacemit/lib -Wl,-rpath-link,/usr/lib/riscv64-linux-gnu"

make -j8
```

#### 验证结果

检查生成的二进制文件：

```bash
file yolov8_demo
```

### 4. 运行测试

#### 执行推理

```bash
cd "$HOME/workspace/spacemit-demo/examples/CV/yolov8/cpp/build"

ORT_LIB_PATH=$(ls -d "$HOME"/code/test_lib/spacemit-ort.riscv64.2.0.* 2>/dev/null | head -n1)
export LD_LIBRARY_PATH="/opt/opencv-spacemit/lib:$ORT_LIB_PATH/lib:$LD_LIBRARY_PATH"

./yolov8_demo --model ../../model/yolov8n.q.onnx --image ../../data/test.jpg
```

正常情况下，终端会看到如下输出：

```text
Result image saved as result.jpg
```

同目录下生成的 result.jpg 即为带检测框的最终结果图。

#### NPU 性能压测

```bash
cd "$HOME/workspace/spacemit-demo/examples/CV/yolov8/cpp/build"

ORT_PATH=$(ls -d "$HOME"/code/test_lib/spacemit-ort.riscv64.2.0.* 2>/dev/null | head -n1)
export LD_LIBRARY_PATH="$ORT_PATH/lib:$LD_LIBRARY_PATH"

"$ORT_PATH/bin/onnxruntime_perf_test" \
  ../../model/yolov8n.q.onnx -e spacemit -r 20 -x 4 -c 1 -S 1 -I \
  -i "SPACEMIT_EP_INTRA_THREAD_NUM|4"
```

终端会输出类似以下的数据：

```text
Using SpaceMITExecutionProvider
setting SPACEMIT_EP_INTRA_THREAD_NUM : 4
Setting intra_op_num_threads to 4
Session creation time cost: 0.471298 s
First inference time cost: 67 ms
Total inference time cost: 0.322035 s
Total inference requests: 20
Average inference time cost total: 16.101773 ms
Total inference run time: 0.322114 s
Number of inferences per second: 62.0897
Avg CPU usage: 59 %
Peak working set size: 67096576 bytes
```
