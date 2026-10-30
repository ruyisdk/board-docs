---
sys: bianbu
sys_ver: 4.0.1
sys_var: Desktop
category: ai
last_update: 2026-10-29
model: Milk-V Jupiter2
profile: llama-server
---

# RuyiSDK 人工智能示例

可直接在开发板上进行编译和运行的示例，适合初学者快速上手。

安装依赖包

```

sudo apt update; sudo apt install -y wget tar zstd xz-utils git build-essential cmake curl jq ca-certificates iproute2

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

## llama-server

本文介绍如何使用 RuyiSDK 在 Milk-V Jupiter2 开发板上快速部署编译环境，并构建 llama-server 大语言模型服务，验证端侧 AI 推理与 API 调用功能

### 1. 准备工作

* **开发板**：Milk-V Jupiter2

* **其他**：USB Type-C 电源适配器（USB-PD 65W）或 ATX 2-pin 电源（12V 输入）、标准 HDMI 线缆、USB Type-C 拓展坞、USB Type-C 数据线、外接键盘、外接鼠标、USB 视频采集卡。

#### 操作系统安装与启动验证

确保您的开发板已准备好系统（本次测试使用出厂预装的 Bianbu 系统，未额外烧录）。

参考文档：https://milkv.io/zh/docs/jupiter2/getting-started/quick-start

### 2. 获取源码

#### 克隆源码

```bash

git clone --depth 1 --branch v0.1.8 https://github.com/spacemit-com/llama.cpp.git spacemit-llama.cpp

cd spacemit-llama.cpp

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

#### 编译 llama-server

```bash

cmake -B build-gcc \
  -DCMAKE_TOOLCHAIN_FILE="$RUYI_VENV/toolchain.cmake" \
  -DCMAKE_BUILD_TYPE=Release \
  -DGGML_NATIVE=OFF \
  -DGGML_CPU_RISCV64_SPACEMIT=OFF \
  -DGGML_CPU_REPACK=OFF \
  -DGGML_OPENMP=OFF \
  -DLLAMA_BUILD_UI=OFF \
  -DLLAMA_OPENSSL=OFF

cmake --build build-gcc --parallel 8 --target llama-server

```

#### 验证结果

检查生成的二进制文件：

```bash

file build-gcc/bin/llama-server

```

### 4.运行测试

#### 下载示例模型

```bash

mkdir -p "$HOME/.cache/models/llm"
MODEL_PATH="$HOME/.cache/models/llm/deepseek-r1-distill-qwen-1.5b-q4_0.gguf"
curl -fL https://archive.spacemit.com/spacemit-ai/model_zoo/llm/deepseek-r1-distill-qwen-1.5b-q4_0.gguf -o "${MODEL_PATH}.tmp" && mv "${MODEL_PATH}.tmp" "$MODEL_PATH"

```

#### 自动化启动与 API 验证

将以下完整脚本复制到终端运行。该脚本会自动启动 llama-server，检查端口占用，等待服务就绪，并验证健康检查、模型列表以及对话接口。

```bash

(
if ! command -v ss > /dev/null 2>&1; then
  echo "未找到 ss，请安装 iproute2"
  exit 1
fi

if ss -H -lnt 'sport = :8080' | grep -q .; then
  echo "8080 端口已被占用"
  exit 1
fi

SERVER_LOG="$PWD/llama-server-gcc.log"
build-gcc/bin/llama-server -m "$HOME/.cache/models/llm/deepseek-r1-distill-qwen-1.5b-q4_0.gguf" -a deepseek-r1-distill-qwen-1.5b -t 8 -c 2048 --host 127.0.0.1 --port 8080 > "$SERVER_LOG" 2>&1 &

SERVER_PID=$!

# 添加中断陷阱，确保脚本被 Ctrl+C 中断时能清理后台进程
trap 'kill "$SERVER_PID" 2>/dev/null; wait "$SERVER_PID" 2>/dev/null; exit 1' INT TERM EXIT

READY=0
for i in $(seq 1 120); do
  if ! kill -0 "$SERVER_PID" 2>/dev/null; then
    tail -n 80 "$SERVER_LOG"
    exit 1
  fi
  if curl --connect-timeout 1 --max-time 2 -fsS http://127.0.0.1:8080/health > /dev/null 2>&1; then
    READY=1
    break
  fi
  sleep 1
done

VALIDATION=0
if [ "$READY" -eq 1 ] &&
  curl --connect-timeout 1 --max-time 5 -fsS http://127.0.0.1:8080/health | jq -e '.status == "ok"' &&
  curl --connect-timeout 1 --max-time 5 -fsS http://127.0.0.1:8080/v1/models | jq -e '.data | length > 0' &&
  curl --connect-timeout 2 --max-time 30 -fsS http://127.0.0.1:8080/v1/chat/completions -H 'Content-Type: application/json' -d '{"model":"deepseek-r1-distill-qwen-1.5b","messages":[{"role":"user","content":"Hello"}],"max_tokens":16}' | jq -e '.choices | length > 0'; then
  VALIDATION=1
fi

# 正常结束时解除 trap 并手动清理
trap - INT TERM EXIT
kill "$SERVER_PID"
wait "$SERVER_PID" || true
test "$VALIDATION" -eq 1
)

```

正常情况下，终端会看到类似如下输出：

```text

true
true
true

```

再次启动服务:

```bash

build-gcc/bin/llama-server -m "$HOME/.cache/models/llm/deepseek-r1-distill-qwen-1.5b-q4_0.gguf" -a deepseek-r1-distill-qwen-1.5b -t 8 -c 2048 --host 127.0.0.1 --port 8080

```

打开另一个终端窗口，发送对话请求：

```bash

curl http://127.0.0.1:8080/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -d '{
    "model": "deepseek-r1-distill-qwen-1.5b",
    "messages": [
      {"role": "user", "content": "你好，请简单介绍一下你自己。"}
    ],
    "max_tokens": 128
  }' | jq
```

运行后，终端会输出类似以下的 JSON 返回数据：

```json

{
  "choices": [
    {
      "finish_reason": "stop",
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "\n\n您好！我是由中国的深度求索（DeepSeek）公司开发的智能助手DeepSeek-R1。我帮助用户解答问题，寻找新朋友等。有什么可以帮您的？"
      }
    }
  ],
  "created": 1793283328,
  "model": "deepseek-r1-distill-qwen-1.5b-q4_0.gguf",
  "object": "chat.completion",
  "usage": {
    "completion_tokens": 43,
    "prompt_tokens": 9,
    "total_tokens": 52
  },
  "timings": {
    "prompt_per_second": 8.883,
    "predicted_per_second": 7.937
  }
}

```
