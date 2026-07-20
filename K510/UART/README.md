---
sys: Ubuntu 20.04.4 LTS in Docker
sys_ver: v1.9
sys_var: null

status: peripheral
last_update: 2026-07-20

model: Canaan K510 CRB-V1.2 KIT
profile: UART
---

# RuyiSDK UART示例

- 安装ruyi包管理器

```bash
sudo apt update; sudo apt install wget

wget https://mirror.iscas.ac.cn/ruyisdk/ruyi/tags/0.50.0/ruyi-0.50.0.amd64
chmod +x ./ruyi-0.50.0.amd64
sudo cp -v ./ruyi-0.50.0.amd64 /usr/local/bin/ruyi
```

- 安装工具链

```bash
ruyi update
ruyi install gnu-ruyisdk
```

## Canaan K510 CRB-V1.2 KIT UART通信测试

- #### 示例描述和硬件环境准备

1. 示例功能：基于 Linux 标准 `termios` 库，通过 `/dev/ttyS0` 串口设备节点，实现数据的发送与回显（Echo）功能。
2. 硬件环境：Canaan K510 CRB-V1.2 KIT 开发板。
3. 软件环境：K510 Buildroot 2020.02.11 (Linux 4.17)，已联网可访问外部仓库（或使用主机交叉编译方式）。

- #### 创建并激活 ruyi 虚拟环境

  ```bash
  ruyi venv -t gnu-ruyisdk generic gcc-env
  . gcc-env/bin/ruyi-activate
  ```

- #### 使用 ruyi 工具链编译 UART 测试代码

  1. **创建测试代码目录并编写代码**

     ```bash
     mkdir tes && cd tes
     nano uart_test.c
     ```

     将以下代码粘贴进` uart_test.c`：

     ```c
     #include <stdio.h>
     #include <stdlib.h>
     #include <string.h>
     #include <fcntl.h>
     #include <unistd.h>
     #include <termios.h>
     #include <errno.h>
     
     int set_uart_attr(int fd, int baud_rate) {
         struct termios options;
         if (tcgetattr(fd, &options) != 0) {
             perror("tcgetattr");
             return -1;
         }
         cfsetispeed(&options, baud_rate);
         cfsetospeed(&options, baud_rate);
         options.c_cflag &= ~PARENB;
         options.c_cflag &= ~CSTOPB;
         options.c_cflag &= ~CSIZE;
         options.c_cflag |= CS8;
         options.c_cflag |= CREAD | CLOCAL;
         options.c_lflag &= ~(ICANON | ECHO | ECHOE | ISIG);
         options.c_iflag &= ~(IXON | IXOFF | IXANY);
         options.c_iflag &= ~(INLCR | ICRNL | IGNCR);
         options.c_oflag &= ~OPOST;
         options.c_cc[VMIN] = 1;
         options.c_cc[VTIME] = 0;
         tcflush(fd, TCIOFLUSH);
         if (tcsetattr(fd, TCSANOW, &options) != 0) {
             perror("tcsetattr");
             return -1;
         }
         return 0;
     }
     
     int main(int argc, char *argv[]) {
         int fd;
         char buf[256];
         if (argc < 2) {
             fprintf(stderr, "Usage: %s <serial device>\n", argv[0]);
             return -1;
         }
         fd = open(argv[1], O_RDWR | O_NOCTTY);
         if (fd < 0) {
             perror("open");
             return -1;
         }
         printf("Opened %s\n", argv[1]);
         if (set_uart_attr(fd, B115200) < 0) {
             close(fd);
             return -1;
         }
         printf("Configured: 115200 8N1\n");
     
         char *send = "Hello from K510 UART!\n";
         write(fd, send, strlen(send));
         printf("Sent: %s", send);
     
         while (1) {
             int n = read(fd, buf, sizeof(buf)-1);
             if (n > 0) {
                 buf[n] = '\0';
                 printf("Received: %s", buf);
                 write(fd, buf, n); // echo back
             }
         }
         close(fd);
         return 0;
     }
     ```
  
  2. **使用 RuyiGCC 编译**
  
     ```bash
     riscv64-ruyisdk-linux-gnu-gcc -static uart_test.c -o uart_test
     ```
  
  3. **剥离属性段**
  
     ```bash
     riscv64-ruyisdk-linux-gnu-objcopy --remove-section=.riscv.attributes uart_test uart_test_stripped
     ```


- #### 传输

  1. **获取主板IP**

     ```bash
     ip addr show
     # 一般在eno1中的inet有：如10.13.21.160
     ```

  2. **PC端传输**

     ```bash
     python3 -m http.server 8000
     ```

  3. **另起一终端窗口进入开发板**

     ```
     sudo minicom
     ```

  4. **下载并运行测试**

     ```bash
     wget http://10.13.21.160:8000/uart_test_stripped -O /root/uart_test
     chmod +x /root/uart_test
     ```
     
  
- #### 运行测试

  ```bash
  /root/uart_test /dev/ttyS0
  ```

  **输出结果**

  - **minicom**

    ```bash
    [root@canaan ~ ]$ wget http://10.13.21.160:8000/uart_test_stripped -O /root/uart
    _test
    Connecting to 10.13.21.160:8000 (10.13.21.160:8000)
    saving to '/root/uart_test'
    uart_test            100% |********************************| 3170k  0:00:00 ETA
    '/root/uart_test' saved
    [root@canaan ~ ]$ chmod +x /root/uart_test
    [root@canaan ~ ]$ /root/uart_test /dev/ttyS0
    Opened /dev/ttyS0Configured: 115200 8N1
                                           Hello from K510 UART!
                                                                Sent: Hello from K5!
    ```
    ​

