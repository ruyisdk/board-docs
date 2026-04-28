# 使用 RuyiSDK 在 Milk\-V Duo256M 上编译运行 opencv\-mobile 教程

---

## 1\. 准备工作

### 安装依赖包

```bash
sudo apt update
sudo apt install -y wget make cmake git unzip build-essential
```

### 安装 ruyi 包管理器

```bash
wget https://mirror.iscas.ac.cn/ruyisdk/ruyi/tags/0.45.0/ruyi-0.45.0.amd64
chmod +x ruyi-0.45.0.amd64
sudo cp -v ruyi-0.45.0.amd64 /usr/local/bin/ruyi
```

### 安装工具链

```bash
ruyi update
ruyi install gnu-milkv-milkv-duo-musl-bin
```

---

## 2\. 创建并激活 ruyi 虚拟环境

```bash
ruyi venv -t gnu-milkv-milkv-duo-musl-bin milkv-duo venv-opencv
. ~/venv-opencv/bin/ruyi-activate
```

### 验证环境

```bash
riscv64-unknown-linux-musl-gcc --version
```

---

## 3\. 获取 opencv\-mobile 预编译库

```bash
mkdir -p ~/duo256m-opencv && cd ~/duo256m-opencv
wget https://github.com/nihui/opencv-mobile/releases/download/v35/opencv-mobile-4.13.0-milkv-duo.zip
unzip opencv-mobile-4.13.0-milkv-duo.zip
```

### log:

