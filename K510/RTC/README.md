---
sys: Ubuntu 20.04.4 LTS in Docker
sys_ver: v1.9
sys_var: null

status: system
last_update: 2026-06-18

model: Canaan K510 CRB-V1.2 KIT
profile: RTC

---

# RuyiSDK 系统示例

- 安装ruyi包管理器

```bash
sudo apt update; sudo apt install wget

wget https://mirror.iscas.ac.cn/ruyisdk/ruyi/tags/0.49.0/ruyi-0.49.0.riscv64
chmod +x ./ruyi-0.49.0.riscv64
sudo cp -v ./ruyi-0.49.0.riscv64 /usr/local/bin/ruyi
```

- 安装工具链

```bash
ruyi update
ruyi install gnu-plct llvm-plct
```

## Canaan K510 CRB-V1.2 KIT RTC 验证

- #### 示例描述和硬件环境准备

1. 示例功能：基于 Linux RTC 驱动，通过 `/dev/rtc0` 设备节点，使用标准 `ioctl` 接口设置和读取硬件实时时钟时间。
2. 硬件环境：Canaan K510 CRB-V1.2 KIT 开发板。
3. 软件环境：K510 Buildroot 2020.02.11 (Linux 4.17)，已联网可访问外部仓库（或使用主机交叉编译方式）。

- #### 创建并激活 ruyi 虚拟环境

  ```bash
  ruyi venv --toolchain gnu-plct generic gcc-env
  . gcc-env/bin/ruyi-activate
  ```

- #### 使用 ruyi 工具链编译 RTC 测试代码

  1. **创建测试代码目录并编写代码**

     ```bash
     mkdir demo && cd demo
     nano rtc_demo.c
     ```

     将以下代码粘贴进`rtc_demo.c`：

     ```c
     #include <stdio.h>
     #include <stdlib.h>
     #include <fcntl.h>
     #include <unistd.h>
     #include <errno.h>
     #include <linux/rtc.h>
     #include <sys/ioctl.h>
     
     int main(int argc, char *argv[])
     {
         int fd, retval;
         struct rtc_time rtc_tm;
         int year, month, day, hour, minute, second;
     
         /* 解析参数：年月日 时分秒 */
         if (argc != 3) {
             fprintf(stdout, "usage:\t ./rtc year-month-day hour:minute:second\n");
             fprintf(stdout, "example: ./rtc 2021-10-11 19:54:30\n");
             return -1;
         }
         sscanf(argv[1], "%d-%d-%d", &year, &month, &day);
         sscanf(argv[2], "%d:%d:%d", &hour, &minute, &second);
     
         /* 打开 RTC 设备 */
         fd = open("/dev/rtc0", O_RDONLY);
         if (fd == -1) {
             perror("/dev/rtc0");
             exit(errno);
         }
     
         /* 设置 RTC 时间 */
         rtc_tm.tm_year = year - 1900;
         rtc_tm.tm_mon = month - 1;
         rtc_tm.tm_mday = day;
         rtc_tm.tm_hour = hour;
         rtc_tm.tm_min = minute;
         rtc_tm.tm_sec = second;
     
         retval = ioctl(fd, RTC_SET_TIME, &rtc_tm);
         if (retval == -1) {
             perror("ioctl");
             exit(errno);
         }
     
         /* 等待 2 秒 */
         sleep(2);
     
         /* 读取 RTC 当前时间 */
         retval = ioctl(fd, RTC_RD_TIME, &rtc_tm);
         if (retval == -1) {
             perror("ioctl");
             exit(errno);
         }
     
         /* 打印 RTC 当前时间 */
         fprintf(stdout, "\nRTC date/time: %d/%d/%d %02d:%02d:%02d\n",
                 rtc_tm.tm_mday, rtc_tm.tm_mon + 1, rtc_tm.tm_year + 1900,
                 rtc_tm.tm_hour, rtc_tm.tm_min, rtc_tm.tm_sec);
     
         close(fd);
         return 0;
     }  
     ```

  2. **使用 RuyiGCC 编译**

     ```bash
     riscv64-plct-linux-gnu-gcc -static rtc_demo.c -o rtc
     ```

  3. **剥离属性段**

     ```bash
     riscv64-linux-gnu-objcopy --remove-section=.riscv.attributes rtc rtc_stripped
     ```


- #### 传输并运行测试

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
     wget http://10.13.61.37:8000/rtc_stripped -O /root/rtc
     chmod +x /root/rtc
     
     # 关闭内核日志（避免干扰输出）
     echo 0 > /proc/sys/kernel/printk
     
     /root/rtc 2026-06-18 15:50:00
     ```

     输出结果

     ```bash
     [root@canaan ~ ]$ wget http://10.13.21.160:8000/rtc_stripped -O /root/rtc
     Connecting to 10.13.21.160:8000 (10.13.21.160:8000)
     saving to '/root/rtc'
     rtc                  100% |********************************| 3605k  0:00:00 ETA
     '/root/rtc' saved
     [root@canaan ~ ]$ chmod +x /root/rtc
     [root@canaan ~ ]$ echo 0 > /proc/sys/kernel/printk
     [root@canaan ~ ]$ /root/rtc 2026-06-18 16:00:00
     
     RTC date/time: 18/6/2026 16:00:02
     [root@canaan ~ ]$ 
     ```

- #### 退出环境

  ```bash
  cd
  ruyi-deactivate
  ```

  
