---
sys: Bianbu
sys_ver: "4.0.7"
sys_var: null

category: ai
last_update: 2026-11-08

model: SpacemiT K3 Pico-ITX
profile: ResNet50
---

# RuyiSDK 人工智能示例

- 安装依赖包

  ```bash
  sudo apt update && sudo apt install -y \
    wget curl ca-certificates tar zstd xz-utils cmake \
    build-essential pkg-config opencv-spacemit spacemit-onnxruntime \
    libyaml-cpp-dev eigen-spacemit openblas-spacemit
  ```

- 安装 ruyi 包管理器

  已安装 ruyi 时可跳过。其他安装方式见 [RuyiSDK 官方安装文档](https://ruyisdk.org/docs/Package-Manager/installation/)。

  ```bash
  wget https://mirror.iscas.ac.cn/ruyisdk/ruyi/stable/latest/ruyi.riscv64
  chmod +x ./ruyi.riscv64
  sudo cp -v ./ruyi.riscv64 /usr/local/bin/ruyi
  ```

- 安装工具链

  ```bash
  ruyi update
  ruyi install gnu-ruyisdk
  ```

## SpacemiT K3 Pico-ITX ResNet50 图片分类

- #### 示例描述和硬件环境准备

  1. **示例功能**　使用 Ruyi GCC 编译 SpacemiT Vision 组件和 ResNet50 C++ 示例，对静态图片分类，在终端输出前五个类别及置信度。
  2. **硬件环境**　SpacemiT K3 Pico-ITX 开发板、可通过 SSH 连接开发板的 Windows 主机。
  3. **软件环境**　Bianbu 4.0.7（riscv64）、CMake 3.18 或更新版本。开发板使用 Bianbu 提供的 OpenCV、ONNX Runtime 和 SpaceMIT Execution Provider。

- #### 创建并激活 ruyi 虚拟环境

  ```bash
  mkdir -p ~/k3-resnet
  cd ~/k3-resnet

  ruyi venv -t gnu-ruyisdk manual resnet-env
  source resnet-env/bin/ruyi-activate
  riscv64-ruyisdk-linux-gnu-g++ --version
  ```

- #### 使用 ruyi 工具链编译示例代码

  1. **下载并传输厂商源码**

     在工作目录中克隆厂商 Vision 仓库。保留 `git rev-parse HEAD` 的输出，实测通过后用该提交号固定源码版本。

     ```powershell
     cd ~/k3-resnet
     git clone https://github.com/spacemit-com/model-zoo-vision.git
     cd model-zoo-vision
     ```

  2. **下载模型和测试图片**

     在 `model-zoo-vision` 根目录运行厂商脚本。

     ```bash
     bash examples/resnet/scripts/download_models.sh
     bash scripts/download_assets.sh
     ```

     默认模型为 `~/.cache/models/vision/resnet/resnet50.q.onnx`，默认图片为 `~/.cache/assets/image/005_kitten.jpg`。

  3. **使用 Ruyi GCC 编译**

     保持虚拟环境激活，在源码根目录执行。

     ```bash
     cd ~/k3-resnet/model-zoo-vision

     k3_lib_flags='-L/usr/lib/riscv64-linux-gnu -L/usr/lib'
     k3_link_dirs='/usr/lib/riscv64-linux-gnu:/usr/lib:/opt/opencv-spacemit/lib:/opt/openblas-spacemit/lib'

     cmake -S . -B build-ruyi-gcc \
       -DCMAKE_BUILD_TYPE=Release \
       -DCMAKE_CXX_COMPILER="$(command -v riscv64-ruyisdk-linux-gnu-g++)" \
       -Dyaml-cpp_DIR=/usr/lib/riscv64-linux-gnu/cmake/yaml-cpp \
       -DCMAKE_CXX_FLAGS='-idirafter /usr/include/riscv64-linux-gnu -idirafter /usr/include' \
       -DCMAKE_SHARED_LINKER_FLAGS="$k3_lib_flags" \
       -DCMAKE_EXE_LINKER_FLAGS="$k3_lib_flags -Wl,-rpath-link,$k3_link_dirs" \
       -DBUILD_EXAMPLES=ON \
       -DBUILD_TESTS=OFF \
       -DBUILD_PYTHON_BINDINGS=OFF \
       -DBUILD_PYTHON_WHEEL=OFF

     cmake --build build-ruyi-gcc --target resnet --parallel 4
     ```

     编译产物为 `build-ruyi-gcc/examples/resnet` 和 `build-ruyi-gcc/libvision.so`。

- #### 运行测试

  1. **运行默认图片分类**

     在源码根目录生成单线程 SpaceMIT EP 配置并运行。

     ```bash
     cd ~/k3-resnet/model-zoo-vision
     sed -E 's/^([[:space:]]*num_threads:).*/\1 1/' \
       examples/resnet/config/resnet50.yaml > build-ruyi-gcc/resnet50-ep1.yaml
     ./build-ruyi-gcc/examples/resnet build-ruyi-gcc/resnet50-ep1.yaml
     ```

     **输出结果**

     ```text
     Loading image: /home/old_king/.cache/assets/image/005_kitten.jpg
     SpaceMIT EP threads: 1
     SpaceMIT EP initialized: /home/old_king/.cache/models/vision/resnet/resnet50.q.onnx
     Top-5 classification results:
       1. tabby, tabby cat (confidence: 0.5056)
       2. tiger cat (confidence: 0.4416)
       3. Egyptian cat (confidence: 0.0443)
       4. lynx, catamount (confidence: 0.0013)
       5. tiger, Panthera tigris (confidence: 0.0010)
     ```

  2. **使用指定图片进行分类**

     将 `--image` 后的路径替换为开发板上的图片路径。

     ```bash
     ./build-ruyi-gcc/examples/resnet build-ruyi-gcc/resnet50-ep1.yaml \
       --image "$HOME/.cache/assets/image/007_dog.jpg"
     ```

     **输出结果**

     ```text
     Loading image: /home/old_king/.cache/assets/image/007_dog.jpg
     SpaceMIT EP threads: 1
     SpaceMIT EP initialized: /home/old_king/.cache/models/vision/resnet/resnet50.q.onnx
     Top-5 classification results:
       1. French bulldog (confidence: 0.5819)
       2. Boston bull, Boston terrier (confidence: 0.0668)
       3. Chihuahua (confidence: 0.0510)
       4. bucket, pail (confidence: 0.0389)
       5. pug, pug-dog (confidence: 0.0297)
     ```

- #### 退出环境

  ```bash
  cd ~
  ruyi-deactivate
  ```
