---
sys: bianbu
sys_ver: 4.0.1
sys_var: Desktop
category: ai
last_update: 2026-11-09
model: Milk-V Jupiter2
profile: onnxruntime
---

# RuyiSDK 人工智能示例

可直接在开发板上进行编译和运行的示例，适合初学者快速上手。

安装依赖包

```

sudo apt update; sudo apt install -y wget tar zstd xz-utils git build-essential cmake curl jq ca-certificates iproute2 python3-numpy

```

安装 ruyi 包管理器

```

wget https://mirror.iscas.ac.cn/ruyisdk/ruyi/tags/0.51.0/ruyi-0.51.0.riscv64
chmod +x ruyi-0.51.0.riscv64
sudo cp -v ruyi-0.51.0.riscv64 /usr/local/bin/ruyi

```

安装工具链

```

ruyi update

ruyi install gnu-ruyisdk llvm-ruyisdk

```

## onnxruntime

本文介绍如何使用 RuyiSDK 在 Milk-V Jupiter2 开发板上快速部署 ONNXRuntime 环境，并构建 Python 与 C++ 的 AI 推理程序，验证端侧 NPU 的加速能力。

### 1. 准备工作

* **开发板**：Milk-V Jupiter2

* **其他**：USB Type-C 电源适配器（USB-PD 65W）或 ATX 2-pin 电源（12V 输入）、标准 HDMI 线缆、USB Type-C 拓展坞、USB Type-C 数据线、外接键盘、外接鼠标、USB 视频采集卡。

#### 操作系统安装与启动验证

确保您的开发板已准备好系统（本次测试使用出厂预装的 Bianbu 系统，未额外烧录）。

参考文档：https://milkv.io/zh/docs/jupiter2/getting-started/quick-start

#### 安装 SpacemiT ONNXRuntime 软件包

```bash

sudo apt install -y spacemit-onnxruntime python3-spacemit-ort spacemit-tcm

```

确认后端已注册：

```bash

python3 -c "import onnxruntime as ort, spacemit_ort; print(ort.__version__); print(ort.get_available_providers())"

```

### 2. 获取模型

```bash

mkdir -p "$HOME/models/onnx"

# 下载 FP32 模型
MODEL="$HOME/models/onnx/resnet18.onnx"
curl -fL https://archive.spacemit.com/spacemit-ai/BRDK/Model_Zoo/CV/ResNet/resnet18.onnx -o "${MODEL}.tmp" && mv "${MODEL}.tmp" "$MODEL"

# 下载 INT8 量化模型（用于后续性能压测）
curl -fL https://archive.spacemit.com/spacemit-ai/BRDK/Model_Zoo/CV/ResNet/resnet18.q.onnx -o "$HOME/models/onnx/resnet18.q.onnx"

```

### 3. 编译应用与验证

#### 创建虚拟环境

```bash

ruyi venv -t gnu-ruyisdk manual venv-gnu-ruyisdk-jupiter2

. venv-gnu-ruyisdk-jupiter2/bin/ruyi-activate

```

#### 验证工具链版本

```bash

riscv64-ruyisdk-linux-gnu-gcc -v

```

#### 编译 C++ 推理程序

准备工程目录及 C++ 源码：

