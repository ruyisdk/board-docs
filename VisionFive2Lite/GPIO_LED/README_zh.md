---
sys: ubuntu
sys_ver: "24.04"
sys_var: null

status: gpio
last_update: 2026-06-02

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


## VisionFive 2 Lite LED Blink基准测试

- #### 示例描述和硬件环境准备

1. 示例功能：使用 RuyiGCC 编译纯 C 程序，通过 Linux sysfs 接口控制 GPIO50 输出高低电平，实现 LED 周期性闪烁，验证 Ruyi 工具链对 GPIO 输出的编译与运行能力。
2. 硬件环境：VisionFive 2 Lite 开发板（eMMC 版本）
3. 软件环境：Debian 12 for RISC-V 系统，已联网可正常访问外部仓库。

- #### 硬件连接

1. 连接 LED 正极：将 LED 长脚（正极）串联 470Ω 电阻后，连接至开发板 40-Pin GPIO 的 引脚 22（对应 GPIO50）。

2. 连接 LED 负极：将 LED 短脚（负极）连接至任意 GND 引脚，推荐使用：

   - 引脚 6（最常用）
   - 或 引脚 9、14、20、25、30、34（备用 GND）

3. ****限流保护：****必须串联电阻**，否则可能损坏 LED 或 GPIO 引脚。

   >  **GND 冲突解决**：若引脚 6 已被串口模块占用，可将串口的 GND 线移至其他空闲 GND 引脚（如引脚 9），释放引脚 6 供 LED 使用。**不可将串口 GND 与 LED GND 并联在同一引脚**，否则会引入地线干扰导致串口通信异常。
![LED_Blink_hardware.jpg](https://github.com/zhiyao310/board-docs/blob/main/VisionFive2Lite/GPIO_LED/LED_Blink_hardware.jpg)

- #### 连接到开发板

  ```
  ssh user@172.20.10.2
  ```

  默认用户/密码：用户名 `user`，密码 `starfive`

- #### 创建并激活 ruyi 虚拟环境

  ```bash
  ruyi venv -t toolchain/gnu-plct manual led-env
  . ~/led-env/bin/ruyi-activate
  ```

- #### 使用 ruyi 工具链编译 LED Blink测试代码

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

     终止程序：按 `Ctrl+C` 即可停止。
     ![LED_Blink_test.jpg](https://github.com/zhiyao310/board-docs/blob/main/VisionFive2Lite/GPIO_LED/LED_Blink_test.jpg)

  3. **退出 Ruyi 虚拟环境**

     ```
     cd
     ruyi-deactivate
     ```

  4. **关闭开发板**

     ```
     sudo poweroff
     ```
