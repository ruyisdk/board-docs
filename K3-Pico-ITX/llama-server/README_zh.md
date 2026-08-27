---
sys: Bianbu
sys_ver: 4.0.4
sys_var: null

category: ai
last_update: 2026-08-28

model: SpacemiT K3 Pico-ITX
profile: llama-server
---

# RuyiSDK 人工智能示例
安装依赖包

```
sudo apt update; sudo apt install -y wget tar zstd xz-utils git build-essential cmake curl jq ca-certificates iproute2
```

安装ruyi包管理器

```
wget https://mirror.iscas.ac.cn/ruyisdk/ruyi/tags/0.51.0/ruyi-0.51.0.riscv64

chmod +x ./ruyi-0.51.0.riscv64

sudo cp -v ./ruyi-0.51.0.riscv64 /usr/local/bin/ruyi
```

安装GCC和LLVM工具链

```
ruyi update

ruyi install gnu-ruyisdk llvm-ruyisdk
```

## llama-server (GCC版)

创建并激活ruyi虚拟环境（GCC）
```
ruyi venv -t gnu-ruyisdk manual venv-gnu-ruyisdk-k3-pico-itx-llama

. venv-gnu-ruyisdk-k3-pico-itx-llama/bin/ruyi-activate
```

验证GCC版本

```
riscv64-ruyisdk-linux-gnu-gcc -v
```

编译并运行llama-server（GCC，以DeepSeek-R1-Distill-Qwen-1.5B Q4_0模型为例）

```
# 获取源码
git clone --depth 1 --branch v0.1.8 https://github.com/spacemit-com/llama.cpp.git spacemit-llama.cpp

cd spacemit-llama.cpp

# 配置并编译llama-server
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

# 下载示例模型
mkdir -p "$HOME/.cache/models/llm"

MODEL_PATH="$HOME/.cache/models/llm/deepseek-r1-distill-qwen-1.5b-q4_0.gguf"

curl -fL https://archive.spacemit.com/spacemit-ai/model_zoo/llm/deepseek-r1-distill-qwen-1.5b-q4_0.gguf -o "$MODEL_PATH"

# 检查端口并启动llama-server
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

build-gcc/bin/llama-server -m "$MODEL_PATH" -a deepseek-r1-distill-qwen-1.5b -t 8 -c 2048 --host 127.0.0.1 --port 8080 > "$SERVER_LOG" 2>&1 &

SERVER_PID=$!

# 等待服务就绪
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

# 验证API
VALIDATION=0
if [ "$READY" -eq 1 ] &&
  curl --connect-timeout 1 --max-time 5 -fsS http://127.0.0.1:8080/health | jq -e '.status == "ok"' &&
  curl --connect-timeout 1 --max-time 5 -fsS http://127.0.0.1:8080/v1/models | jq -e '.data | length > 0' &&
  curl --connect-timeout 2 --max-time 30 -fsS http://127.0.0.1:8080/v1/chat/completions -H 'Content-Type: application/json' -d '{"model":"deepseek-r1-distill-qwen-1.5b","messages":[{"role":"user","content":"Hello"}],"max_tokens":16}' | jq -e '.choices | length > 0'; then
  VALIDATION=1
fi

# 停止llama-server
kill "$SERVER_PID"

wait "$SERVER_PID" || true

test "$VALIDATION" -eq 1
)
```

正常情况下，终端会看到类似如下输出：

```
true
true
true
```

再次启动llama-server（GCC）

```
MODEL_PATH="$HOME/.cache/models/llm/deepseek-r1-distill-qwen-1.5b-q4_0.gguf"

build-gcc/bin/llama-server -m "$MODEL_PATH" -a deepseek-r1-distill-qwen-1.5b -t 8 -c 2048 --host 127.0.0.1 --port 8080
```

打开另一个终端，连接开发板并调用聊天接口