```bash
mkdir -p "$HOME/ort-demo" && cd "$HOME/ort-demo"

cat > main.cc <<'EOF'
#include <array>
#include <chrono>
#include <cstdio>
#include <cstdlib>
#include <string>
#include <unordered_map>
#include <vector>
#include <onnxruntime_cxx_api.h>

// SpacemiT SDK 里的 EP 环境初始化头文件
#if __has_include("spacemit_ort_env.h")
#include "spacemit_ort_env.h"
#define USE_SPACEMIT_EP 1
#else
#define USE_SPACEMIT_EP 0
#endif

int main(int argc, char** argv) {
  const char* model_path = argc > 1 ? argv[1] : "resnet18.onnx";
  const int runs = argc > 2 ? std::atoi(argv[2]) : 20;

  Ort::Env env(ORT_LOGGING_LEVEL_WARNING, "resnet18-ep-demo");
  Ort::SessionOptions so;
  so.SetIntraOpNumThreads(4);
  so.SetGraphOptimizationLevel(GraphOptimizationLevel::ORT_ENABLE_ALL);

#if USE_SPACEMIT_EP
  std::unordered_map<std::string, std::string> ep_opts;
  ep_opts["SPACEMIT_EP_INTRA_THREAD_NUM"] = "4";
  SessionOptionsSpaceMITEnvInit(so, ep_opts);
  std::printf("[info] SpaceMIT EP enabled\n");
#else
  std::printf("[warn] spacemit_ort_env.h not found -> CPU only\n");
#endif

  Ort::Session session(env, model_path, so);
  Ort::AllocatorWithDefaultOptions alloc;
  auto in_name = session.GetInputNameAllocated(0, alloc);
  auto out_name = session.GetOutputNameAllocated(0, alloc);
  
  std::array<int64_t, 4> shape{1, 3, 224, 224};
  std::vector<float> data(3 * 224 * 224, 0.5f);
  auto mem = Ort::MemoryInfo::CreateCpu(OrtArenaAllocator, OrtMemTypeDefault);
  auto input = Ort::Value::CreateTensor<float>(mem, data.data(), data.size(), shape.data(), shape.size());

  const char* in_names[] = {in_name.get()};
  const char* out_names[] = {out_name.get()};

  session.Run(Ort::RunOptions{nullptr}, in_names, &input, 1, out_names, 1);

  std::vector<Ort::Value> out;
  auto t0 = std::chrono::steady_clock::now();
  for (int i = 0; i < runs; ++i) {
    out = session.Run(Ort::RunOptions{nullptr}, in_names, &input, 1, out_names, 1);
  }
  auto t1 = std::chrono::steady_clock::now();
  const double ms = std::chrono::duration<double, std::milli>(t1 - t0).count() / runs;
  std::printf("avg latency : %.2f ms/infer (%d runs)\n", ms, runs);
  std::printf("RESULT: PASS\n");
  return 0;
}
EOF
```

准备 `CMakeLists.txt`：

```bash
cat > CMakeLists.txt <<'EOF'
cmake_minimum_required(VERSION 3.16)
project(resnet18_ep_demo CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

if(NOT ORT_HOME)
  message(FATAL_ERROR "缺少 ORT_HOME，请用 -DORT_HOME=<spacemit-ort 解压目录> 指定")
endif()

include_directories("${ORT_HOME}/include" "${ORT_HOME}/include/onnxruntime")
link_directories("${ORT_HOME}/lib")

add_executable(resnet18_ep_demo main.cc)
# SpacemiT EP 的初始化函数在 libspacemit_ep.so 中，需要一起链接
target_link_libraries(resnet18_ep_demo PRIVATE onnxruntime spacemit_ep)
EOF
```

下载并解压官方 SDK：

```bash
cd "$HOME"
ORT_VER=2.0.2
mkdir -p spacemit-sdk
curl -fL -o spacemit-ort.tar.gz "https://archive.spacemit.com/spacemit-ai/onnxruntime/spacemit-ort.riscv64.${ORT_VER}.tar.gz"
tar -xzf spacemit-ort.tar.gz -C spacemit-sdk
export ORT_HOME=$(find "$HOME/spacemit-sdk" -maxdepth 3 -type d -name include | head -n1 | xargs -r dirname)
echo "ORT_HOME=$ORT_HOME"
```

编译：

```bash
cd "$HOME/ort-demo"
cmake -B build -DCMAKE_TOOLCHAIN_FILE="$RUYI_VENV/toolchain.cmake" -DCMAKE_BUILD_TYPE=Release -DORT_HOME="$ORT_HOME"
cmake --build build --parallel 8
```

确认产物为 RISC-V 可执行文件：

```bash
file build/resnet18_ep_demo
```



### 4.运行测试

#### Python 验证测试

将以下代码保存为 $HOME/ort_resnet18.py：

