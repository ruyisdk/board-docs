---
sys: FreeRTOS
sys_ver: null
sys_var: null

category: getting-started
last_update: 2026-05-07

model: ESP32-P4-Function-EV-Board
profile: Hello World

---

# RuyiSDK Getting Started Example

> Note: ESP32-P4 must be built with Espressif's official IDF toolchain. In this example, RuyiSDK is used only to create the virtual environment, obtain the source code, and edit `hello_world_main.c`; compilation and flashing are still performed with `idf.py`.

This example can be compiled and run directly on the development board, making it suitable for beginners.

Install the ruyi package manager (see the [official installation guide](https://ruyisdk.org/docs/Package-Manager/installation) for other methods)

```bash
sudo apt update; sudo apt install -y wget tar zstd xz-utils git build-essential
pip install esptool

wget https://mirror.iscas.ac.cn/ruyisdk/ruyi/tags/0.51.0/ruyi-0.51.0.amd64
chmod +x ./ruyi-0.51.0.amd64
sudo cp -v ./ruyi-0.51.0.amd64 /usr/local/bin/ruyi
```

Install the GCC and LLVM toolchains

```
ruyi update
ruyi install gnu-plct llvm-plct
```

Install ESP-IDF v5.5.4 and its toolchain

```
# Download and run the ESP-IDF offline installer
# After installation, open a terminal using the "ESP-IDF PowerShell" shortcut
```

## Hello World (GCC)

Create and configure the project

```
xcopy /e /i $env:IDF_PATH\examples\get-started\hello_world hello_world
cd hello_world

idf.py set-target esp32p4
```

Create and activate the ruyi virtual environment (GCC)

```
ruyi venv -t toolchain/gnu-plct manual venv-gnu-plct
. venv-gnu-plct/bin/ruyi-activate
```

Edit the source code in the virtual environment:

```
cd /mnt/d/platform/esp/hello_world/main
nano hello_world_main.c

#include <stdio.h>
void app_main(void)
{
    printf("Hello, World!\n");
}
```

Compile and run Hello World (GCC)

```
idf.py build
idf.py -p COM6 flash

idf.py -p COM6 monitor
```

Under normal circumstances, the terminal displays output similar to:

```
...
Hello world!
...
```

Press `Ctrl + ]` to exit the monitor.

## Hello World (LLVM)

Install the Clang toolchain

```
python "$env:IDF_PATH/tools/idf_tools.py" install esp-clang
```

Switch to the Clang toolchain

```
cd hello_world
$env:IDF_TOOLCHAIN = "clang"
```

Rebuild, flash, and run

```
idf.py fullclean

idf.py build
idf.py -p COM6 flash

idf.py -p COM6 monitor
```

Under normal circumstances, the terminal displays output similar to:

```
...
Hello world!
...
```

Press `Ctrl + ]` to exit the monitor.

Clean up the environment

```
idf.py fullclean
```