```
«Ruyi venv-opencv» cuiqiyun@DESKTOP-FOE2N7B:~$ mkdir -p ~/duo256m-opencv && cd ~/duo256m-opencv
«Ruyi venv-opencv» cuiqiyun@DESKTOP-FOE2N7B:~/duo256m-opencv$ wget https://github.com/nihui/opencv-mobile/releases/download/v35/opencv-mobile-4.13.0-milkv-duo.zip
--2026-04-27 21:17:17--  https://github.com/nihui/opencv-mobile/releases/download/v35/opencv-mobile-4.13.0-milkv-duo.zip
Resolving github.com (github.com)... 20.205.243.166
Connecting to github.com (github.com)|20.205.243.166|:443... connected.
HTTP request sent, awaiting response... 302 Found
Location: https://release-assets.githubusercontent.com/github-production-release-asset/327885181/e8e58a08-6663-41e5-9784-3eaf5fc69ed0?sp=r&sv=2018-11-09&sr=b&spr=https&se=2026-04-27T14%3A08%3A40Z&rscd=attachment%3B+filename%3Dopencv-mobile-4.13.0-milkv-duo.zip&rsct=application%2Foctet-stream&skoid=96c2d410-5711-43a1-aedd-ab1947aa7ab0&sktid=398a6654-997b-47e9-b12b-9515b896b4de&skt=2026-04-27T13%3A07%3A53Z&ske=2026-04-27T14%3A08%3A40Z&sks=b&skv=2018-11-09&sig=0zY%2BiawrV34rXQXkFMIy2bKBRldzR9i%2FB9vUpZzMTgc%3D&jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmVsZWFzZS1hc3NldHMuZ2l0aHVidXNlcmNvbnRlbnQuY29tIiwia2V5Ijoia2V5MSIsImV4cCI6MTc3NzI5NjEzNywibmJmIjoxNzc3Mjk1ODM3LCJwYXRoIjoicmVsZWFzZWFzc2V0cHJvZHVjdGlvbi5ibG9iLmNvcmUud2luZG93cy5uZXQifQ.BchBWfKeqgjp9wd22AqU22dqaHlPYLqYSLI_H0N3Sjk&response-content-disposition=attachment%3B%20filename%3Dopencv-mobile-4.13.0-milkv-duo.zip&response-content-type=application%2Foctet-stream [following]
--2026-04-27 21:17:18--  https://release-assets.githubusercontent.com/github-production-release-asset/327885181/e8e58a08-6663-41e5-9784-3eaf5fc69ed0?sp=r&sv=2018-11-09&sr=b&spr=https&se=2026-04-27T14%3A08%3A40Z&rscd=attachment%3B+filename%3Dopencv-mobile-4.13.0-milkv-duo.zip&rsct=application%2Foctet-stream&skoid=96c2d410-5711-43a1-aedd-ab1947aa7ab0&sktid=398a6654-997b-47e9-b12b-9515b896b4de&skt=2026-04-27T13%3A07%3A53Z&ske=2026-04-27T14%3A08%3A40Z&sks=b&skv=2018-11-09&sig=0zY%2BiawrV34rXQXkFMIy2bKBRldzR9i%2FB9vUpZzMTgc%3D&jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmVsZWFzZS1hc3NldHMuZ2l0aHVidXNlcmNvbnRlbnQuY29tIiwia2V5Ijoia2V5MSIsImV4cCI6MTc3NzI5NjEzNywibmJmIjoxNzc3Mjk1ODM3LCJwYXRoIjoicmVsZWFzZWFzc2V0cHJvZHVjdGlvbi5ibG9iLmNvcmUud2luZG93cy5uZXQifQ.BchBWfKeqgjp9wd22AqU22dqaHlPYLqYSLI_H0N3Sjk&response-content-disposition=attachment%3B%20filename%3Dopencv-mobile-4.13.0-milkv-duo.zip&response-content-type=application%2Foctet-stream
Resolving release-assets.githubusercontent.com (release-assets.githubusercontent.com)... 185.199.110.133, 185.199.108.133, 185.199.111.133, ...
Connecting to release-assets.githubusercontent.com (release-assets.githubusercontent.com)|185.199.110.133|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 8761605 (8.4M) [application/octet-stream]
Saving to: ‘opencv-mobile-4.13.0-milkv-duo.zip’

opencv-mobile-4.13.0-milkv-du 100%[=================================================>]   8.36M  8.66MB/s    in 1.0s

2026-04-27 21:17:19 (8.66 MB/s) - ‘opencv-mobile-4.13.0-milkv-duo.zip’ saved [8761605/8761605]
«Ruyi venv-opencv» cuiqiyun@DESKTOP-FOE2N7B:~/duo256m-opencv$ unzip opencv-mobile-4.13.0-milkv-duo.zip
Archive:  opencv-mobile-4.13.0-milkv-duo.zip
   creating: opencv-mobile-4.13.0-milkv-duo/
   creating: opencv-mobile-4.13.0-milkv-duo/lib/
  inflating: opencv-mobile-4.13.0-milkv-duo/lib/libopencv_features2d.a
  inflating: opencv-mobile-4.13.0-milkv-duo/lib/libopencv_photo.a
  inflating: opencv-mobile-4.13.0-milkv-duo/lib/libopencv_imgproc.a
  inflating: opencv-mobile-4.13.0-milkv-duo/lib/libopencv_video.a
  inflating: opencv-mobile-4.13.0-milkv-duo/lib/libopencv_core.a
  inflating: opencv-mobile-4.13.0-milkv-duo/lib/libopencv_highgui.a
   creating: opencv-mobile-4.13.0-milkv-duo/lib/cmake/
   creating: opencv-mobile-4.13.0-milkv-duo/lib/cmake/opencv4/
  inflating: opencv-mobile-4.13.0-milkv-duo/lib/cmake/opencv4/OpenCVModules.cmake
  inflating: opencv-mobile-4.13.0-milkv-duo/lib/cmake/opencv4/OpenCVConfig-version.cmake
  inflating: opencv-mobile-4.13.0-milkv-duo/lib/cmake/opencv4/OpenCVConfig.cmake
  inflating: opencv-mobile-4.13.0-milkv-duo/lib/cmake/opencv4/OpenCVModules-release.cmake
   creating: opencv-mobile-4.13.0-milkv-duo/bin/
  inflating: opencv-mobile-4.13.0-milkv-duo/bin/setup_vars_opencv4.sh
   creating: opencv-mobile-4.13.0-milkv-duo/include/
   creating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/
   creating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/opencv2/
  inflating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/opencv2/highgui.hpp
  inflating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/opencv2/imgproc.hpp
  inflating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/opencv2/opencv.hpp
  inflating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/opencv2/video.hpp
  inflating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/opencv2/photo.hpp
  inflating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/opencv2/features2d.hpp
  inflating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/opencv2/opencv_modules.hpp
  inflating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/opencv2/cvconfig.h
   creating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/opencv2/features2d/
  inflating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/opencv2/features2d/features2d.hpp
   creating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/opencv2/features2d/hal/
  inflating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/opencv2/features2d/hal/interface.h
   creating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/opencv2/photo/
  inflating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/opencv2/photo/photo.hpp
   creating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/opencv2/photo/legacy/
  inflating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/opencv2/photo/legacy/constants_c.h
   creating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/opencv2/core/
  inflating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/opencv2/core/utility.hpp
  inflating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/opencv2/core/types_c.h
  inflating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/opencv2/core/quaternion.hpp
  inflating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/opencv2/core/dualquaternion.inl.hpp
  inflating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/opencv2/core/softfloat.hpp
   creating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/opencv2/core/utils/
  inflating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/opencv2/core/utils/filesystem.hpp
  inflating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/opencv2/core/utils/tls.hpp
  inflating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/opencv2/core/utils/logger.defines.hpp
  inflating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/opencv2/core/utils/logtag.hpp
  inflating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/opencv2/core/utils/trace.hpp
  inflating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/opencv2/core/utils/instrumentation.hpp
  inflating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/opencv2/core/utils/allocator_stats.impl.hpp
  inflating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/opencv2/core/utils/logger.hpp
  inflating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/opencv2/core/utils/allocator_stats.hpp
  inflating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/opencv2/core/utils/fp_control_utils.hpp
  inflating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/opencv2/core/bindings_utils.hpp
   creating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/opencv2/core/parallel/
  inflating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/opencv2/core/parallel/parallel_backend.hpp
   creating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/opencv2/core/parallel/backend/
  inflating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/opencv2/core/parallel/backend/parallel_for.tbb.hpp
  inflating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/opencv2/core/parallel/backend/parallel_for.openmp.hpp
  inflating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/opencv2/core/sse_utils.hpp
  inflating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/opencv2/core/neon_utils.hpp
  inflating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/opencv2/core/eigen.hpp
  inflating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/opencv2/core/cvdef.h
  inflating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/opencv2/core/affine.hpp
  inflating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/opencv2/core/persistence.hpp
  inflating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/opencv2/core/base.hpp
  inflating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/opencv2/core/mat.hpp
  inflating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/opencv2/core/mat.inl.hpp
  inflating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/opencv2/core/optim.hpp
   creating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/opencv2/core/hal/
  inflating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/opencv2/core/hal/intrin.hpp
  inflating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/opencv2/core/hal/intrin_wasm.hpp
  inflating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/opencv2/core/hal/intrin_msa.hpp
  inflating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/opencv2/core/hal/simd_utils.impl.hpp
  inflating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/opencv2/core/hal/intrin_avx.hpp
  inflating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/opencv2/core/hal/intrin_legacy_ops.h
  inflating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/opencv2/core/hal/intrin_vsx.hpp
  inflating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/opencv2/core/hal/hal.hpp
  inflating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/opencv2/core/hal/intrin_lasx.hpp
  inflating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/opencv2/core/hal/intrin_rvv071.hpp
  inflating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/opencv2/core/hal/intrin_avx512.hpp
  inflating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/opencv2/core/hal/intrin_neon.hpp
  inflating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/opencv2/core/hal/intrin_forward.hpp
  inflating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/opencv2/core/hal/intrin_sse.hpp
  inflating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/opencv2/core/hal/msa_macros.h
  inflating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/opencv2/core/hal/intrin_math.hpp
  inflating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/opencv2/core/hal/intrin_cpp.hpp
  inflating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/opencv2/core/hal/intrin_sse_em.hpp
  inflating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/opencv2/core/hal/interface.h
  inflating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/opencv2/core/hal/intrin_lsx.hpp
  inflating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/opencv2/core/hal/intrin_rvv_scalable.hpp
  inflating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/opencv2/core/traits.hpp
  inflating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/opencv2/core/saturate.hpp
  inflating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/opencv2/core/cvstd.inl.hpp
  inflating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/opencv2/core/cvstd_wrapper.hpp
  inflating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/opencv2/core/matx.inl.hpp
  inflating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/opencv2/core/cv_cpu_helper.h
   creating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/opencv2/core/detail/
  inflating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/opencv2/core/detail/exception_ptr.hpp
  inflating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/opencv2/core/detail/dispatch_helper.impl.hpp
  inflating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/opencv2/core/detail/async_promise.hpp
  inflating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/opencv2/core/operations.hpp
  inflating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/opencv2/core/cv_cpu_dispatch.h
  inflating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/opencv2/core/matx.hpp
  inflating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/opencv2/core/cvstd.hpp
  inflating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/opencv2/core/core.hpp
  inflating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/opencv2/core/bufferpool.hpp
  inflating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/opencv2/core/vsx_utils.hpp
  inflating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/opencv2/core/core_c.h
  inflating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/opencv2/core/async.hpp
  inflating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/opencv2/core/fast_math.hpp
  inflating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/opencv2/core/quaternion.inl.hpp
  inflating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/opencv2/core/dualquaternion.hpp
  inflating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/opencv2/core/check.hpp
  inflating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/opencv2/core/types.hpp
  inflating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/opencv2/core/version.hpp
  inflating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/opencv2/core/simd_intrinsics.hpp
  inflating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/opencv2/dnn.hpp
   creating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/opencv2/imgproc/
  inflating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/opencv2/imgproc/imgproc.hpp
  inflating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/opencv2/imgproc/types_c.h
  inflating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/opencv2/imgproc/bindings.hpp
  inflating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/opencv2/imgproc/imgproc_c.h
   creating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/opencv2/imgproc/hal/
  inflating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/opencv2/imgproc/hal/hal.hpp
  inflating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/opencv2/imgproc/hal/interface.h
   creating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/opencv2/imgproc/detail/
  inflating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/opencv2/imgproc/detail/legacy.hpp
  inflating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/opencv2/imgproc/detail/gcgraph.hpp
  inflating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/opencv2/imgproc/segmentation.hpp
  inflating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/opencv2/core.hpp
   creating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/opencv2/dnn/
  inflating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/opencv2/dnn/dnn.hpp
   creating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/opencv2/video/
  inflating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/opencv2/video/background_segm.hpp
  inflating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/opencv2/video/video.hpp
   creating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/opencv2/video/legacy/
  inflating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/opencv2/video/legacy/constants_c.h
   creating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/opencv2/video/detail/
  inflating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/opencv2/video/detail/tracking.detail.hpp
  inflating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/opencv2/video/tracking.hpp
   creating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/opencv2/highgui/
  inflating: opencv-mobile-4.13.0-milkv-duo/include/opencv4/opencv2/highgui/highgui.hpp
   creating: opencv-mobile-4.13.0-milkv-duo/share/
   creating: opencv-mobile-4.13.0-milkv-duo/share/licenses/
   creating: opencv-mobile-4.13.0-milkv-duo/share/licenses/opencv4/
  inflating: opencv-mobile-4.13.0-milkv-duo/share/licenses/opencv4/SoftFloat-COPYING.txt
  inflating: opencv-mobile-4.13.0-milkv-duo/share/licenses/opencv4/mscr-chi_table_LICENSE.txt
```