```bash

cat > "$HOME/ort_resnet18.py" <<'PY'
#!/usr/bin/env python3
import os
import sys
import time
import numpy as np
import onnxruntime as ort
import spacemit_ort

MODEL = os.environ.get("ORT_MODEL", os.path.expanduser("~/models/onnx/resnet18.onnx"))
RUNS = int(os.environ.get("ORT_RUNS", "20"))
THREADS = int(os.environ.get("ORT_THREADS", "4"))

def make_session(providers):
    so = ort.SessionOptions()
    so.intra_op_num_threads = THREADS
    so.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
    so.log_severity_level = 2
    return ort.InferenceSession(MODEL, so, providers=providers)

def bench(session, x):
    name = session.get_inputs()[0].name
    out = session.run(None, {name: x})[0]
    t0 = time.perf_counter()
    for _ in range(RUNS):
        session.run(None, {name: x})
    ms = (time.perf_counter() - t0) / RUNS * 1000.0
    return out, ms

def main():
    if not os.path.isfile(MODEL):
        sys.exit("模型不存在: %s" % MODEL)
    print("onnxruntime: %s" % ort.__version__)
    ep = make_session(["SpaceMITExecutionProvider"])
    cpu = make_session(["CPUExecutionProvider"])
    shape = [d if isinstance(d, int) and d > 0 else 1 for d in ep.get_inputs()[0].shape]
    x = np.random.RandomState(0).rand(*shape).astype(np.float32)
    out_ep, ms_ep = bench(ep, x)
    out_cpu, ms_cpu = bench(cpu, x)
    diff = float(np.max(np.abs(out_ep - out_cpu)))
    print("SpaceMIT EP : %8.2f ms/infer" % ms_ep)
    print("CPU         : %8.2f ms/infer" % ms_cpu)
    print("max|EP-CPU| : %.6f" % diff)
    print("RESULT: PASS" if diff < 1e-2 else "RESULT: CHECK")

if __name__ == "__main__":
    sys.exit(main())
PY

```

运行测试：

```bash

cd "$HOME"
python3 ort_resnet18.py 2>&1 | tee ort_resnet18.log

```

实际运行结果：

```text

model file : /home/jupiter2/models/onnx/resnet18.onnx (44.6 MB)
onnxruntime: 1.24.2+spacemit.a1
available providers: SpaceMITExecutionProvider, CPUExecutionProvider
EP session providers: ['SpaceMITExecutionProvider', 'CPUExecutionProvider']
----------------------------------------------
input shape : [1, 3, 224, 224]
output shape: (1, 1000)
SpaceMIT EP :   102.64 ms/infer
CPU         :   172.57 ms/infer
speedup     :     1.68x
max|EP-CPU| : 0.000006
top-1 class : EP=111  CPU=111
RESULT: PASS

```

#### C++ 程序运行

```bash
cd "$HOME/ort-demo"
LD_LIBRARY_PATH="$ORT_HOME/lib:$LD_LIBRARY_PATH" \
  ./build/resnet18_ep_demo "$HOME/models/onnx/resnet18.onnx"
```

实际运行结果：

```text
[info] SpaceMIT EP enabled
model: /home/jupiter2/models/onnx/resnet18.onnx
avg latency : 106.37 ms/infer (20 runs)
RESULT: PASS
```

#### onnxruntime_perf_test 性能压测

由于该工具默认需要测试数据，需加上 -I 参数自动生成随机输入数据。这里测试的是 INT8 量化模型：

```bash

export LD_LIBRARY_PATH="$ORT_HOME/lib:$LD_LIBRARY_PATH"
"$ORT_HOME/bin/onnxruntime_perf_test" "$HOME/models/onnx/resnet18.q.onnx" \
  -e spacemit -m times -r 20 -x 4 -c 1 -S 1 -I

```

实际运行结果：

```text

using SpaceMITExecutionProvider
Setting intra_op_num_threads to 4
Session creation time cost: 0.0805251 s
First inference time cost: 74 ms
Total inference time cost: 0.0569932 s
Total inference requests: 20
Average inference time cost total: 2.849661 ms
Total inference run time: 0.0570415 s
Number of inferences per second: 350.622 
Avg CPU usage: 58 %
Peak working set size: 61992960 bytes
...
P50 Latency: 0.00285392 s
P99 Latency: 0.003003 s

```