```
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

本次运行得到如下输出，模型生成内容仅用于验证接口调用：

```
sk3@k3pico:~$ curl http://127.0.0.1:8080/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -d '{
    "model": "deepseek-r1-distill-qwen-1.5b",
    "messages": [
      {"role": "user", "content": "你好，请简单介绍一下你自己。"}
    ],
    "max_tokens": 128
  }' | jq
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  1380  100  1202  100   178     77     11  00:16  00:15  00:01   219
{
  "choices": [
    {
      "finish_reason": "stop",
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "\n\n您好！我是由中国的深度求索（DeepSeek）公司开发的智能助手DeepSeek-R1。我擅长通过思考和分析来回答您的问题。我DeepSeek-R1由深度求索（DeepSeek Inc.）开发，专注于帮您找到更加高效、智能的解决方案。",
        "reasoning_content": "\n您好！我是由中国的深度求索（DeepSeek）公司开发的智能助手DeepSeek-R1。我擅长通过思考和分析来回答您的问题。我DeepSeek-R1由深度求索（DeepSeek Inc.）开发，专注于帮您找到更加高效、智能的解决方案。\n"
      }
    }
  ],
  "created": 1787857810,
  "model": "deepseek-r1-distill-qwen-1.5b",
  "system_fingerprint": "b1-754e371",
  "object": "chat.completion",
  "usage": {
    "completion_tokens": 127,
    "prompt_tokens": 9,
    "total_tokens": 136,
    "prompt_tokens_details": {
      "cached_tokens": 0
    }
  },
  "id": "chatcmpl-CEnlUCCxsyDHiDYX4mfRRTKsfrIKqu73",
  "timings": {
    "cache_n": 0,
    "prompt_n": 9,
    "prompt_ms": 865.131,
    "prompt_per_token_ms": 96.12566666666666,
    "prompt_per_second": 10.403048786831128,
    "predicted_n": 127,
    "predicted_ms": 14622.04,
    "predicted_per_token_ms": 115.13417322834647,
    "predicted_per_second": 8.685518573331764
  }
}
sk3@k3pico:~$
```

返回运行llama-server的终端，按`Ctrl+C`停止服务

返回上级目录并退出ruyi GCC虚拟环境

```
cd ..; ruyi-deactivate
```

## llama-server (LLVM版)

创建并激活ruyi虚拟环境（LLVM）

```
ruyi venv -t llvm-ruyisdk manual \
  --sysroot-from gnu-ruyisdk \
  venv-llvm-ruyisdk-k3-pico-itx-llama

. venv-llvm-ruyisdk-k3-pico-itx-llama/bin/ruyi-activate
```

验证LLVM版本

```
clang -v
```

编译并运行llama-server（LLVM）

```
# 进入源码目录
cd spacemit-llama.cpp

# 配置并编译llama-server
cmake -B build-llvm \
  -DCMAKE_TOOLCHAIN_FILE="$RUYI_VENV/toolchain.cmake" \
  -DCMAKE_BUILD_TYPE=Release \
  -DGGML_NATIVE=OFF \
  -DGGML_CPU_RISCV64_SPACEMIT=OFF \
  -DGGML_CPU_REPACK=OFF \
  -DGGML_OPENMP=OFF \
  -DLLAMA_BUILD_UI=OFF \
  -DLLAMA_OPENSSL=OFF

cmake --build build-llvm --parallel 8 --target llama-server

# 指定示例模型路径
MODEL_PATH="$HOME/.cache/models/llm/deepseek-r1-distill-qwen-1.5b-q4_0.gguf"