---

## 4\. 准备测试图片 in\.jpg

1. 在电脑上任意找一张 JPG 图片

2. 放入目录：`\~/duo256m\-opencv/`

3. 重命名为：`in\.jpg`

---

## 5\. 编写测试代码 main\.cpp

```bash
cat > main.cpp << 'EOF'
#include <opencv2/opencv.hpp>
using namespace cv;

int main()
{
    Mat img = imread("in.jpg");
    if (img.empty()) {
        printf("open in.jpg failed!\n");
        return -1;
    }

    int w = img.cols;
    int h = img.rows;
    printf("w=%d, h=%d\n", w, h);

    resize(img, img, Size(320, 240));
    imwrite("out.jpg", img);
    printf("resize success, out.jpg saved!\n");

    return 0;
}
EOF
```

### log:

```
«Ruyi venv-opencv» cuiqiyun@DESKTOP-FOE2N7B:~/duo256m-opencv$ cat > main.cpp << 'EOF'
#include <opencv2/opencv.hpp>
using namespace cv;

int main()
{
    Mat img = imread("in.jpg");
    if(img.empty()){
        printf("open in.jpg failed!\n");
        return -1;
    }

    int w = img.cols;
    int h = img.rows;
    printf("w=%d, h=%d\n", w, h);

    resize(img, img, Size(320, 240));
    imwrite("out.jpg", img);
    printf("resize success, out.jpg saved!\n");

    return 0;
}
EOF
```



