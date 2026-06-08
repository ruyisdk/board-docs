---
sys: FreeRTOS
sys_ver: 

status: lvgl
last_update: 2026-05-29

model: ESP32-P4-Function-EV-Board
profile: LVGL Demo v9

---

# RuyiSDK LVGL 示例

> 说明：ESP32-P4 硬件驱动依赖乐鑫官方 IDF 工具链。本示例中，RuyiSDK 仅用于虚拟环境管理、源码获取和编辑，编译烧录仍使用 `idf.py` 命令。

## 环境准备

- **安装依赖包**

  ```bash
  sudo apt update && sudo apt install -y git cmake
  ```

- **安装 ESP-IDF**

  根据 [ESP-IDF 编程指南](https://docs.espressif.com/projects/esp-idf/zh_CN/v5.5/esp32p4/get-started/index.html)，完成 ESP-IDF v5.5 的安装和环境配置。

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

## ESP32-P4 LVGL Demo v9

- #### 示例描述和硬件环境准备

  1. **示例功能**：基于 LVGL v9 实现嵌入式图形界面演示，包括性能基准测试、控件展示 、音乐播放器 、压力测试、渲染测试 、滚动测试、变换测试、Flex 布局 、多语言共九个 Demo。

  2. **硬件环境**：

     - ESP32-P4-Function-EV-Board 开发板（ESP32-P4 芯片）
     - MIPI-DSI 接口 LCD 显示屏（1024x600，EK79007 驱动）
     - GT911 电容触摸屏（I2C 接口）

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

  3. **进入项目目录**

     ```bash
     cd lvgl_demo_v9
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
     lvgl_demo_v9.bin binary size 0x110fb0 bytes. Smallest app partition is 0x800000 bytes. 0x6ef050 bytes (87%) free.
     ```

  6. **切换 Demo 类型**

     编辑 `main/main.c` 文件：

     ```c
     void app_main(void)
     {
         // ...初始化代码...
     
         // lv_demo_music();          // 音乐播放器：音频解码 + 界面交互
         lv_demo_benchmark();         // 性能测试：FPS + 填充率
         // lv_demo_widgets();        // 控件展示：全部 LVGL 控件
         // lv_demo_stress();         // 压力测试：持续重绘
         // lv_demo_render();         // 渲染测试 (v9 新增)
         // lv_demo_scroll();         // 滚动测试 (v9 新增)
         // lv_demo_transform();      // 变换测试 (v9 新增)
         // lv_demo_flex_layout();    // Flex 布局 Demo (v9 新增)
         // lv_demo_multilang();      // 多语言 Demo (v9 新增)
     
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

     **输出结果**

     ```text
     Serial port COM6
     Connecting...
     Connected to ESP32-P4 on COM6
     Chip type:          ESP32-P4 (revision v1.0)
     Features:           Dual Core + LP Core, 400MHz
     Crystal frequency:  40MHz
     
     Wrote 1118128 bytes (608096 compressed) at 0x00010000 in 16.8 seconds (531.0 kbit/s).
     Hash of data verified.
     
     Hard resetting via RTS pin...
     ```

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
     
     I (565) mmu_psram: .rodata xip on psram
     I (604) mmu_psram: .text xip on psram
     I esp_psram: Found 32MB PSRAM device
     I esp_psram: Speed: 200MHz
     I (1073) cpu_start: Pro cpu start user code
     I (1073) cpu_start: cpu freq: 360000000 Hz
     
     I (1208) ESP32_P4_EV: MIPI DSI PHY Powered on
     I (1217) ESP32_P4_EV: Install EK79007 LCD control panel
     I (1222) ek79007: version: 2.0.2
     I (1395) ESP32_P4_EV: Display initialized
     I (1395) esp_lvgl:adapter: LVGL adapter initialized successfully
     I (1397) esp_lvgl:bridge_v9: Initializing hardware resources
     I (1429) GT911: TouchPad_ID:0x39,0x31,0x31
     I (1436) esp_lvgl:touch: Touch input device registered successfully
     I (1455) esp_lvgl:adapter: LVGL task started successfully
     I (1460) ESP32_P4_EV: Setting LCD backlight: 100%
     I (1466) main_task: Returned from app_main()
     ```

  2. **屏幕显示验证**

     烧录成功后，开发板 MIPI-DSI 屏幕将显示 LVGL v9 演示界面：

     - **Benchmark**: 显示 FPS 帧率、CPU 占用、GPU 填充率等实时性能数据
     - **Widgets**: 展示 LVGL 全部控件（按钮、滑块、图表、列表等）
     - **Music**: 显示音乐播放器界面（音频编解码 + 频谱可视化）
     - **Stress**: 持续进行图形渲染压力测试
     - **Render**: 图形渲染能力测试 (v9 新增)
     - **Scroll**: 滚动性能测试 (v9 新增)
     - **Transform**: 图形变换（旋转、缩放等）(v9 新增)
     - **Flex Layout**: Flex 弹性布局展示 (v9 新增)
     - **Multilang**: 多语言文字渲染 (v9 新增)

     触摸屏应能正常响应手指滑动和点击操作。