# 检查端口并启动llama-server
(
if ! command -v ss > /dev/null 2>&1; then
  echo "未找到 ss，请安装 iproute2"
  exit 1
fi

if ss -H -lnt 'sport = :8080' | grep -q .; then
  echo "8080 端口已被占用"
  exit 1
fi

SERVER_LOG="$PWD/llama-server-llvm.log"

build-llvm/bin/llama-server -m "$MODEL_PATH" -a deepseek-r1-distill-qwen-1.5b -t 8 -c 2048 --host 127.0.0.1 --port 8080 > "$SERVER_LOG" 2>&1 &

SERVER_PID=$!

# 等待服务就绪
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

# 验证API
VALIDATION=0
if [ "$READY" -eq 1 ] &&
  curl --connect-timeout 1 --max-time 5 -fsS http://127.0.0.1:8080/health | jq -e '.status == "ok"' &&
  curl --connect-timeout 1 --max-time 5 -fsS http://127.0.0.1:8080/v1/models | jq -e '.data | length > 0' &&
  curl --connect-timeout 2 --max-time 30 -fsS http://127.0.0.1:8080/v1/chat/completions -H 'Content-Type: application/json' -d '{"model":"deepseek-r1-distill-qwen-1.5b","messages":[{"role":"user","content":"Hello"}],"max_tokens":16}' | jq -e '.choices | length > 0'; then
  VALIDATION=1
fi

# 停止llama-server
kill "$SERVER_PID"

wait "$SERVER_PID" || true

test "$VALIDATION" -eq 1
)
```

正常情况下，终端会看到类似如下输出：

```
true
true
true
```

再次启动llama-server（LLVM）

```
MODEL_PATH="$HOME/.cache/models/llm/deepseek-r1-distill-qwen-1.5b-q4_0.gguf"

build-llvm/bin/llama-server -m "$MODEL_PATH" -a deepseek-r1-distill-qwen-1.5b -t 8 -c 2048 --host 127.0.0.1 --port 8080
```

打开另一个终端，连接开发板并调用聊天接口

```
curl http://127.0.0.1:8080/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -d '{
    "model": "deepseek-r1-distill-qwen-1.5b",
    "messages": [
      {"role": "user", "content": "你好，请简单介绍一下你自己。"}
    ],
    "max_tokens": 512
  }' | jq
```

本次运行得到如下输出，模型生成内容仅用于验证接口调用：

```
sk3@k3pico:~$ curl http://127.0.0.1:8080/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -d '{
    "model": "deepseek-r1-distill-qwen-1.5b",
    "messages": [
      {
        "role": "user",
        "content": "你好，请简单介绍一下你自己。"
      }
    ],
    "max_tokens": 512
  }' | jq
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  1399  100  1197  100   202     85     14  00:14  00:13  00:01   202
{
  "choices": [
    {
      "finish_reason": "stop",
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "\n\n您好！我是由中国的深度求索（DeepSeek）公司开发的智能助手DeepSeek-R1。我擅长通过思考来帮您解答复杂的数学，代码和逻辑推理等理工类问题。如果你有任何问题，我会尽力提供详细、准确的答案。",
        "reasoning_content": "\n您好！我是由中国的深度求索（DeepSeek）公司开发的智能助手DeepSeek-R1。我擅长通过思考来帮您解答复杂的数学，代码和逻辑推理等理工类问题。如果你有任何问题，我会尽力提供详细、准确的答案。\n"
      }
    }
  ],
  "created": 1787856964,
  "model": "deepseek-r1-distill-qwen-1.5b",
  "system_fingerprint": "b1-754e371",
  "object": "chat.completion",
  "usage": {
    "completion_tokens": 113,
    "prompt_tokens": 9,
    "total_tokens": 122,
    "prompt_tokens_details": {
      "cached_tokens": 3
    }
  },
  "id": "chatcmpl-B0Ze42pLpmJRq15EC1x5aLQhwMdTumHF",
  "timings": {
    "cache_n": 3,
    "prompt_n": 6,
    "prompt_ms": 587.301,
    "prompt_per_token_ms": 97.88350000000001,
    "prompt_per_second": 10.216226432442648,
    "predicted_n": 113,
    "predicted_ms": 13323.646,
    "predicted_per_token_ms": 117.90837168141593,
    "predicted_per_second": 8.481161988242556
  }
}
sk3@k3pico:~$
```

返回运行llama-server的终端，按`Ctrl+C`停止服务

返回上级目录并退出ruyi LLVM虚拟环境

```
cd ..; ruyi-deactivate
```
