---
sys: Bianbu
sys_ver: "4.0.7"
sys_var: null

category: benchmark
last_update: 2026-11-21

model: SpacemiT K3 Pico-ITX
profile: OpenBLAS SGEMM
---

# RuyiSDK 性能测试示例

- **安装依赖包**

  在开发板终端执行。

  ```bash
  sudo apt update && sudo apt install -y \
    wget ca-certificates tar xz-utils zstd build-essential \
    file binutils util-linux openblas-spacemit
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

## SpacemiT K3 Pico-ITX OpenBLAS SGEMM 验证

- #### 示例描述和硬件环境准备

1. 示例功能：使用 Ruyi GCC 编译 SGEMM 测试程序，调用厂商 OpenBLAS 的 `cblas_sgemm`，校验矩阵乘法结果，并输出单精度矩阵乘法耗时和 GFLOPS。
2. 硬件环境：SpacemiT K3 Pico-ITX 开发板、供电设备及可通过 SSH 连接开发板的主机。
3. 软件环境：Bianbu 4.0.7（riscv64），开发板已联网，可访问 Bianbu 软件源和 Ruyi 软件源。
4. 构建范围：Ruyi GCC 编译测试程序，链接 `/opt/openblas-spacemit` 中的厂商预编译库。测试结果反映该库的 SGEMM 性能。

  测试程序基于厂商 `cblas_sgemm` 示例扩展。计时采用一次预热和五轮采样，取单次调用耗时的中位数，吞吐按 `2 × M × N × K / 秒数 / 10⁹` 计算。参考[厂商数学库文档](https://github.com/spacemit-com/docs-ai/blob/main/zh/compute_stack/math_library.md#openblas-demo)。

- #### 创建并激活 ruyi 虚拟环境

  ```bash
  mkdir -p ~/k3-openblas-sgemm/logs
  cd ~/k3-openblas-sgemm
  set -o pipefail

  ruyi venv -t gnu-ruyisdk manual openblas-env
  source openblas-env/bin/ruyi-activate
  riscv64-ruyisdk-linux-gnu-gcc --version
  ```

- #### 使用 Ruyi 工具链编译 SGEMM 测试程序

  1. **创建测试程序**

     ```bash
     cat > sgemm_demo.c <<'EOF'
     #define _POSIX_C_SOURCE 200809L
     #include <cblas.h>
     #include <errno.h>
     #include <math.h>
     #include <stdio.h>
     #include <stdlib.h>
     #include <time.h>

     enum { REPEATS = 5 };

     static double now_seconds(void)
     {
         struct timespec ts;
         if (clock_gettime(CLOCK_MONOTONIC, &ts) != 0) {
             perror("clock_gettime");
             exit(EXIT_FAILURE);
         }
         return (double)ts.tv_sec + (double)ts.tv_nsec * 1e-9;
     }

     static int compare_seconds(const void *left, const void *right)
     {
         double a = *(const double *)left;
         double b = *(const double *)right;
         return (a > b) - (a < b);
     }

     static int check_demo(void)
     {
         const float a[4] = {1, 2, 3, 4};
         const float b[4] = {5, 6, 7, 8};
         const float expected[4] = {19, 22, 43, 50};
         float c[4] = {0};

         cblas_sgemm(CblasRowMajor, CblasNoTrans, CblasNoTrans,
                     2, 2, 2, 1.0f, a, 2, b, 2, 0.0f, c, 2);
         printf("C = [%.6f, %.6f, %.6f, %.6f]\n",
                c[0], c[1], c[2], c[3]);
         for (int i = 0; i < 4; ++i) {
             if (!isfinite(c[i]) || fabsf(c[i] - expected[i]) > 1e-5f)
                 return 0;
         }
         return 1;
     }

     static int check_samples(const float *a, const float *b,
                              const float *c, int n)
     {
         const int points[3] = {0, n / 2, n - 1};
         for (int row = 0; row < 3; ++row) {
             for (int col = 0; col < 3; ++col) {
                 int i = points[row];
                 int j = points[col];
                 double expected = 0.0;
                 for (int k = 0; k < n; ++k)
                     expected += (double)a[(size_t)i * n + k]
                               * (double)b[(size_t)k * n + j];
                 double got = c[(size_t)i * n + j];
                 if (!isfinite(got) ||
                     fabs(got - expected) > 1e-3 * (1.0 + fabs(expected)))
                     return 0;
             }
         }
         return 1;
     }

     static int benchmark(int n)
     {
         size_t count = (size_t)n * n;
         float *a = malloc(count * sizeof(*a));
         float *b = malloc(count * sizeof(*b));
         float *c = malloc(count * sizeof(*c));
         int ok = 0;

         if (!a || !b || !c) {
             fprintf(stderr, "Matrix allocation failed for N=%d\n", n);
             goto cleanup;
         }
         for (size_t i = 0; i < count; ++i) {
             a[i] = (float)((int)(i % 17) - 8) / 16.0f;
             b[i] = (float)((int)(i % 13) - 6) / 16.0f;
             c[i] = 0.0f;
         }

         cblas_sgemm(CblasRowMajor, CblasNoTrans, CblasNoTrans,
                     n, n, n, 1.0f, a, n, b, n, 0.0f, c, n);
         if (!check_samples(a, b, c, n)) {
             fprintf(stderr, "Warm-up sample check: FAIL (N=%d)\n", n);
             goto cleanup;
         }

         double seconds[REPEATS];
         for (int r = 0; r < REPEATS; ++r) {
             double start = now_seconds();
             cblas_sgemm(CblasRowMajor, CblasNoTrans, CblasNoTrans,
                         n, n, n, 1.0f, a, n, b, n, 0.0f, c, n);
             seconds[r] = now_seconds() - start;
             if (seconds[r] <= 0.0) {
                 fprintf(stderr, "Invalid elapsed time\n");
                 goto cleanup;
             }
             if (!check_samples(a, b, c, n)) {
                 fprintf(stderr, "Sample check: FAIL (N=%d, round=%d)\n",
                         n, r + 1);
                 goto cleanup;
             }
         }
         qsort(seconds, REPEATS, sizeof(seconds[0]), compare_seconds);
         double median = seconds[REPEATS / 2];
         double gflops = 2.0 * n * n * n / median / 1e9;
         printf("%5d %5d %5d %7d %12.6f %12.3f PASS\n",
                n, n, n, REPEATS, median * 1000.0, gflops);
         ok = 1;

     cleanup:
         free(a);
         free(b);
         free(c);
         return ok;
     }

     int main(int argc, char **argv)
     {
         const int sizes[] = {256, 512, 1024};
         int selected = 0;
         if (argc > 2) {
             fprintf(stderr, "Usage: %s [N: 1..8192]\n", argv[0]);
             return EXIT_FAILURE;
         }
         if (argc == 2) {
             char *end;
             errno = 0;
             long value = strtol(argv[1], &end, 10);
             if (errno || end == argv[1] || *end || value < 1 || value > 8192) {
                 fprintf(stderr, "N must be an integer from 1 to 8192\n");
                 return EXIT_FAILURE;
             }
             selected = (int)value;
         }

         printf("OpenBLAS: %s\n", openblas_get_config());
         printf("Core: %s\n", openblas_get_corename());
         printf("Threads: %d\n", openblas_get_num_threads());
         int ok = check_demo();
         printf("SGEMM check: %s\n", ok ? "PASS" : "FAIL");
         if (!ok)
             return EXIT_FAILURE;
         puts("    M     N     K Repeats    Median_ms       GFLOPS Sample_check");
         if (selected) {
             ok = benchmark(selected);
         } else {
             for (size_t i = 0; i < sizeof(sizes) / sizeof(sizes[0]); ++i) {
                 if (!benchmark(sizes[i])) {
                     ok = 0;
                     break;
                 }
             }
         }
         printf("Overall: %s\n", ok ? "PASS" : "FAIL");
         return ok ? EXIT_SUCCESS : EXIT_FAILURE;
     }
     EOF
     ```

  2. **使用 RuyiGCC 编译**

     ```bash
     export OPENBLAS_DIR=/opt/openblas-spacemit
     set -o pipefail

     riscv64-ruyisdk-linux-gnu-gcc \
       -std=c11 -O2 -Wall -Wextra \
       -march=rv64gc -mabi=lp64d \
       -I"$OPENBLAS_DIR/include" \
       sgemm_demo.c \
       -L"$OPENBLAS_DIR/lib" \
       -Wl,-rpath,"$OPENBLAS_DIR/lib" \
       -Wl,-rpath-link,/usr/lib/riscv64-linux-gnu:/usr/lib \
       -lopenblas -lm \
       -o sgemm_demo \
       2>&1 | tee logs/build.log
     echo "Build exit code: $?"
     ```

     编译成功时返回值为 `0`。检查程序架构和动态库。

     ```bash
     file sgemm_demo
     ldd sgemm_demo
     ```

     `libopenblas` 应解析到 `/opt/openblas-spacemit/lib/`，动态库检查应无 `not found`。

- #### 运行示例并验证结果

  1. **运行单线程矩阵乘法测试**

     ```bash
     cd ~/k3-openblas-sgemm
     set -o pipefail
     export OPENBLAS_NUM_THREADS=1
     export OMP_NUM_THREADS=1
     export LD_LIBRARY_PATH=/opt/openblas-spacemit/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}

     taskset -c 0 ./sgemm_demo 2>&1 | tee logs/run-single.log
     echo "Run exit code: $?"
     ```

     **输出结果**

     ```text
     OpenBLAS: OpenBLAS 0.3.32 NO_AFFINITY x100 MAX_THREADS=8
     Core: x100
     Threads: 1
     C = [19.000000, 22.000000, 43.000000, 50.000000]
     SGEMM check: PASS
         M     N     K Repeats    Median_ms       GFLOPS Sample_check
       256   256   256       5     1.232729       27.220 PASS
       512   512   512       5     9.807254       27.371 PASS
      1024  1024  1024       5    75.868364       28.305 PASS
     Overall: PASS
     Run exit code: 0
     ```

     `SGEMM check` 检查厂商示例的全部四个结果，`Sample_check` 检查大矩阵中的九个采样位置。`Median_ms` 为五轮调用耗时的中位数，校验和内存分配均在计时区间外。

  2. **运行 5120 阶矩阵测试**

     ```bash
     taskset -c 0 ./sgemm_demo 5120 2>&1 | tee logs/run-5120.log
     echo "Run exit code: $?"
     ```

     **输出结果**

     ```text
     OpenBLAS: OpenBLAS 0.3.32 NO_AFFINITY x100 MAX_THREADS=8
     Core: x100
     Threads: 1
     C = [19.000000, 22.000000, 43.000000, 50.000000]
     SGEMM check: PASS
         M     N     K Repeats    Median_ms       GFLOPS Sample_check
      5120  5120  5120       5  9058.607966       29.633 PASS
     Overall: PASS
     Run exit code: 0
     ```

     厂商也使用 5120 阶 SGEMM 评估单核吞吐。本程序采用 CBLAS 接口及五轮中位数，计时方法见上述代码。参考[厂商单核 SGEMM 基准](https://github.com/spacemit-com/docs-ai/blob/main/zh/compute_stack/math_library.md#1-openblas-sgemm-性能基准单核)。

- #### 退出环境

  ```bash
  cd ~
  ruyi-deactivate
  ```
