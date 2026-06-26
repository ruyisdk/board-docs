---
sys: Ubuntu 20.04.4 LTS in Docker
sys_ver: v1.9
sys_var: null

status: gpio
last_update: 2026-06-25

model: Canaan K510 CRB-V1.2 KIT
profile: GPIO_KEYS

---

# RuyiSDK GPIO功能示例

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

## Canaan K510 CRB-V1.2 KIT GPIO KEYS Demo

- #### 示例描述和硬件环境准备

1. 示例功能：基于 Linux input 子系统，读取 K510 开发板上的物理按键（`KEY0`、`KEY1`）事件，打印按键码、按下/释放动作及持续时长。
2. 硬件环境：Canaan K510 CRB-V1.2 KIT 开发板。
3. 软件环境：K510 Buildroot 2020.02.11 (Linux 4.17)，已联网可访问外部仓库（或使用主机交叉编译方式）。

- #### 创建并激活 ruyi 虚拟环境

  ```bash
  ruyi venv --toolchain gnu-plct generic gcc-env
  . gcc-env/bin/ruyi-activate
  ```

- #### 使用 ruyi 工具链编译 GPIO KEYS 测试代码

  1. **创建测试代码目录并编写代码**

     ```bash
     mkdir demo && cd demo
     nano gpio_keys_demo.c
     ```

     将以下代码粘贴进`gpio_keys_demo.c`：

     ```c
     #include <stdio.h>
     #include <stdlib.h>
     #include <string.h>
     #include <unistd.h>
     #include <fcntl.h>
     #include <errno.h>
     #include <linux/input.h>
     #include <sys/time.h>
     
     /* 按键状态 */
     #define KEY_PRESSED   1
     #define KEY_RELEASED  0
     
     /* 按键动作描述 */
     static const char *get_key_action(int value)
     {
         if (value == KEY_PRESSED)
             return "PRESSED";
         else if (value == KEY_RELEASED)
             return "RELEASED";
         else
             return "UNKNOWN";
     }
     
     int main(int argc, char *argv[])
     {
         int fd;
         struct input_event ev;
         struct timeval start_time, end_time;
         long duration_ms;
         int key_down = 0;
         unsigned int last_key_code = 0;
     
         /* 参数检查：需要指定 input 设备路径 */
         if (argc != 2) {
             fprintf(stderr, "Usage: %s <input_device>\n", argv[0]);
             fprintf(stderr, "Example: %s /dev/input/event0\n", argv[0]);
             fprintf(stderr, "\nHint: Run 'cat /proc/bus/input/devices' to find the correct event node.\n");
             return -1;
         }
     
         /* 打开 input 设备 */
         fd = open(argv[1], O_RDONLY);
         if (fd == -1) {
             perror("open");
             fprintf(stderr, "Failed to open %s. Please check device path and permissions.\n", argv[1]);
             return -1;
         }
     
         printf("GPIO_KEYS Demo started. Monitoring %s ...\n", argv[1]);
         printf("Press any key on the board. Press Ctrl+C to exit.\n\n");
     
         /* 主循环：阻塞式读取按键事件 */
         while (1) {
             memset(&ev, 0, sizeof(ev));
     
             /* 阻塞读取一个 input 事件 */
             if (read(fd, &ev, sizeof(ev)) < 0) {
                 perror("read");
                 close(fd);
                 return -1;
             }
     
             /* 只处理 EV_KEY 类型事件（按键事件） */
             if (ev.type == EV_KEY) {
                 /* 记录按键按下时间 */
                 if (ev.value == KEY_PRESSED) {
                     gettimeofday(&start_time, NULL);
                     key_down = 1;
                     last_key_code = ev.code;
                     printf("[%ld.%06ld] KEY CODE: %-4u ACTION: %s\n",
                            start_time.tv_sec, start_time.tv_usec,
                            ev.code, get_key_action(ev.value));
                 }
                 /* 按键释放时计算持续时间 */
                 else if (ev.value == KEY_RELEASED && key_down && ev.code == last_key_code) {
                     gettimeofday(&end_time, NULL);
                     duration_ms = (end_time.tv_sec - start_time.tv_sec) * 1000 +
                                   (end_time.tv_usec - start_time.tv_usec) / 1000;
                     printf("[%ld.%06ld] KEY CODE: %-4u ACTION: %s DURATION: %ld ms\n",
                            end_time.tv_sec, end_time.tv_usec,
                            ev.code, get_key_action(ev.value), duration_ms);
                     key_down = 0;
                 }
                 /* 其他情况（如重复事件） */
                 else if (ev.value == 2) {
                     /* 长按重复事件，可选择打印 */
                     /* printf("[*] KEY CODE: %u REPEAT\n", ev.code); */
                 }
             }
         }
     
         close(fd);
         return 0;
     }
     ```

  2. **使用 RuyiGCC 编译**

     ```bash
     riscv64-plct-linux-gnu-gcc -static -o gpio_keys gpio_keys_demo.c
     ```

  3. **剥离属性段**

     ```bash
     riscv64-plct-linux-gnu-objcopy --remove-section=.riscv.attributes gpio_keys gpio_keys_stripped
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
     wget http://10.13.21.160:8000/gpio_keys_stripped -O /root/gpio
     _keys_stripped
     chmod +x /root/gpio_keys_stripped
     
     # 查看 GPIO 按键对应的 input 事件节点
     cat /proc/bus/input/devices
     # 找到含有 "gpio-keys" 的条目，记下对应的 event 编号（如 event1）
     
     # 运行测试程序（指定事件节点）
     /root/gpio_keys_stripped /dev/input/event1
     ```

     输出结果

     ```bash
     [root@canaan ~ ]$ wget http://10.13.21.160:8000/gpio_keys_stripped -O /root/gpio
     _keys_stripped
     Connecting to 10.13.21.160:8000 (10.13.21.160:8000)
     saving to '/root/gpio_keys_stripped'
     gpio_keys_stripped   100% |********************************| 3191k  0:00:00 ETA
     '/root/gpio_keys_stripped' saved
     [root@canaan ~ ]$ chmod +x /root/gpio_keys_stripped
     [root@canaan ~ ]$ cat /proc/bus/input/devices
     I: Bus=0018 Vendor=0416 Product=038f Version=1060
     N: Name="Goodix Capacitive TouchScreen"
     P: Phys=input/ts
     S: Sysfs=/devices/platform/99900000.noc_bus/99900000.noc_bus:apb_bus/99900000.noc_bus:apb_0
     U: Uniq=
     H: Handlers=kbd event0 
     B: PROP=2
     B: EV=b
     B: KEY=400 0 0 0 2000000000000000 0
     B: ABS=265800000000003
     
     I: Bus=0019 Vendor=0001 Product=0001 Version=0100
     N: Name="99900000.noc_bus:gpio-keys"
     P: Phys=gpio-keys/input0
     S: Sysfs=/devices/platform/99900000.noc_bus/99900000.noc_bus:gpio-keys/input/input1
     U: Uniq=
     H: Handlers=kbd event1 
     B: PROP=0
     B: EV=3
     B: KEY=1000040000000
     
     [root@canaan ~ ]$ /root/gpio_keys_stripped /dev/input/event1
     GPIO_KEYS Demo started. Monitoring /dev/input/event1 ...
     Press any key on the board. Press Ctrl+C to exit.
     
     [1291173014.801218] KEY CODE: 48   ACTION: PRESSED
     [1291173014.986088] KEY CODE: 48   ACTION: RELEASED DURATION: 184 ms
     [1291173019.298035] KEY CODE: 30   ACTION: PRESSED
     [1291173019.515556] KEY CODE: 30   ACTION: RELEASED DURATION: 217 ms
     ```

- #### **退出环境**

```bash
cd
ruyi-deactivate
```
