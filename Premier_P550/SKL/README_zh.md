---
sys: fedora
sys_ver: "44"
sys_var: null

category: ai
last_update: 2026-10-26

model: Premier P550
profile: SKL
---

# RuyiSDK 人工智能示例

- **安装依赖包**

  在开发板 Fedora 终端执行：

  ```bash
  sudo dnf install -y git glibc-devel
  ```

- **安装 RuyiSDK**

  根据 [RuyiSDK 官方安装指南](https://ruyisdk.org/docs/Package-Manager/installation)，在开发板上完成 Ruyi 包管理器本身的安装部署。

- **安装工具链**

  ```bash
  ruyi update
  ruyi install gnu-ruyisdk
  ```

## HiFive Premier P550 SKL 验证

- #### 示例描述和硬件环境准备

1. 示例功能：使用 RuyiGCC 编译 SiFive SKL 的 FP32 标量参考算子及验证程序，检查矩阵乘法、Softmax 和 Softmax 大数值输入的计算结果。
2. 硬件环境：HiFive Premier P550 开发板、供电设备、USB A-C 调试串口数据线及 Ubuntu 主机。
3. 软件环境：Fedora 44 Server，内核 `7.1.5-201.0.riscv64.omni.fc44.riscv64`，开发板已联网，可访问 Fedora 软件源、GitHub 和 Ruyi 软件源。
4. 测试使用的工具链环境：Ruyi `0.52.0`，`gnu-ruyisdk-0.20260625.0`，RuyiGCC `16.1.1 20260624`。

- #### 连接到开发板

  使用 USB A-C 数据线连接 Ubuntu 主机与开发板调试串口，并使用配套供电设备给开发板上电。

  在 **Ubuntu 主机**执行：

  ```bash
  sudo picocom -b 115200 /dev/ttyUSB2
  ```

  若主机未安装 picocom，先执行 `sudo apt install -y picocom`。串口设备名以实际识别结果为准。

  按回车后登录：

  ```text
  login: fedora
  Password: linux
  ```

- #### 创建并激活 ruyi 虚拟环境

  ```bash
  mkdir -p ~/p550-skl/logs
  cd ~/p550-skl
  set -o pipefail

  ruyi venv -t toolchain/gnu-ruyisdk manual ~/ruyi-skl-env
  . ~/ruyi-skl-env/bin/ruyi-activate
  ```

- #### 使用 Ruyi 工具链编译 SKL

  1. **获取厂商源码**

     ```bash
     git -c http.version=HTTP/1.1 clone --depth 1 \
       https://github.com/sifiveinc/skl.git
     
     git -C skl -c http.version=HTTP/1.1 fetch --depth 1 origin \
       a3cb2cf34e677d106f8d4b616031bf9f60dbf0fa
     
     git -C skl checkout --detach a3cb2cf34e677d106f8d4b616031bf9f60dbf0fa
     git -C skl rev-parse HEAD > logs/source-commit.log
     ```

     固定源码版本，以保持本教程使用的文件路径和接口一致。
     
  2. **创建算子验证程序**

     矩阵乘法使用 `2×3` 与 `3×2` 的输入矩阵，核对结果 `58、64、139、154`；Softmax 使用 `[1, 2, 3]`，核对输出及概率总和，并检查输入整体平移为 `[1001, 1002, 1003]` 后的结果。

     ```bash
     cat > skl_demo.c <<'EOF'
     #include <math.h>
     #include <stdio.h>
     #include "gemm_f32rc_f32rc_f32rc.h"
     #include "softmax_f32.h"
     
     static int check(const float *got, const float *expected, size_t n)
     {
         for (size_t i = 0; i < n; ++i) {
             if (!isfinite(got[i]) || fabsf(got[i] - expected[i]) > 1e-5f)
                 return 0;
         }
         return 1;
     }
     
     int main(void)
     {
         const float a[6] = {1, 2, 3, 4, 5, 6};
         const float b[6] = {7, 8, 9, 10, 11, 12};
         const float expected_c[4] = {58, 64, 139, 154};
         float c[4] = {0};
     
         skl_gemm_f32rc_f32rc_f32rc_ref(
             2, 2, 3, 1.0f, a, 3, 1, b, 2, 1, 0.0f, c, 2, 1);
     
         printf("GEMM result:\n%.0f %.0f\n%.0f %.0f\n",
                c[0], c[1], c[2], c[3]);
     
         int gemm_ok = check(c, expected_c, 4);
         printf("GEMM: %s\n", gemm_ok ? "PASS" : "FAIL");
     
         const float x[3] = {1, 2, 3};
         const float expected_y[3] = {
             0.09003057f, 0.24472847f, 0.66524096f
         };
         float y[3] = {0};
     
         skl_softmax_f32_ref(y, x, 1.0f, 3);
     
         float sum = y[0] + y[1] + y[2];
         printf("Softmax result: %.6f %.6f %.6f\n", y[0], y[1], y[2]);
         printf("Softmax sum: %.6f\n", sum);
     
         int softmax_ok = check(y, expected_y, 3)
                       && fabsf(sum - 1.0f) < 1e-5f;
         printf("Softmax: %s\n", softmax_ok ? "PASS" : "FAIL");
     
         const float shifted[3] = {1001, 1002, 1003};
         skl_softmax_f32_ref(y, shifted, 1.0f, 3);
     
         int stable_ok = check(y, expected_y, 3);
         printf("Softmax large-input check: %s\n",
                stable_ok ? "PASS" : "FAIL");
     
         int ok = gemm_ok && softmax_ok && stable_ok;
         printf("Overall: %s\n", ok ? "PASS" : "FAIL");
         return ok ? 0 : 1;
     }
     EOF
     ```
     
  3. **使用 RuyiGCC 编译**
  
     ```bash
     set -o pipefail

     riscv64-ruyisdk-linux-gnu-gcc \
       -std=c11 -O2 -Wall -Wextra \
       -march=rv64gc -mabi=lp64d \
       -Iskl/include \
       -Iskl/ref/gemm \
       -Iskl/ref/softmax \
       skl_demo.c \
       skl/ref/gemm/gemm_f32rc_f32rc_f32rc.c \
       skl/ref/softmax/softmax_f32.c \
       -lm \
       -o skl_demo \
       2>&1 | tee logs/build.log

     echo "Build exit code: $?"
     ```

     实际输出：

     ```text
     Build exit code: 0
     ```
  
  `-march=rv64gc -mabi=lp64d` 指定目标指令集和 ABI；`-lm` 链接 Softmax 所需的数学函数库。本例仅编译两个 FP32 参考算子，不使用仓库默认的向量工具链配置。
  
- #### 运行示例并验证结果

  1. **运行测试程序**

     ```bash
     ./skl_demo 2>&1 | tee logs/run.log
     echo "Run exit code: $?"
     ```

     **输出结果**：

     ```text
     «Ruyi ruyi-skl-env» [fedora@localhost p550-skl]$ ./skl_demo 2>&1 | tee logs/run.log
     GEMM result:
     58 64
     139 154
     GEMM: PASS
     Softmax result: 0.090031 0.244728 0.665241
     Softmax sum: 1.000000
     Softmax: PASS
     Softmax large-input check: PASS
     Overall: PASS
     «Ruyi ruyi-skl-env» [fedora@localhost p550-skl]$ echo "Run exit code: $?"
     Run exit code: 0
     ```
     
     矩阵乘法、Softmax 和 Softmax 大数值输入检查均为 `PASS`，程序退出码为 `0`，本示例的数值校验通过。编译与运行日志分别保存在 `logs/build.log` 和 `logs/run.log`。
     
  2. **退出 Ruyi 虚拟环境**
  
     ```bash
     cd
     ruyi-deactivate
     ```
  
  3. **关闭开发板**
  
     ```bash
     sudo poweroff
     ```
