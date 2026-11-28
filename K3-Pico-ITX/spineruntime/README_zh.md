---
sys: Bianbu
sys_ver: "4.0.7"
sys_var: null

category: system
last_update: 2026-11-22

model: SpacemiT K3 Pico-ITX
profile: SpineRuntime Quickstart
---

# RuyiSDK 多核任务执行示例

- **安装依赖包**

  在开发板终端执行。

  ```bash
  sudo apt update && sudo apt install -y \
    wget curl ca-certificates tar xz-utils zstd \
    build-essential file pkg-config spacemit-runtime
  ```

- **安装 RuyiSDK**

  已安装 ruyi 时可跳过。其他安装方式见 [RuyiSDK 官方安装指南](https://ruyisdk.org/docs/Package-Manager/installation/)。

  ```bash
  wget https://mirror.iscas.ac.cn/ruyisdk/ruyi/stable/latest/ruyi.riscv64
  chmod +x ./ruyi.riscv64
  sudo cp -v ./ruyi.riscv64 /usr/local/bin/ruyi
  ```

- **安装工具链**

  已安装 `gnu-ruyisdk` 时可直接创建虚拟环境。

  ```bash
  ruyi update
  ruyi install gnu-ruyisdk
  ```

## SpacemiT K3 Pico-ITX SpineRuntime Quickstart 验证

- #### 示例描述和硬件环境准备

  1. 使用 Ruyi GCC 编译厂商 C++17 示例，链接 Bianbu 提供的 `libspert`。
  2. 向 K3 A100 后端提交八个任务。每个任务写入其编号的平方，主机等待任务完成并逐项校验结果。
  3. 硬件为 SpacemiT K3 Pico-ITX 开发板。软件环境为 Bianbu 4.0.7（riscv64），运行时包使用 `spacemit-runtime`。本示例用于验证任务执行与同步。

- #### 创建并激活 ruyi 虚拟环境

  ```bash
  mkdir -p ~/k3-spine-runtime/logs
  cd ~/k3-spine-runtime
  set -o pipefail

  ruyi venv -t gnu-ruyisdk manual spine-env
  source spine-env/bin/ruyi-activate

  riscv64-ruyisdk-linux-gnu-g++ --version
  dpkg-query -W spacemit-runtime spacemit-tcm
  ```

- #### 使用 Ruyi 工具链编译 SpineRuntime Quickstart

  1. **下载厂商源码**

     在开发板上下载固定提交的源码包。[厂商源码提交](https://github.com/spacemit-com/spine-runtime/commit/574a70a5273ec7b85e15f5402c4aea769a8dd19c)

     ```bash
     spine_commit=574a70a5273ec7b85e15f5402c4aea769a8dd19c
     curl -fL -o spine-runtime-quickstart.tar.gz \
       "https://github.com/spacemit-com/spine-runtime/archive/$spine_commit.tar.gz"
     ```

     如果板端下载遇到 TLS 错误，在另开的 Windows PowerShell 下载并传输。将 `K3_USER@K3_IP` 替换为开发板的 SSH 登录信息。

     ```powershell
     curl.exe --http1.1 -fL --retry 3 --retry-all-errors -o spine-runtime-quickstart.tar.gz "https://codeload.github.com/spacemit-com/spine-runtime/tar.gz/574a70a5273ec7b85e15f5402c4aea769a8dd19c"
     scp spine-runtime-quickstart.tar.gz K3_USER@K3_IP:~/k3-spine-runtime/
     ```

  2. **提取示例并指定 K3 后端**

     回到开发板，从归档提取 Quickstart 源码。生成编译副本，显式选择 `spacemit-k3` 后端。[厂商后端说明](https://github.com/spacemit-com/spine-runtime/blob/574a70a5273ec7b85e15f5402c4aea769a8dd19c/docs/backends_ZH.md)

     ```bash
     cd ~/k3-spine-runtime
     spine_commit=574a70a5273ec7b85e15f5402c4aea769a8dd19c
     tar -xOf spine-runtime-quickstart.tar.gz \
       "spine-runtime-$spine_commit/examples/quickstart/demo.cpp" > demo.cpp

     sed 's/spert::Stream stream;/spert::Stream stream(spert::backend("spacemit-k3"));/' \
       demo.cpp > demo_k3.cpp
     grep -F 'spert::Stream stream(spert::backend("spacemit-k3"));' demo_k3.cpp
     ```

  3. **使用 Ruyi GCC 编译**

     将板端头文件目录放在 Ruyi GCC 默认搜索路径之后，并直接链接厂商库。

     ```bash
      test -r /usr/include/spert.hpp && test -r /usr/lib/libspert.so
     ```

     ```bash
      riscv64-ruyisdk-linux-gnu-g++ \
       -std=c++17 -O2 -Wall -Wextra \
       -march=rv64gc -mabi=lp64d \
       -idirafter /usr/include/riscv64-linux-gnu -idirafter /usr/include \
       demo_k3.cpp /usr/lib/libspert.so \
       -Wl,-rpath-link,/usr/lib/riscv64-linux-gnu:/usr/lib \
       -pthread -o spine_quickstart \
       2>&1 | tee logs/build.log
     echo "Build exit code: $?"
     ```

     **编译输出**

     ```text
      Build exit code: 0
     ```

     检查程序架构和动态库。

     ```bash
      file spine_quickstart
     ldd spine_quickstart
     ```

     板端实测生成了 64 位 RISC-V ELF。`ldd` 将 `libspert.so.1` 解析到 `/lib/libspert.so.1`，所有依赖均已找到。

- #### 运行测试

  **运行多核任务测试**

  ```bash
  ./spine_quickstart 2>&1 | tee logs/run.log
  echo "Run exit code: $?"
  ```

  **输出结果**

  ```text
  SpineRuntime quickstart passed on 8 core(s)
  Run exit code: 0
  ```

  本次运行在显式选择的 K3 后端取得了 8 个计算核，八个任务的平方结果均通过校验。其他进程占用计算核时，执行流取得的核心数可能变化。

- #### 退出环境

  ```bash
  cd ~
  ruyi-deactivate
  ```
