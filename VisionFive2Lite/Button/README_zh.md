---
sys: ubuntu
sys_ver: "24.04"
sys_var: null

status: peripheral
last_update: 2026-07-20

model: VisionFive2 Lite
profile: GPIO_Button
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
  ruyi install gnu-ruyisdk
  ```


## VisionFive 2 Lite 基础按键检测

- #### 示例描述和硬件环境准备

1. 示例功能：使用 C 语言通过 Linux GPIO 子系统检测按键的按下与释放事件，利用 `poll()` 实现边沿触发中断式检测，并包含防抖动处理。
2. 硬件环境：VisionFive 2 Lite 开发板（eMMC 版本）
3. 软件环境：Debian 12 for RISC-V 系统，已联网可正常访问外部仓库。

- #### 硬件连接

1. 将轻触开关插入面包板，确保引脚处于对角线位置。
2. 使用公对母杜邦线连接：
   - 按键的 **Pin ④** → 开发板 40-Pin GPIO 的 **Pin 37 (GPIO60)**
   - 按键的 **Pin ③** → 开发板的 **Pin 39 (GND)**
3. （可选）在 GPIO60 与 3.3V 之间连接一个 10kΩ 上拉电阻，确保未按下时电平为高。

  ![device-connect.jpg](https://github.com/zhiyao310/board-docs/blob/add-documents-K510-VF2Lite/VisionFive2Lite/Button/device-connect.jpg)
- #### 连接到开发板

  ```
  ssh user@172.20.10.2
  ```

  默认用户/密码：用户名 `user`，密码 `starfive`

- #### 创建并激活 ruyi 虚拟环境

  ```bash
  ruyi venv -t gnu-ruyisdk manual venv-gnu-ruyisdk
  . venv-gnu-ruyisdk/bin/ruyi-activate
  ```

- #### 使用 ruyi 工具链编译 GPIO_Button测试代码

  1. **创建测试代码目录并编写代码**

     ```bash
     mkdir -p ~/button && cd ~/button
     nano key_detection.c
     ```

     将以下代码粘贴进`key_detection.c`：

     ```c
     #include <stdio.h>
     #include <stdlib.h>
     #include <unistd.h>
     #include <fcntl.h>
     #include <string.h>
     #include <errno.h>
     #include <poll.h>

     #define GPIO_BASE_PATH "/sys/class/gpio"
     #define GPIO_PIN "60"           
     #define GPIO_DIRECTION "in"
     #define GPIO_EDGE "both"       

     int write_to_file(const char *path, const char *value) {
         int fd = open(path, O_WRONLY);
         if (fd < 0) return -1;
         int len = write(fd, value, strlen(value));
         close(fd);
         return (len < 0) ? -1 : 0;
     }

     int read_from_file(const char *path, char *buffer, size_t size) {
         int fd = open(path, O_RDONLY);
         if (fd < 0) return -1;
         ssize_t bytes = read(fd, buffer, size - 1);
         close(fd);
         if (bytes < 0) return -1;
         buffer[bytes] = '\0';
         return 0;
     }

     int export_gpio(const char *pin) {
         if (write_to_file(GPIO_BASE_PATH "/export", pin) < 0) {
             if (errno == EBUSY) return 0; 
             perror("Export GPIO failed");
             return -1;
         }
         usleep(100000);
         return 0;
     }

     int unexport_gpio(const char *pin) {
         if (write_to_file(GPIO_BASE_PATH "/unexport", pin) < 0) {
             perror("Unexport GPIO failed");
             return -1;
         }
         return 0;
     }

     int set_gpio_direction(const char *pin, const char *direction) {
         char path[128];
         snprintf(path, sizeof(path), GPIO_BASE_PATH "/gpio%s/direction", pin);
         if (write_to_file(path, direction) < 0) {
             perror("Set direction failed");
             return -1;
         }
         return 0;
     }

     int set_gpio_edge(const char *pin, const char *edge) {
         char path[128];
         snprintf(path, sizeof(path), GPIO_BASE_PATH "/gpio%s/edge", pin);
         if (write_to_file(path, edge) < 0) {
             return 0;
         }
         return 0;
     }

     int main() {
         char value_path[128];
         struct pollfd fdset;
         char buffer[4] = {0};
         int gpio_fd;

         printf("\n=== VisionFive 2 Lite 基础按键检测 (RuyiGCC) ===\n");
         printf("监控 GPIO Pin %s (开发板 Pin 37) ...\n", GPIO_PIN);
         printf("检测双边沿事件 (按下和释放)[reference:11]\n");
         printf("按 Ctrl+C 退出程序\n\n");

         if (export_gpio(GPIO_PIN) < 0) return 1;
         if (set_gpio_direction(GPIO_PIN, GPIO_DIRECTION) < 0) {
             unexport_gpio(GPIO_PIN);
             return 1;
         }
         if (set_gpio_edge(GPIO_PIN, GPIO_EDGE) < 0) {
         }

         snprintf(value_path, sizeof(value_path), GPIO_BASE_PATH "/gpio%s/value", GPIO_PIN);
         gpio_fd = open(value_path, O_RDONLY);
         if (gpio_fd < 0) {
             perror("Open value file failed");
             unexport_gpio(GPIO_PIN);
             return 1;
         }

         read(gpio_fd, buffer, sizeof(buffer) - 1);
         lseek(gpio_fd, 0, SEEK_SET);

         fdset.fd = gpio_fd;
         fdset.events = POLLPRI; 

         printf("等待按键事件 ...\n");

         while (1) {
             int ret = poll(&fdset, 1, -1); 

             if (ret < 0) {
                 perror("poll failed");
                 break;
             }

             if (fdset.revents & POLLPRI) {
                 lseek(gpio_fd, 0, SEEK_SET);
                 read(gpio_fd, buffer, sizeof(buffer) - 1);
                 int value = atoi(buffer);

                 printf("*-----------------------------------*\n");
                 if (value == 0) {
                     printf("Falling edge detected on pin %s ! (按键按下)\n", GPIO_PIN);
                 } else {
                     printf("Rising edge detected on pin %s ! (按键释放)\n", GPIO_PIN);
                 }
                 printf("*-----------------------------------*\n");
             }
         }

         close(gpio_fd);
         unexport_gpio(GPIO_PIN);
         printf("\n程序退出\n");
         return 0;
     }
     ```

  2. **使用 RuyiGCC 编译**

     ```bash
     riscv64-ruyisdk-linux-gnu-gcc -static -o key_detection key_detection.c
     ```


- #### 运行测试

  1. **运行测试程序**

     ```bash
     sudo ./key_detection
     ```

     **输出结果**（按下/释放按键时）：

     ```bash
     «Ruyi venv-gnu-ruyisdk» user@starfive:~/button$ sudo ./key_detection
     
     === VisionFive 2 Lite 基础按键检测 (RuyiGCC) ===
     监控 GPIO Pin 60 (开发板 Pin 37) ...
     检测双边沿事件 (按下和释放)[reference:11]
     按 Ctrl+C 退出程序
     
     等待按键事件 ...
     *-----------------------------------*
     Falling edge detected on pin 60 ! (按键按下)
     *-----------------------------------*
     *-----------------------------------*
     Rising edge detected on pin 60 ! (按键释放)
     *-----------------------------------*
     *-----------------------------------*
     Falling edge detected on pin 60 ! (按键按下)
     *-----------------------------------*
     *-----------------------------------*
     Rising edge detected on pin 60 ! (按键释放)
     *-----------------------------------*
     ^C
     «Ruyi venv-gnu-ruyisdk» user@starfive:~/button$
     ```
  
     终止程序：按 `Ctrl+C` 即可停止。
  
  2. **退出 Ruyi 虚拟环境**
  
     ```
     cd
     ruyi-deactivate
     ```
  
  3. **关闭开发板**
  
     ```
     sudo poweroff
     ```
