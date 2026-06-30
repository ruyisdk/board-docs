---
sys: FreeRTOS
sys_ver: 

status: gui
last_update: 2026-05-29

model: ESP32-P4-Function-EV-Board
profile: LVGL_Demo_v8

---

# RuyiSDK 图形界面示例

> 说明：ESP32-P4 硬件驱动依赖乐鑫官方 IDF 工具链。本示例中，RuyiSDK 仅用于虚拟环境管理、源码获取和编辑，编译烧录仍使用 `idf.py` 命令。

## 环境准备

- **安装依赖包**

  ```bash
  sudo apt update && sudo apt install -y git cmake
  ```

- **安装 ESP-IDF**

  根据 [ESP-IDF 编程指南](https://docs.espressif.com/projects/esp-idf/zh_CN/v5.5/esp32p4/get-started/index.html)，完成 ESP-IDF v5.5.x 的安装和环境配置。

  ```bash
  git clone --depth 1 --branch release/v5.5 https://github.com/espressif/esp-idf.git
  cd esp-idf
  ./install.sh esp32p4
  source export.sh
  ```

- **安装 RuyiSDK**
  根据 [RuyiSDK 官方安装指南](https://ruyisdk.org/docs/Package-Manager/installation)，在开发板上完成 Ruyi 包管理器本身的安装部署

- **安装工具链**

  ```bash
  ruyi update
  ruyi install gnu-plct-xthead
  python $IDF_PATH/tools/idf_tools.py install --targets=esp32p4
  ```


## ESP32-P4 LVGL Demo v8

- #### 示例描述和硬件环境准备

  1. **示例功能**：基于 LVGL v8 实现嵌入式图形界面演示，包括性能基准测试 、控件展示 、音乐播放器、压力测试四个 Demo，验证 ESP-IDF + RISC-V GCC 在 ESP32-P4-Function-EV-Board 上的 LVGL 编译与运行能力。

  2. **硬件环境**：

     - ESP32-P4-Function-EV-Board 开发板
     - MIPI-DSI 接口 LCD 显示屏
     - GT911 电容触摸屏

  3. **软件环境**：

     - ESP-IDF v5.5

  4. **芯片版本适配**：

     在编译前，请确认开发板芯片版本（查看 PCB 丝印或芯片 Mark 标识），在 `sdkconfig.defaults` 中配置正确的版本：

     | 芯片版本    | sdkconfig 配置                                               |
     | ----------- | ------------------------------------------------------------ |
     | v0.1        | `CONFIG_ESP32P4_SELECTS_REV_LESS_V3=y` + `CONFIG_ESP32P4_REV_MIN_1=y` |
     | v1.0        | `CONFIG_ESP32P4_SELECTS_REV_LESS_V3=y` + `CONFIG_ESP32P4_REV_MIN_100=y` |
     | v3.1 (默认) | `CONFIG_ESP32P4_REV_MIN_301=y`                               |

- #### 配置与编译

  1. **创建并激活虚拟环境**

     ```
     ruyi venv -t toolchain/gnu-plct manual venv-gnu-plct
     . venv-gnu-plct/bin/ruyi-activate
     ```

  2. **获取项目源码**

     ```bash
     git clone --recursive https://github.com/espressif/esp-dev-kits.git
     ```

     > 为避免 Windows 长路径限制，将项目复制到短路径：
     >
     > ```bash
     > cp -r lvgl_demo_v8 /d/p4/lvgl_demo_v8
     > ```

  3. **进入项目目录**

     ```bash
     cd lvgl_demo_v8
     ```

  4. **配置项目**

     ```bash
     # 设置目标芯片
     idf.py set-target esp32p4
     # 配置项目选项
     idf.py menuconfig
     ```

  5. **编译项目**

     ```bash
     # 完整清理编译
     idf.py fullclean
     # 编译
     idf.py build
     ```

     **输出结果**

     ```text
     Project build complete.
     lvgl_demo_v8.bin binary size 0xb41d0 bytes. Smallest app partition is 0x800000 bytes. 0x74be30 bytes (91%) free.
     ```

  6. **切换 Demo 类型**

     编辑 `main/main.c` 文件：

     ```c
     void app_main(void)
     {
         // ...初始化代码...
     
         // lv_demo_music();     
         lv_demo_benchmark();    
         // lv_demo_widgets();   
         // lv_demo_stress();     
     
         esp_lv_adapter_unlock();
     }
     ```

     修改后重新执行 `idf.py build` 编译。

- #### 烧录固件

  1. **连接开发板**

     使用 USB Type-C 数据线连接开发板的 UART 接口到电脑，确认串口设备：Windows通常显示为 `COM6`。

  2. **烧录**

     ```bash
     idf.py -p COM6 flash
     ```

     > 如遇监视器崩溃，设置编码后启动：
     >
     > ```bash
     > export PYTHONIOENCODING=utf-8
     > python $IDF_PATH/tools/idf_monitor.py -p COM6 -b 115200 \
     > --toolchain-prefix riscv32-esp-elf- --target esp32p4 \
     > --revision 100 build/lvgl_demo_v8.elf
     > ```

- #### 运行测试

  1. **启动日志**

     ```text
     ESP-ROM:esp32p4-eco2-20240710
     Build:Jul 10 2024
     rst:0x1 (POWERON),boot:0x30f (SPI_FAST_FLASH_BOOT)
     SPI mode:DIO, clock div:2
     
     I (28) boot: ESP-IDF v5.5.4 2nd stage bootloader
     I (30) boot: chip revision: v1.0
     I (39) boot.esp32p4: SPI Speed      : 40MHz
     I (47) boot.esp32p4: SPI Mode       : QIO
     I (51) boot.esp32p4: SPI Flash Size : 16MB
     
     I (288) esp_psram: Found 32MB PSRAM device
     I (292) esp_psram: Speed: 200MHz
     I (986) cpu_start: Pro cpu start user code
     I (987) cpu_start: cpu freq: 360000000 Hz
     
     I (1131) ESP32_P4_EV: Install EK79007 LCD control panel
     I (1136) ek79007: version: 2.0.2
     I (1310) ESP32_P4_EV: Display initialized
     I (1311) esp_lvgl:adapter: LVGL adapter initialized successfully
     I (1344) GT911: TouchPad_ID:0x39,0x31,0x31
     I (1347) GT911: TouchPad_Config_Version:89
     I (1350) esp_lvgl:touch: Touch input device registered successfully
     I (1370) esp_lvgl:adapter: LVGL task started successfully
     I (1375) ESP32_P4_EV: Setting LCD backlight: 100%
     I (1388) main_task: Returned from app_main()
     ```

  2. **屏幕显示验证**

     烧录成功后，开发板 MIPI-DSI 屏幕将显示 LVGL 演示界面：

     - **Benchmark**: 显示 FPS 帧率、CPU 占用、GPU 填充率等实时性能数据
     - **Widgets**: 展示 LVGL 全部控件（按钮、滑块、图表、列表等）
     - **Music**: 显示音乐播放器界面（音频编解码 + 频谱可视化）
     - **Stress**: 持续进行图形渲染压力测试

     触摸屏应能正常响应手指滑动和点击操作。
     