---

## 6\. 编写 CMakeLists\.txt

```bash
cat > CMakeLists.txt << 'EOF'
cmake_minimum_required(VERSION 3.5)
project(opencv-mobile-test)

set(CMAKE_CXX_STANDARD 11)

set(CMAKE_C_COMPILER riscv64-unknown-linux-musl-gcc)
set(CMAKE_CXX_COMPILER riscv64-unknown-linux-musl-g++)

set(OpenCV_DIR ${CMAKE_CURRENT_SOURCE_DIR}/opencv-mobile-4.13.0-milkv-duo/lib/cmake/opencv4)
find_package(OpenCV REQUIRED)

add_executable(opencv-test main.cpp)
target_link_libraries(opencv-test ${OpenCV_LIBS})
EOF
```

### log：

```
«Ruyi venv-opencv» cuiqiyun@DESKTOP-FOE2N7B:~/duo256m-opencv$ cat > CMakeLists.txt << 'EOF'
cmake_minimum_required(VERSION 3.5)
project(opencv-mobile-test)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_C_COMPILER riscv64-unknown-linux-musl-gcc)
set(CMAKE_CXX_COMPILER riscv64-unknown-linux-musl-g++)

set(OpenCV_DIR ${CMAKE_CURRENT_SOURCE_DIR}/opencv-mobile-4.13.0-milkv-duo/lib/cmake/opencv4)
find_package(OpenCV REQUIRED)

add_executable(opencv-test main.cpp)
target_link_libraries(opencv-test ${OpenCV_LIBS})
EOF
```



