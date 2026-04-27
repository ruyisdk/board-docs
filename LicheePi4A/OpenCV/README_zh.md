---
sys: Debian
sys_ver: 12 (Bookworm)
sys_var: 
provider: PLCT/Sipeed
status: Supported
last_update: 2026-04-21

model: LicheePi 4A
profile: sipeed-lpi4a-opencv

---

#  RuyiSDK 计算机视觉示例

- **安装依赖包**

  ```bash
  sudo apt update
  sudo apt install -y git cmake libprotobuf-dev protobuf-compiler libvulkan-dev libopencv-dev
  ```

- **安装 RuyiSDK**
  根据 [RuyiSDK 官方安装指南](https://ruyisdk.org/docs/Package-Manager/installation)，在开发板上完成 Ruyi 包管理器本身的安装部署

- **安装工具链**

  ```bash
  ruyi update
  ruyi install gnu-plct-xthead
  ```


## LicheePi 4A Dhrystone 基准测试

- #### 示例描述和硬件环境准备

1. 示例功能：基于 OpenCV 实现图像读取、窗口显示，验证 RuyiGCC 在 LicheePi 4A 上的 OpenCV 编译与运行能力。
2. 硬件环境：LicheePi 4A 开发板（TH1520 芯片）
3. 软件环境：Debian/openEuler for RISC-V 系统，已联网可正常访问外部仓库

- #### 创建并激活 ruyi 虚拟环境

  ```bash
  # 创建虚拟环境：指定工具链+目标开发板+环境名称
  ruyi venv -t gnu-plct-xthead sipeed-lpi4a opencv-env
  
  # 激活虚拟环境
  source opencv-env/bin/ruyi-activate
  ```

- #### 使用 ruyi 工具链编译示例代码

  1. **获取 OpenCV 官方源码**

     ```bash
     git clone https://github.com/opencv/opencv.git
     cd opencv
     git checkout 4.9.0
     ```

  2. **CMake配置与编译**

     ```bash
     # 创建独立的编译目录
     mkdir build && cd build
     
     # CMake配置
     cmake -DCMAKE_BUILD_TYPE=Release \
           -DCMAKE_C_COMPILER=riscv64-plctxthead-linux-gnu-gcc \
           -DCMAKE_CXX_COMPILER=riscv64-plctxthead-linux-gnu-g++ \
           -DOPENCV_GENERATE_PKGCONFIG=ON \
           -DCMAKE_INSTALL_PREFIX=./install \
           -DWITH_GTK=ON \
           ..
     
     make -j$(nproc)
     make install
     ```

  3. **环境变量配置**

     ```bash
     cd install
     export OPENCV_HOME=$(pwd)
     
     nano ~/.bashrc
     ```

     在文本编辑器中，用方向键滚到文件最末尾，把下面的内容粘贴进`bashrc`:

     ```c#
     # OpenCV 环境变量配置
     export OPENCV_HOME=$HOME/opencv/build/install
     
     if [ -d "$OPENCV_HOME/lib64" ]; then
         export PKG_CONFIG_PATH=$OPENCV_HOME/lib64/pkgconfig:$PKG_CONFIG_PATH
         export LD_LIBRARY_PATH=$OPENCV_HOME/lib64:$LD_LIBRARY_PATH
     else
         export PKG_CONFIG_PATH=$OPENCV_HOME/lib/pkgconfig:$PKG_CONFIG_PATH
         export LD_LIBRARY_PATH=$OPENCV_HOME/lib:$LD_LIBRARY_PATH
     fi
     ```

  4. **立即生效并验证**

     ```c#
     source ~/.bashrc
     pkg-config --modversion opencv4
     ```

     **输出结果**

     ```bash
     Â«Ruyi opencv-envÂ» debian@revyos-lpi4a:~/opencv/build/installsource ~/.bashrcrc
     debian@revyos-lpi4a:~/opencv/build/install$ pkg-config --modversion opencv4
     4.14.0
     ```


- #### 运行测试

  1. **编写代码**

     ```bash
     # 进入示例生成目录
     cd ~/opencv
     
     nano test.cpp
     ```

     将以下代码粘贴进`nano test.cpp`:

     ```c#
     #include <opencv2/imgcodecs.hpp>
     #include <opencv2/highgui.hpp>
     #include <opencv2/imgproc.hpp>
     #include <iostream>
     
     using namespace cv;
     using namespace std;
     
     int main() {
         // Create a 512x512 white background
         Mat img(512, 512, CV_8UC3, Scalar(255, 255, 255));
     
         // Draw shapes: red filled circle, white rectangle, cyan line
         circle(img, Point(256, 256), 100, Scalar(0, 0, 255), FILLED);
         rectangle(img, Rect(128, 128, 256, 256), Scalar(255, 255, 255), 2);
         line(img, Point(256, 128), Point(256, 256), Scalar(255, 255, 0), 3);
     
         // Draw text
         putText(img, "Hello LicheePi", Point(150, 450),
                 FONT_HERSHEY_DUPLEX, 1, Scalar(0, 0, 0), 2);
     
         // Save image
         if (imwrite("test_output.jpg", img)) {
             cout << "Success! Image saved as test_output.jpg" << endl;
         } else {
             cout << "Failed to save image!" << endl;
         }
         return 0;
     }
     ```

  2. **运行测试程序**

     ```bash
     # 编译程序
     g++ draw_test.cpp -o draw_test `pkg-config --cflags --libs opencv4`
     
     # 运行程序
     ./test
     ```

     **输出结果**

     ```c#
     Success! Image saved as test_output.jpg
     ```
     ![test.png](./images/test.png)


     
