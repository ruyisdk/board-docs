---
sys: ubuntu
sys_ver: "24.04"
sys_var: null

status: gpio
last_update: 2026-05-17

model: VisionFive2 Lite
profile: GPIO_PUD

---

#  RuyiSDK GPIO功能示例

- **安装依赖包**

  ```bash
  sudo apt update
  sudo apt install -y wget tar zstd xz-utils git build-essential python3-pip libxml2-dev libxslt-dev -y
  ```

- **安装 RuyiSDK**
  根据 [RuyiSDK 官方安装指南](https://ruyisdk.org/docs/Package-Manager/installation)，在开发板上完成 Ruyi 包管理器本身的安装部署

- **安装工具链**

  ```bash
  ruyi update
  ruyi install gnu-plct
  ```


## VisionFive 2 Lite GPIO PUD 验证

- #### 示例描述和硬件环境准备

1. 示例功能：基于 libgpiod 库实现 VisionFive 2 Lite 开发板 动态配置 GPIO 31 的内部上拉/下拉电阻，并读取电平变化，验证 PUD 硬件功能。
2. 硬件环境：VisionFive 2 Lite 开发板（eMMC 版本）
3. 软件环境：Debian 12 for RISC-V 系统，已联网可正常访问外部仓库。

- #### 连接到开发板

  ```
  ssh user@172.20.10.2
  ```
  默认用户/密码：用户名 `user`，密码 `starfive`

- #### 创建并激活 ruyi 虚拟环境

  ```bash
  ruyi venv -t toolchain/gnu-plct manual ruyi-gpio-env
  . ~/ruyi-gpio-env/bin/ruyi-activate
  ```

- #### 使用 ruyi 工具链编译 GPIO PUD 测试代码

  1. **创建测试代码目录并编写代码**

     ```bash
     mkdir -p ~/pud && cd ~/pud
     nano gpio_pud_test.c
     ```

     将以下代码粘贴进`gpio_pud_test.cpp`：

     ```c
     #include <stdio.h>
     #include <stdlib.h>
     #include <unistd.h>
     #include <fcntl.h>
     #include <string.h>
     
     #define TEST_GPIO_PIN 44
     
     int gpio_export(int pin_num)
     {
         int fd = open("/sys/class/gpio/export", O_WRONLY);
         if(fd < 0)
         {
             perror("Export GPIO failed");
             return -1;
         }
         char pin_buf[8] = {0};
         snprintf(pin_buf, sizeof(pin_buf), "%d", pin_num);
         write(fd, pin_buf, strlen(pin_buf));
         close(fd);
         return 0;
     }
     
     int gpio_set_dir_in(int pin_num)
     {
         char dir_path[128] = {0};
         snprintf(dir_path, sizeof(dir_path), "/sys/class/gpio/gpio%d/direction", pin_num);
         int fd = open(dir_path, O_WRONLY);
         if(fd < 0)
             return -1;
         write(fd, "in", 2);
         close(fd);
         return 0;
     }
     
     int gpio_set_pud_mode(int pin_num, const char *mode)
     {
         char pud_path[128] = {0};
         snprintf(pud_path, sizeof(pud_path), "/sys/class/gpio/gpio%d/pull", pin_num);
         int fd = open(pud_path, O_WRONLY);
         if(fd < 0)
             return -1;
         write(fd, mode, strlen(mode));
         close(fd);
         return 0;
     }
     
     int gpio_read_value(int pin_num)
     {
         char val_path[128] = {0};
         snprintf(val_path, sizeof(val_path), "/sys/class/gpio/gpio%d/value", pin_num);
         int fd = open(val_path, O_RDONLY);
         if(fd < 0)
             return -1;
         char val_buf[2] = {0};
         read(fd, val_buf, 1);
         close(fd);
         return atoi(val_buf);
     }
     
     int main(void)
     {
         printf("==== VisionFive2 GPIO PUD Official Demo ====\n");
         printf("Compile: Ruyi GCC gnu-plct\n");
         printf("Reference: RVspace Application Note\n\n");
     
         gpio_export(TEST_GPIO_PIN);
         gpio_set_dir_in(TEST_GPIO_PIN);
         usleep(100000);
     
         gpio_set_pud_mode(TEST_GPIO_PIN, "up");
         usleep(100000);
         int level_up = gpio_read_value(TEST_GPIO_PIN);
         printf("Pull-Up Mode  | GPIO Level: %d\n", level_up);
     
         gpio_set_pud_mode(TEST_GPIO_PIN, "down");
         usleep(100000);
         int level_down = gpio_read_value(TEST_GPIO_PIN);
         printf("Pull-Down Mode| GPIO Level: %d\n", level_down);
     
         printf("\nPUD Demo Run Complete\n");
         return 0;
     }
     ```

  2. **使用 RuyiGCC 编译**

     ```bash
     riscv64-plct-linux-gnu-gcc -static -o gpio_pud_test gpio_pud_test.c
     ```


- #### 运行测试

  1. **运行测试程序**

     ```bash
     sudo ./gpio_pud_test
     ```

     **输出结果**

     ```bash
     «Ruyi ruyi-gpio-env» user@starfive:~/pud$ sudo ./gpio_pud_test
     ==== VisionFive2 GPIO PUD Official Demo ====
     Compile: Ruyi GCC gnu-plct
     Reference: RVspace Application Note
     
     Pull-Up Mode  | GPIO Level: 1
     Pull-Down Mode| GPIO Level: 1
     
     PUD Demo Run Complete
     «Ruyi ruyi-gpio-env» user@starfive:~/pud$
     ```

  2. **退出环境**

     ```bash
     cd
     ruyi-deactivate
     ```