---

## 7\. 交叉编译

```bash
mkdir build && cd build
cmake ..
make -j4
```

### log：

```Plain Text
«Ruyi venv-opencv» cuiqiyun@DESKTOP-FOE2N7B:~/duo256m-opencv$ mkdir build && cd build
«Ruyi venv-opencv» cuiqiyun@DESKTOP-FOE2N7B:~/duo256m-opencv/build$ cmake ..
-- The C compiler identification is GNU 11.4.0
-- The CXX compiler identification is GNU 11.4.0
-- Detecting C compiler ABI info
-- Detecting C compiler ABI info - done
-- Check for working C compiler: /usr/bin/cc - skipped
-- Detecting C compile features
-- Detecting C compile features - done
-- Detecting CXX compiler ABI info
-- Detecting CXX compiler ABI info - done
-- Check for working CXX compiler: /usr/bin/c++ - skipped
-- Detecting CXX compile features
-- Detecting CXX compile features - done
-- Found OpenCV: /home/cuiqiyun/duo256m-opencv/opencv-mobile-4.13.0-milkv-duo (found version "4.13.0")
-- Configuring done
-- Generating done
-- Build files have been written to: /home/cuiqiyun/duo256m-opencv/build
«Ruyi venv-opencv» cuiqiyun@DESKTOP-FOE2N7B:~/duo256m-opencv/build$ make -j4
[ 50%] Building CXX object CMakeFiles/opencv-test.dir/main.cpp.o
[100%] Linking CXX executable opencv-test
[100%] Built target opencv-test
«Ruyi venv-opencv» cuiqiyun@DESKTOP-FOE2N7B:~/duo256m-opencv/build$ scp opencv-test root@192.168.42.1:/root
^C«Ruyi venv-opencv» cuiqiyun@DESKTOP-FOE2N7B:~/duo256m-opencv/build$ cd ~/duo256m-opencv
«Ruyi venv-opencv» cuiqiyun@DESKTOP-FOE2N7B:~/duo256m-opencv$ wget https://upload.wikimedia.org/wikipedia/commons/thumb/6/63/Neon signs.jpg/320px-Neon signs.jpg -O in.jpg
--2026-04-27 21:20:01--  https://upload.wikimedia.org/wikipedia/commons/thumb/6/63/Neon
Resolving upload.wikimedia.org (upload.wikimedia.org)... 103.102.166.240, 2001:df2:e500:ed1a::2:b
Connecting to upload.wikimedia.org (upload.wikimedia.org)|103.102.166.240|:443... connected.
OpenSSL: error:0A000126:SSL routines::unexpected eof while reading
Unable to establish SSL connection.
--2026-04-27 21:22:02--  http://signs.jpg/320px-Neon
Resolving signs.jpg (signs.jpg)... failed: Temporary failure in name resolution.
wget: unable to resolve host address ‘signs.jpg’
--2026-04-27 21:22:12--  http://signs.jpg/
Resolving signs.jpg (signs.jpg)... failed: Name or service not known.
wget: unable to resolve host address ‘signs.jpg’
```

---

## 8\. 传输文件至开发板

```bash
scp opencv-test root@192.168.42.1:/root
scp ../in.jpg root@192.168.42.1:/root
```

### log：

```
«Ruyi venv-opencv» cuiqiyun@DESKTOP-FOE2N7B:~/duo256m-opencv$ scp in.jpg root@192.168.42.1:/root/
root@192.168.42.1's password:
in.jpg                                                                                100%   44KB   2.9MB/s   00:00
«Ruyi venv-opencv» cuiqiyun@DESKTOP-FOE2N7B:~/duo256m-opencv$ scp build/opencv-test root@192.168.42.1:/root/
root@192.168.42.1's password:
opencv-test                                                                           100% 2237KB   3.4MB/s   00:00
```



---

## 9\. 在 Duo256M 上运行

```bash
ssh root@192.168.42.1
chmod +x opencv-test
./opencv-test
```

### log：

```
«Ruyi venv-opencv» cuiqiyun@DESKTOP-FOE2N7B:~/duo256m-opencv$ ssh root@192.168.42.1
root@192.168.42.1's password:
[root@milkv-duo]~# chmod +x opencv-test
[root@milkv-duo]~# ./opencv-test
opencv-mobile HW JPG decoder with cvi
Error loading shared library /mnt/system/usr/lib/libvpu.so: No such file or directory
w=940, h=940
resize success, out.jpg saved!
```



---
