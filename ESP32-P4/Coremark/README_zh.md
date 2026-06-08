---
sys: FreeRTOS
sys_ver: 

status: basics
last_update: 2026-05-07

model: ESP32-P4-Function-EV-Board
profile: Coremark

---

# RuyiSDK 基础示例

可直接在开发板上进行编译和运行的示例，适合初学者快速上手。

安装 ESP-IDF v5.5.4 及工具链

```
# 下载并运行 ESP-IDF 离线安装包（从乐鑫官网或 GitHub）
# 安装完成后，通过开始菜单中的 "ESP-IDF 5.5.4 PowerShell" 快捷方式打开终端
```

验证工具链

```
riscv32-esp-elf-gcc --version
idf.py --version
```

## Coremark (GCC版)

创建并配置项目

```
idf.py create-project-from-example "espressif/coremark:coremark_example"
cd coremark_example

idf.py set-target esp32p4
```

验证GCC版本

```
riscv64-esp-elf-gcc -v
```

编译并运行coremark（GCC）

```
idf.py build
idf.py -p COM6 flash

idf.py -p COM6 monitor
```

正常情况下，终端会看到类似如下输出：

```
...
Running coremark...
2K performance run parameters for coremark.
CoreMark Size    : 666
Total ticks      : 18325
Total time (secs): 18.325000
Iterations/Sec   : 1091.405184
Iterations       : 20000
Compiler version : GCC13.2.0
Compiler flags   : -ffunction-sections -fdata-sections -gdwarf-4 -ggdb -nostartfiles -nostartfiles -Og -fno-shrink-wrap -fstrict-volatile-bitfields -fno-jump-tables -fno-tree-switch-conversion -std=gnu17 -O3 -fjump-tables -ftree-switch-conversion
Memory location  : IRAM
seedcrc          : 0xe9f5
[0]crclist       : 0xe714
[0]crcmatrix     : 0x1fd7
[0]crcstate      : 0x8e3a
[0]crcfinal      : 0x382f
Correct operation validated. See README.md for run and reporting rules.
CoreMark 1.0 : 1091.405184 / GCC13.2.0 -ffunction-sections -fdata-sections -gdwarf-4 -ggdb -nostartfiles -nostartfiles -Og -fno-shrink-wrap -fstrict-volatile-bitfields -fno-jump-tables -fno-tree-switch-conversion -std=gnu17 -O3 -fjump-tables -ftree-switch-conversion / IRAM
CPU frequency: 360 MHz
I (28895) main_task: Returned from app_main()
...
```


按 `Ctrl + ]` 退出监视器。

## Coremark (LLVM版)

安装 Clang 工具链

```
python "$env:IDF_PATH/tools/idf_tools.py" install esp-clang
```

切换到 Clang 工具链

```
cd coremark_example
$env:IDF_TOOLCHAIN = "clang"
```

重新编译、烧录并运行

```
idf.py fullclean

idf.py build
idf.py -p COM6 flash monitor
```

正常情况下，终端会看到类似如下输出：

```
...
Running coremark...
2K performance run parameters for coremark.
CoreMark Size    : 666
Total ticks      : 18310
Total time (secs): 18.310000
Iterations/Sec   : 1092.295467
Iterations       : 20000
Compiler version : Clang-19.1.2
Compiler flags   : -ffunction-sections -fdata-sections -std=gnu17 -O3 -fno-exceptions -fno-rtti
Memory location  : IRAM
seedcrc          : 0xe9f5
[0]crclist       : 0xe714
[0]crcmatrix     : 0x1fd7
[0]crcstate      : 0x8e3a
[0]crcfinal      : 0x382f
Correct operation validated. See README.md for run and reporting rules.
CoreMark 1.0 : 1092.295467 / Clang-19.1.2 -ffunction-sections -fdata-sections -std=gnu17 -O3 -fno-exceptions -fno-rtti / IRAM
CPU frequency: 360 MHz
I (28895) main_task: Returned from app_main()
...
```

按 `Ctrl + ]` 退出监视器。

清理环境

```
idf.py fullclean
```

