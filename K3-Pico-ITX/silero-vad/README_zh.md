---
sys: Bianbu
sys_ver: "4.0.7"
sys_var: null

category: ai
last_update: 2026-11-15

model: SpacemiT K3 Pico-ITX
profile: Silero VAD Simple Demo
---

# RuyiSDK 语音活动检测示例

- **安装依赖包**

  在 K3 开发板终端执行。

  ```bash
  sudo apt update && sudo apt install -y \
    wget curl ca-certificates tar xz-utils zstd \
    build-essential cmake file pkg-config \
    libcurl4-openssl-dev spacemit-onnxruntime
  ```

- **安装 RuyiSDK**

  已安装 ruyi 时可跳过。其他安装方式见 [RuyiSDK 官方安装指南](https://ruyisdk.org/docs/Package-Manager/installation/)。

  ```bash
  wget https://mirror.iscas.ac.cn/ruyisdk/ruyi/stable/latest/ruyi.riscv64
  chmod +x ./ruyi.riscv64
  sudo cp -v ./ruyi.riscv64 /usr/local/bin/ruyi
  ```

- **安装工具链**

  ```bash
  ruyi update
  ruyi install gnu-ruyisdk
  ```

## SpacemiT K3 Pico-ITX Silero VAD Simple Demo 验证

- #### 示例描述和硬件环境准备

  1. 使用 Ruyi GCC 编译厂商 VAD 组件和 `vad_simple_demo`，链接 Bianbu 提供的 ONNX Runtime 及 libcurl。
  2. 示例在程序内生成七帧 16 kHz 合成音频，每帧 512 个采样点，输出检测概率、状态、耗时和实时率 RTF。
  3. 开发板为 SpacemiT K3 Pico-ITX，运行 Bianbu 4.0.7（riscv64）。本例使用 CPU 推理，无需麦克风、音频文件或 Python 绑定。[厂商 VAD 组件](https://github.com/spacemit-com/model-zoo-vad/tree/4124a85a8efe8c3047aef5cad621b8c208c4723b)

- #### 创建并激活 ruyi 虚拟环境

  ```bash
  mkdir -p ~/k3-silero-vad/logs
  cd ~/k3-silero-vad
  set -o pipefail

  ruyi venv -t gnu-ruyisdk manual vad-env
  source vad-env/bin/ruyi-activate
  riscv64-ruyisdk-linux-gnu-g++ --version
  dpkg-query -W spacemit-onnxruntime libcurl4-openssl-dev
  ```

- #### 使用 Ruyi 工具链编译 Silero VAD Simple Demo

  1. **下载厂商源码**

     ```bash
     vad_commit=4124a85a8efe8c3047aef5cad621b8c208c4723b
     curl -fL -o model-zoo-vad.tar.gz \
       "https://github.com/spacemit-com/model-zoo-vad/archive/$vad_commit.tar.gz"
     ```

     如果板端下载遇到 TLS 错误，在 Windows PowerShell 下载并传输。将 `K3_USER@K3_IP` 替换为开发板的 SSH 登录信息。

     ```powershell
     curl.exe --http1.1 -fL --connect-timeout 10 -o model-zoo-vad.tar.gz "https://codeload.github.com/spacemit-com/model-zoo-vad/tar.gz/4124a85a8efe8c3047aef5cad621b8c208c4723b"
     scp model-zoo-vad.tar.gz K3_USER@K3_IP:~/k3-silero-vad/
     ```

     回到开发板解压。

     ```bash
     cd ~/k3-silero-vad
     mkdir -p model-zoo-vad
     tar -xzf model-zoo-vad.tar.gz -C model-zoo-vad --strip-components=1
     cd model-zoo-vad
     ```

  2. **下载 Silero VAD 模型**

     ```bash
     vad_model_dir="$HOME/.cache/models/vad/silero"
     vad_model_sha=2623a2953f6ff3d2c1e61740c6cdb7168133479b267dfef114a4a3cc5bdd788f
     mkdir -p "$vad_model_dir"

     curl -fL -o "$vad_model_dir/silero_vad.onnx.part" \
       https://archive.spacemit.com/spacemit-ai/model_zoo/vad/silero/silero_vad.onnx &&
     printf '%s  %s\n' "$vad_model_sha" "$vad_model_dir/silero_vad.onnx.part" | sha256sum -c - &&
     mv "$vad_model_dir/silero_vad.onnx.part" "$vad_model_dir/silero_vad.onnx"
     ```

  3. **使用 Ruyi GCC 配置和编译**

     在源码根目录执行。将 ONNX Runtime 的公开头文件引入独立目录，并用板端 `pkg-config` 查询 libcurl 的链接目录。

     ```bash
     mkdir -p ruyi-ort-headers
     for header in /usr/include/onnxruntime*.h; do
       ln -sfn "$header" ruyi-ort-headers/
     done

     ls -l ruyi-ort-headers/onnxruntime_cxx_api.h /usr/lib/libonnxruntime.so
     vad_curl_libdir=$(pkg-config --variable=libdir libcurl)
     printf 'libcurl libdir: %s\n' "$vad_curl_libdir"
     ```

     确认两项文件可读且 libcurl 目录有值，再配置。

     ```bash
     cmake -S . -B build-ruyi-gcc \
       -DCMAKE_BUILD_TYPE=Release \
       -DCMAKE_C_COMPILER="$(command -v riscv64-ruyisdk-linux-gnu-gcc)" \
       -DCMAKE_CXX_COMPILER="$(command -v riscv64-ruyisdk-linux-gnu-g++)" \
       -DONNXRUNTIME_INCLUDE_DIR="$PWD/ruyi-ort-headers" \
       -DONNXRUNTIME_LIB=/usr/lib/libonnxruntime.so \
       -DCMAKE_CXX_FLAGS='-idirafter /usr/include/riscv64-linux-gnu -idirafter /usr/include' \
       -DCMAKE_EXE_LINKER_FLAGS="-L$vad_curl_libdir -Wl,-rpath-link,$vad_curl_libdir:/usr/lib/riscv64-linux-gnu:/usr/lib" \
       -DBUILD_VAD_EXAMPLES=ON \
       -DBUILD_VAD_PYTHON=OFF \
       -DBUILD_STREAM_DEMO=OFF \
       2>&1 | tee ../logs/configure.log
     ```

     确认出现 `Configuring done` 和 `Generating done` 后编译。

     ```bash
     cmake --build build-ruyi-gcc --target vad_simple_demo --parallel 4 \
       2>&1 | tee ../logs/build.log
     echo "Build exit code: $?"
     ```

     检查程序架构和动态库。

     ```bash
     file build-ruyi-gcc/bin/vad_simple_demo
     ldd build-ruyi-gcc/bin/vad_simple_demo
     ```

- #### 运行示例并验证结果

  1. **运行 VAD Simple Demo**

     ```bash
     ./build-ruyi-gcc/bin/vad_simple_demo 2>&1 | tee ../logs/run.log
     echo "Run exit code: $?"
     ```

     **输出结果**

     ```text
     === VAD Simple Demo ===
     VAD Engine initialized: Silero VAD

     Processing test audio frames:
     -----------------------------
     Frame duration: 32.00 ms
     Frame 0 (Silence): prob=0.02, state=0, processing=1.424 ms, RTF=0.0445
     Frame 1 (Silence): prob=0.0073, state=0, processing=0.787 ms, RTF=0.0246
     Frame 2 (Speech): prob=0.4544, state=0, processing=0.760 ms, RTF=0.0238
     Frame 3 (Speech): prob=0.1777, state=0, processing=0.750 ms, RTF=0.0234
     Frame 4 (Speech): prob=0.0949, state=0, processing=0.750 ms, RTF=0.0234
     Frame 5 (Silence): prob=0.0199, state=0, processing=0.750 ms, RTF=0.0234
     Frame 6 (Silence): prob=0.0211, state=0, processing=0.750 ms, RTF=0.0234

     Performance summary:
       Frames: 7
       Total audio: 224.00 ms
       Total processing: 5.970 ms
       Avg processing/frame: 0.853 ms
       Avg RTF: 0.0267

     === Demo Complete ===
     Run exit code: 0
     ```

     七帧均处理成功。标为 `Speech` 的三帧使用 440 Hz 正弦波，最高检测概率为 `0.4544`。

  2. **退出 Ruyi 虚拟环境**

     ```bash
     cd ~
     ruyi-deactivate
     ```
