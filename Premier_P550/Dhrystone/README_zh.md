---
sys: fedora
sys_ver: "44"
sys_var: null

category: benchmark
last_update: 2026-10-22

model: Premier P550
profile: Dhrystone

---

# RuyiSDK 性能测试示例

- **安装依赖包**

  ```bash
  sudo dnf install -y \
    git wget ca-certificates binutils tar xz zstd \
    python3 make file coreutils glibc libstdc++ libgcc
  ```

- **安装 RuyiSDK**
  根据 [RuyiSDK 官方安装指南](https://ruyisdk.org/docs/Package-Manager/installation)，在开发板上完成 Ruyi 包管理器本身的安装部署

- **安装工具链**

  ```bash
  ruyi update
  ruyi install gnu-ruyisdk
  ```


## HiFive Premier P550 Dhrystone 验证

- #### 示例描述和硬件环境准备

1. 示例功能：使用 RuyiGCC 编译 Dhrystone 2.1，执行一亿次迭代，检查变量、结构体和字符串的计算结果，并输出每秒迭代次数。
2. 硬件环境：HiFive Premier P550 开发板、供电设备、USB A-C 调试串口数据线及 Ubuntu 主机。
3. 软件环境：Fedora 44 Server，内核 `7.1.5-201.0.riscv64.omni.fc44.riscv64`，开发板已联网，可访问 Fedora 软件源、GitHub 和 Ruyi 软件源。
4. 实测工具版本：Ruyi `0.52.0`，`gnu-ruyisdk-0.20260625.0`，RuyiGCC `16.1.1 20260624`。

- #### 连接到开发板

  使用 USB A-C 数据线连接 Ubuntu 主机与开发板调试串口，并给开发板上电。

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
  ruyi venv -t toolchain/gnu-ruyisdk manual ~/ruyi-dhrystone-env
  . ~/ruyi-dhrystone-env/bin/ruyi-activate
  ```

- #### 使用 Ruyi 工具链编译 Dhrystone

  1. **获取厂商源码**

     ```bash
     mkdir -p ~/p550-dhrystone/logs
     cd ~/p550-dhrystone
     set -o pipefail
     
     git clone https://github.com/sifive/benchmark-dhrystone.git
     git -C benchmark-dhrystone rev-parse HEAD > logs/source-commit.txt
     ```

     保留原始仓库，复制源码到适配目录：

     ```c
     mkdir -p linux
     cp benchmark-dhrystone/dhry.h linux/
     cp benchmark-dhrystone/dhry_1.c linux/
     cp benchmark-dhrystone/dhry_2.c linux/
     cd linux
     ```

  2. **进行 Linux 兼容调整**

     补充标准头文件，移除冲突的旧声明，修正指针与浮点输出，并为 `main()` 增加返回值。计时使用 `times()` 的用户态 CPU 时间，计时频率由 `sysconf(_SC_CLK_TCK)` 获取。

     在新复制的适配目录中执行以下代码一次：

     ```bash
     python3 - <<'PYCODE'
     from pathlib import Path
     
     p = Path('dhry.h')
     s = p.read_text()
     s = s.replace('#include <stdio.h>', '#include <stdio.h>\n#include <stdlib.h>\n#include <string.h>\n#include <unistd.h>')
     p.write_text(s)
     
     p = Path('dhry_1.c')
     s = p.read_text()
     s = s.replace('extern char     *malloc ();', '')
     s = s.replace('extern  int     times ();', '')
     s = s.replace('main ()', 'int main (void)', 1)
     s = s.replace('"  Ptr_Comp:          %d\\n", (int) Ptr_Glob->Ptr_Comp', '"  Ptr_Comp:          %p\\n", (void *) Ptr_Glob->Ptr_Comp')
     s = s.replace('"  Ptr_Comp:          %d\\n", (int) Next_Ptr_Glob->Ptr_Comp', '"  Ptr_Comp:          %p\\n", (void *) Next_Ptr_Glob->Ptr_Comp')
     s = s.replace('User_Time = End_Time - Begin_Time;', 'User_Time = End_Time - Begin_Time;\n  printf("CPU time: %.3f seconds\\n", (double) User_Time / HZ);')
     s = s.replace('printf ("%d \\n", (int)Microseconds);', 'printf ("%.3f \\n", (double) Microseconds);')
     s = s.replace('printf ("%d \\n", (int)Dhrystones_Per_Second);', 'printf ("%.3f \\n", (double) Dhrystones_Per_Second);')
     marker = '\n}\n\n\nProc_1'
     assert marker in s, 'Unexpected upstream layout'
     s = s.replace(marker, '\n  return 0;\n}\n\n\nProc_1', 1)
     p.write_text(s)
     print('Linux compatibility changes applied.')
     PYCODE
     ```

     预期输出：

     ```text
     Linux compatibility changes applied.
     ```

  3. **使用 RuyiGCC 编译**

     ```bash
     riscv64-ruyisdk-linux-gnu-gcc \
       -std=gnu89 -O2 -fno-lto -fno-builtin \
       -march=rv64gc -mabi=lp64d \
       -Wno-error=implicit-int \
       -Wno-error=implicit-function-declaration \
       '-DHZ=sysconf(_SC_CLK_TCK)' \
       -DDHRY_ITERS=100000000 \
       dhry_1.c dhry_2.c \
       -o dhrystone \
       2>&1 | tee ../logs/build.log
     ```

     紧接着执行以下命令，确认返回值为 `0`：

     ```bash
     echo $?
     ```

     `-std=gnu89` 用于兼容旧式 C 写法；`-fno-lto` 和 `-fno-builtin` 分别关闭链接时优化和内建函数替换；`-DDHRY_ITERS=100000000` 指定一亿次迭代。本例不使用原始 Makefile 中的嵌入式栈、堆链接参数。

     检查程序架构和动态库：

     ```bash
     file dhrystone
     ldd dhrystone
     ```

     程序应为 RISC-V ELF，动态库检查不应出现 `not found` 或版本错误。


- 1. **运行测试程序**

     ```bash
     ./dhrystone 2>&1 | tee ../logs/run.log
     ```

     **输出结果**（以下为 Fedora 44、RuyiGCC 16.1.1、一亿次迭代的实际输出）：

     ```bash
     «Ruyi ruyi-dhrystone-env» [fedora@localhost linux]$ ./dhrystone 2>&1 | tee ../logs/run.log
     
     Dhrystone Benchmark, Version 2.1 (Language: C)
     
     Program compiled without 'register' attribute
     
     Execution starts, 100000000 runs through Dhrystone
     Execution ends
     
     Final values of the variables used in the benchmark:
     
     Int_Glob:            5
             should be:   5
     Bool_Glob:           1
             should be:   1
     Ch_1_Glob:           A
             should be:   A
     Ch_2_Glob:           B
             should be:   B
     Arr_1_Glob[8]:       7
             should be:   7
     Arr_2_Glob[8][7]:    100000010
             should be:   Number_Of_Runs + 10
     Ptr_Glob->
       Ptr_Comp:          0x5555cd960010
             should be:   (implementation-dependent)
       Discr:             0
             should be:   0
       Enum_Comp:         2
             should be:   2
       Int_Comp:          17
             should be:   17
       Str_Comp:          DHRYSTONE PROGRAM, SOME STRING
             should be:   DHRYSTONE PROGRAM, SOME STRING
     Next_Ptr_Glob->
       Ptr_Comp:          0x5555cd960010
             should be:   (implementation-dependent), same as above
       Discr:             0
             should be:   0
       Enum_Comp:         1
             should be:   1
       Int_Comp:          18
             should be:   18
       Str_Comp:          DHRYSTONE PROGRAM, SOME STRING
             should be:   DHRYSTONE PROGRAM, SOME STRING
     Int_1_Loc:           5
             should be:   5
     Int_2_Loc:           13
             should be:   13
     Int_3_Loc:           7
             should be:   7
     Enum_Loc:            1
             should be:   1
     Str_1_Loc:           DHRYSTONE PROGRAM, 1'ST STRING
             should be:   DHRYSTONE PROGRAM, 1'ST STRING
     Str_2_Loc:           DHRYSTONE PROGRAM, 2'ND STRING
             should be:   DHRYSTONE PROGRAM, 2'ND STRING
     
     CPU time: 16.400 seconds
     Microseconds for one run through Dhrystone: 0.164 
     Dhrystones per Second:                      6097561.000 
     
     «Ruyi ruyi-dhrystone-env» [fedora@localhost linux]$
     ```

  2. **退出 Ruyi 虚拟环境**

     ```
     cd
     ruyi-deactivate
     ```

  3. **关闭开发板**

     ```
     sudo poweroff
     ```
