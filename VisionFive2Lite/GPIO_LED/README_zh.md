---
sys: ubuntu
sys_ver: "24.04"
sys_var: null

status: gpio
last_update: 2026-05-24

model: VisionFive2 Lite
profile: GPIO_LED Blink

---

#  RuyiSDK GPIO示例

- **安装依赖包**

  ```bash
  sudo apt update
  sudo apt install -y libgpiod-dev
  ```

- **安装 RuyiSDK**
  根据 [RuyiSDK 官方安装指南](https://ruyisdk.org/docs/Package-Manager/installation)，在开发板上完成 Ruyi 包管理器本身的安装部署

- **安装工具链**

  ```bash
  ruyi update
  ruyi install gnu-plct
  ```


## VisionFive 2 Lite LED 闪烁基准测试

- #### 示例描述和硬件环境准备

1. 示例功能：使用 RuyiGCC 编译纯 C 程序，通过 Linux sysfs 接口控制 GPIO50 输出高低电平，实现 LED 周期性闪烁，验证 Ruyi 工具链对 GPIO 输出的编译与运行能力。
2. 硬件环境：VisionFive 2 Lite 开发板（eMMC 版本）
3. 软件环境：Debian 12 for RISC-V 系统，已联网可正常访问外部仓库。

- #### 创建并激活 ruyi 虚拟环境

  ```bash
  ruyi venv -t toolchain/gnu-plct manual led-env
  . ~/led-env/bin/ruyi-activate
  ```

- #### 使用 ruyi 工具链编译 GPIO PUD 测试代码

  1. **创建测试代码目录并编写代码**

     ```bash
     mkdir -p ~/led && cd ~/led
     nano led_blink.c
     ```

     将以下代码粘贴进`led_blink.c`：

     ```c
     #include <stdio.h>
     #include <stdlib.h>
     #include <unistd.h>
     #include <fcntl.h>
     #include <string.h>
     
     #define GPIO_PIN 50
     #define DELAY_SECOND 1
     
     int gpio_export(int pin) {
         int fd = open("/sys/class/gpio/export", O_WRONLY);
         if (fd < 0) return -1;
         char buf[4];
         snprintf(buf, sizeof(buf), "%d", pin);
         write(fd, buf, strlen(buf));
         close(fd);
         return 0;
     }
     
     int gpio_set_output(int pin) {
         char path[128];
         snprintf(path, sizeof(path), "/sys/class/gpio/gpio%d/direction", pin);
         int fd = open(path, O_WRONLY);
         if (fd < 0) return -1;
         write(fd, "out", 3);
         close(fd);
         return 0;
     }
     
     int gpio_set_value(int pin, int val) {
         char path[128];
         snprintf(path, sizeof(path), "/sys/class/gpio/gpio%d/value", pin);
         int fd = open(path, O_WRONLY);
         if (fd < 0) return -1;
         char v = val ? '1' : '0';
         write(fd, &v, 1);
         close(fd);
         return 0;
     }
     
     int main() {
         printf("=========================================\n");
         printf("VisionFive 2 Lite LED Blink (RuyiGCC)\n");
         printf("GPIO: %d (Physical Pin 22)\n", GPIO_PIN);
         printf("=========================================\n");
     
         gpio_export(GPIO_PIN);
         gpio_set_output(GPIO_PIN);
         sleep(1);
     
         while (1) {
             gpio_set_value(GPIO_PIN, 1);
             printf("LED ON\n");
             sleep(DELAY_SECOND);
     
             gpio_set_value(GPIO_PIN, 0);
             printf("LED OFF\n");
             sleep(DELAY_SECOND);
         }
     
         return 0;
     }
     ```

  2. **使用 RuyiGCC 编译**

     ```bash
     riscv64-plct-linux-gnu-gcc led_blink.c -o led_blink
     ```


- #### 运行测试

  1. **运行测试程序**

     ```bash
     sudo ./led_blink
     ```

     **输出结果**

     ```bash
     «Ruyi led-env» user@starfive:~/led$ sudo ./led_blink
     [sudo] password for user:
     =========================================
     VisionFive 2 Lite LED Blink (RuyiGCC)
     GPIO: 50 (Physical Pin 22)
     =========================================
     LED ON
     LED OFF
     LED ON
     LED OFF
     LED ON
     LED OFF
     ...
     ```

  2. **退出环境**

     ```bash
     cd
     ruyi-deactivate
     ```

